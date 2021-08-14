import dash
import numpy as np
import plotly.graph_objs as go
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import os
dir_path = os.path.dirname(os.path.realpath(__file__))


class DaysUntilVacDataset:
    @staticmethod
    def load():
        return pd.read_csv(os.path.join(dir_path, "tempo-desde-17-por-uf-categorizado-agrupado.csv"))

    @staticmethod
    def filter_by_uf(df, uf):
        if uf != "Todos":
            df = df.query(f"paciente_endereco_uf==\"{uf}\"")
        df = df.drop("paciente_endereco_uf", axis=1) \
            .sort_values(["Dias até vacinar", "count"]) \
            .groupby(["categoria", "Dias até vacinar"]) \
            .sum() \
            .reset_index()
        df["Dias até vacinar"] = df["Dias até vacinar"].astype(int)
        return df

    @staticmethod
    def sort_by_mean(df):
        mean_df = df[["categoria", "count", "Dias até vacinar"]]
        mean_df["Dias até vacinar"] = mean_df["count"] * mean_df["Dias até vacinar"].astype(int)
        mean_df = mean_df.groupby("categoria").sum()
        mean_df["Média dias"] = mean_df["Dias até vacinar"] / mean_df["count"]
        mean_df = mean_df.drop(["count", "Dias até vacinar"], axis=1)
        return df.join(mean_df, on="categoria").sort_values(["Média dias", "Dias até vacinar"]).drop(["Média dias"],
                                                                                                     axis=1)

    @staticmethod
    def calculate_whiskers(q1, q3, min_, max_):
        iqr = q3 - q1
        lowerfence = max(q1 - iqr, min_)
        upperfence = min(q3 + iqr, max_)
        return lowerfence, upperfence

    @staticmethod
    def detect_quantiles(df):
        df = df.set_index("categoria")
        df["quantile1_pos"] = df.reset_index()[["categoria", "count"]].groupby("categoria").sum()["count"].apply(
            lambda c: c // 4)
        df["median_pos"] = df.reset_index()[["categoria", "count"]].groupby("categoria").sum()["count"].apply(
            lambda c: c // 2)
        df["quantile3_pos"] = df.reset_index()[["categoria", "count"]].groupby("categoria").sum()["count"].apply(
            lambda c: (3 * c) // 4)
        summary = {}
        for index in df.index.unique():
            category_df = df.loc[index]
            quantile1_pos = category_df.iloc[0]["quantile1_pos"]
            median_pos = category_df.iloc[0]["median_pos"]
            quantile3_pos = category_df.iloc[0]["quantile3_pos"]
            count_series = category_df["count"]
            acu = 0
            targets_pos = [quantile1_pos, median_pos, quantile3_pos]
            targets_values = []
            for i, c in enumerate(count_series):
                acu += c
                if len(targets_pos) == 0:
                    break
                if acu > targets_pos[0]:
                    targets_pos.pop(0)
                    value = category_df.iloc[i]["Dias até vacinar"]
                    targets_values.append(value)
            q1, median, q3 = targets_values
            min_, max_ = category_df.iloc[0]["Dias até vacinar"], category_df.iloc[-1]["Dias até vacinar"]
            lowerfence, upperfence = DaysUntilVacDataset.calculate_whiskers(q1, q3, min_, max_)
            targets_values.insert(0, lowerfence)
            targets_values.append(upperfence)
            summary[index] = targets_values
        return summary


class DaysUntilVac:
    fig: go.Figure
    df: pd.DataFrame

    def show(self):
        self.fig.show()

    def __init__(self, df=DaysUntilVacDataset.load(), uf="Todos"):
        with open(os.path.join(dir_path, "cache-color.txt")) as f:
            self.color_map = dict([line.rstrip().split(": ", maxsplit=1) for line in f.readlines()])
        self.df = df
        self.sorted_df = DaysUntilVacDataset.sort_by_mean(DaysUntilVacDataset.filter_by_uf(self.df, uf))
        self.summary = np.array(list(DaysUntilVacDataset.detect_quantiles(self.sorted_df).values()))
        self.generate_figure()

    def generate_figure(self):
        self.fig = go.Figure()
        for i, cat in zip(self.summary, self.sorted_df.set_index("categoria").index.unique()):
            color = self.color_map[cat]
            self.fig.add_trace(go.Box(x=[""], name=cat, lowerfence=[i[0]], q1=[i[1]], median=[i[2]],
                                      q3=[i[3]], upperfence=[i[4]], line=dict(color=color)))
        self.fig.update_layout(height=650, width=1300, font=dict(size=16), yaxis_title="Dias até vacinar",
                               boxmode="group")
        return self.fig


class DaysUntilVacDash(DaysUntilVac):
    def __init__(self, app: dash.Dash):
        super().__init__()
        uf_label = "paciente_endereco_uf"
        options = [{'label': i, 'value': i} for i in self.df.query(f'{uf_label}!="XX"')[uf_label].unique().tolist()]
        options.append({'label': "Todos", 'value': "Todos"})

        self.component_html = html.Div([
            html.Hr(),
            html.H4('Distribuição da vacinação por grupos em dias desde o início da vacinação'),
            html.H6('Nessa visualização utilizamos boxplots para representar a distribuição da vacinação por grupo' +
                    ' ao longo do tempo. O tempo é medido em dias desde a data de início da vacinação no Brasil ' +
                    '(17/01/2021) e quanto às interações suportadas temos a seleção de um subconjunto de grupos e ' +
                    'filtragem por UF (unidade federativa). Além disso, os grupos estão representados por cores ' +
                    'únicas e consistentes, o que facilita compará-los para uma ou mais UFs. '),
            html.Label("Selecione o estado"),
            html.Div([
                dcc.Dropdown(
                    id='uf',
                    options=options,
                    value='Todos',
                )
            ],
                style={'width': '48%', 'display': 'inline-block'}),
            dcc.Graph(id='days-util-vac')
        ])
        app.callback(Output('days-util-vac', 'figure'), Input('uf', 'value'))(self.callback)

    def callback(self, uf: str):
        self.sorted_df = DaysUntilVacDataset.sort_by_mean(DaysUntilVacDataset.filter_by_uf(self.df, uf))
        self.summary = np.array(list(DaysUntilVacDataset.detect_quantiles(self.sorted_df).values()))
        return self.generate_figure()
