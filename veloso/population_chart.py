import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
dir_path = os.path.dirname(os.path.realpath(__file__))


class PopulationChartDataset:
    @staticmethod
    def load():
        df = pd.read_csv(os.path.join(dir_path, "normalized-renamed-count-per-uf-sex-age.csv"), index_col=[0, 1, 2, 3])
        return df.unstack("sexo")["count"].drop("I", axis=1).reset_index().fillna(0)

    @staticmethod
    def extract_categories_array(merged_df):
        women = merged_df["Fpartial"].to_numpy().astype(int)
        men = merged_df["Mpartial"].apply(lambda c: -1 * c).to_numpy().astype(int)
        women_at_least_a_dose = merged_df["Fcomplete"].to_numpy().astype(int)
        men_at_least_a_dose = merged_df["Mcomplete"].apply(lambda c: -1 * c).to_numpy().astype(int)
        return men_at_least_a_dose, men, women_at_least_a_dose, women

    @staticmethod
    def filter_by_uf(df, uf):
        df = df.reset_index()
        if uf == "Todos":
            return df.groupby("idade").sum().reset_index()
        return df[df["uf"] == uf].groupby("idade").sum().reset_index()

    @staticmethod
    def split_by_groups(df):
        unica_df = df.query('dose=="Única"').query('uf!="XX"').drop("dose", axis=1)
        dose1_df = df.query('dose=="1a Dose"').query('uf!="XX"').drop("dose", axis=1)
        dose2_df = df.query('dose=="2a Dose"').query('uf!="XX"').drop("dose", axis=1)
        complete_df = unica_df.set_index(["uf", "idade"]).add(dose2_df.set_index(["uf", "idade"]), fill_value=0)
        vaccinated_df = unica_df.set_index(["uf", "idade"]).add(dose1_df.set_index(["uf", "idade"]), fill_value=0)
        return complete_df, vaccinated_df


class PopulationChart:
    blue = "dodgerblue"
    pink = "rgb(255, 182, 193)"
    y = list(range(0, 221, 1))
    x = np.arange(-1000000, 1000001, 20000)
    fig: go.Figure
    complete_df: pd.DataFrame
    vaccinated_df: pd.DataFrame
    merged_df: pd.DataFrame
    df: pd.DataFrame

    def show(self):
        self.fig.show()

    def __init__(self, df=PopulationChartDataset.load()):
        self.df = df
        self.complete_df, self.vaccinated_df = PopulationChartDataset.split_by_groups(self.df)
        self.generate_figure()

    def generate_figure(self, category="Todos", x_range=None, fixed=True):
        if fixed is True:
            x_range = (-1000000, 1000000)
        if isinstance(x_range, tuple):
            step = (abs(x_range[1]) + abs(x_range[0])) / 10
            self.x = np.around(np.arange(x_range[0], x_range[1] + 1, step))
        vaccinated_aggregated_df = PopulationChartDataset.filter_by_uf(self.vaccinated_df, category)
        complete_aggregated_df = PopulationChartDataset.filter_by_uf(self.complete_df, category)
        self.fig = go.Figure(data=self.generate_bars(self.merge(complete_aggregated_df, vaccinated_aggregated_df)),
                             layout=self.generate_layout())
        self.fig.update_layout(height=960, font=dict(size=16))
        return self.fig

    def generate_layout(self):
        return go.Layout(yaxis=go.layout.YAxis(title='Idade (em anos)'),
                         xaxis=go.layout.XAxis(
                             range=[self.x[0], self.x[-1]],
                             tickvals=[t for t in self.x],
                             ticktext=[abs(t) for t in self.x]),
                         font=dict(
                             size=16),
                         barmode='overlay',
                         bargap=0.1,
                         autosize=True)

    def generate_bars(self, merged_df):
        men_complete, men, women_complete, women = PopulationChartDataset.extract_categories_array(merged_df)

        return [self.generate_bar(women, "Mulheres que receberam ao menos uma dose", self.pink,
                                  opacity=0.5),
                self.generate_bar(men, "Homens que receberam ao menos uma dose", self.blue,
                                  text=-1 * men, opacity=0.5),
                self.generate_bar(women_complete, "Mulheres completamente imunizadas", self.pink),
                self.generate_bar(men_complete, "Homens completamente imunizadas", self.blue,
                                  text=-1 * men_complete)]

    def generate_bar(self, x, legend_text, color, opacity=1.0, text=None):
        text = x if text is None else text
        return go.Bar(y=self.y,
                      x=x,
                      orientation='h',
                      name=legend_text,
                      text=text,
                      hovertext=text.astype(str),
                      hoverinfo='text',
                      showlegend=True,
                      opacity=opacity,
                      marker=dict(color=color)
                      )

    def merge(self, full_df, partial_df):
        return full_df.set_index("idade").join(partial_df.set_index("idade"), how="inner", lsuffix="complete",
                                               rsuffix="partial")


class PopulationChartDash(PopulationChart):
    def __init__(self, app: dash.Dash):
        super().__init__()

        options = [{'label': i, 'value': i} for i in self.df.query('uf!="XX"')["uf"].unique().tolist()]
        options.append({'label': "Todos", 'value': "Todos"})

        self.component_html = html.Div([
            html.Hr(),
            html.H4('População vacinada e imunizada por sexo e idade'),
            html.Label("Selecione o estado"),
            html.Div([
                dcc.Dropdown(
                    id='unidade_federativa',
                    options=options,
                    value='Todos',
                ),
                dcc.RadioItems(
                    id='fixedscale',
                    options=[{"label": "Escala fixa", "value": 1},
                             {"label": "Escala dinâmica", "value": 0}],
                    value=1
                )
            ],
                style={'width': '48%', 'display': 'inline-block'}),
            dcc.Graph(id='piramide-populacional')
        ])
        cb_params = [Output('piramide-populacional', 'figure'), Input('unidade_federativa', 'value'), Input('fixedscale', 'value')]
        app.callback(*cb_params)(self.callback)

    @staticmethod
    def callback(unidade_federativa: str, fixedscale: int):
        pop = PopulationChart()
        df = PopulationChartDataset.filter_by_uf(pop.vaccinated_df, unidade_federativa)
        max_range = abs(max(df["M"].max(), df["F"].max()))
        return pop.generate_figure(unidade_federativa, x_range=(-max_range, max_range), fixed=fixedscale == 1)
