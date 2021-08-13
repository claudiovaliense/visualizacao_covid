import dash
import numpy as np
import plotly.graph_objs as go
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import os

class PopulationChartDataset:
    @staticmethod
    def load():
        dir_path = os.path.dirname(os.path.realpath(__file__)) + "/"
        df = pd.read_csv(dir_path + "normalized-renamed-count-per-uf-sex-age.csv", index_col=[0, 1, 2, 3])
        return df.unstack("sexo")["count"].drop("I", axis=1).reset_index().fillna(0)

    @staticmethod
    def extract_categories_array(merged_df):
        women = merged_df["Fpartial"].apply(lambda c: -1 * c).to_numpy().astype(int)
        men = merged_df["Mpartial"].to_numpy().astype(int)
        women_at_least_a_dose = merged_df["Fcomplete"].apply(lambda c: -1 * c).to_numpy().astype(int)
        men_at_least_a_dose = merged_df["Mcomplete"].to_numpy().astype(int)
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
    blue = "rgb(0, 102, 255)"
    dark_blue = "rgb(0, 102, 153)"
    pink = "rgb(255, 0, 255)"
    dark_pink = "rgb(155, 0, 155)"
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
        if isinstance(x_range, tuple):
            step = (abs(x_range[1]) + abs(x_range[0])) / 10
            self.x = np.arange(x_range[0], x_range[1], step)
        vaccinated_aggregated_df = PopulationChartDataset.filter_by_uf(self.vaccinated_df, category)
        complete_aggregated_df = PopulationChartDataset.filter_by_uf(self.complete_df, category)
        self.fig = go.Figure(data=self.generate_bars(self.merge(complete_aggregated_df, vaccinated_aggregated_df)),
                             layout=self.generate_layout(fixed=fixed))
        return self.fig

    def generate_layout(self, fixed=True):
        if fixed:
            range_ = [-1000000, 1000000]
        else:
            range_ = [self.x[0], self.x[-1]]
        return go.Layout(yaxis=go.layout.YAxis(title='Idade (em anos)'),
                         xaxis=go.layout.XAxis(
                             range=range_,
                             tickvals=list(map(int, self.x)),
                             ticktext=[abs(int(t)) for t in self.x]),
                         barmode='overlay',
                         bargap=0.1,
                         autosize=True,
                         height=960)

    def generate_bars(self, merged_df):
        men_complete, men, women_complete, women = PopulationChartDataset.extract_categories_array(merged_df)

        return [self.generate_bar(men, "Homens que receberam ao menos uma dose", self.blue,
                                  opacity=0.5),
                self.generate_bar(women, "Mulheres que receberam ao menos uma dose", self.pink,
                                  text=-1 * women, opacity=0.5),
                self.generate_bar(men_complete, "Homens completamente imunizadas", self.dark_blue),
                self.generate_bar(women_complete, "Mulheres completamente imunizadas", self.dark_pink,
                                  text=-1 * women_complete)]

    def generate_bar(self, x, legend_text, color, opacity=1.0, text=x):
        return go.Bar(y=self.y,
                      x=x,
                      orientation='h',
                      name=legend_text,
                      text=text,
                      hoverinfo='x',
                      showlegend=True,
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
