import dash
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from pandas.core.groupby import DataFrameGroupBy
import dash_html_components as html
import dash_core_components as dcc


class StackedArea:
    azul = "rgb(0, 102, 255)"
    azul_escuro = "rgb(0, 102, 153)"
    rosa = "rgb(255, 0, 255)"
    laranja = "rgb(255, 153, 0)"
    verde = "rgb(0, 153, 51)"
    vermelho = "rgb(204, 0, 0)"
    roxo = "rgb(153, 51, 153)"
    marrom = "rgb(153, 102, 51)"
    color = [azul, laranja, azul_escuro, roxo, rosa, marrom]
    fig: go.Figure
    total_df: pd.DataFrame
    categories: pd.DataFrame
    semanas: pd.DataFrame
    df: pd.DataFrame

    def show(self):
        self.fig.show()

    def __init__(self, df: pd.DataFrame, category: str, x_col: str, y_col: str):
        self.df = df
        self.categories = df[category].unique().tolist()
        self.total_df = self.generate_total_df(x_col)
        df['Total semana (%)'] = self.calculate_percentage(x_col)
        self.fig = self.generate_figure(category, x_col, y_col)

    def generate_total_df(self, x_col: str) -> pd.DataFrame:
        result = self.df.groupby(x_col).apply(self.calculate_total).reset_index()
        result.columns = [x_col, 'to be removed', 'Total dia (semana)']
        return result[[x_col, 'Total dia (semana)']]

    @staticmethod
    def calculate_total(grouped_df: DataFrameGroupBy) -> pd.DataFrame:
        result = {'Total (semana)': [sum(grouped_df['Total (semana)'].tolist())]}
        return pd.DataFrame(result)

    def calculate_percentage(self, x_col: str) -> pd.Series:
        df = self.df.join(self.total_df.set_index(x_col), on=x_col)
        return (df['Total (semana)'] / df['Total dia (semana)']) * 100

    def calculate_y(self, category, i, x_col, y_col):
        y = self.df[self.df[category] == self.categories[i]][y_col].tolist()
        return y + [1] * (len(self.df[x_col].unique().tolist()) - len(y))

    def generate_figure(self, category: str, x_col: str, y_col: str):
        fig = go.Figure()
        for i in range(len(self.categories)):
            y = self.calculate_y(category, i, x_col, y_col)
            if i == 0:
                fig.add_trace(go.Scatter(
                    x=(self.df[x_col].unique().tolist()), y=y,
                    mode='lines',
                    line=dict(width=0.5, color=self.color[i]),
                    name=self.categories[i],
                    stackgroup='one',
                    groupnorm='percent'  # sets the normalization for the sum of the stackgroup
                ))
            else:
                fig.add_trace(go.Scatter(
                    x=(self.df[x_col].unique().tolist()), y=y,
                    mode='lines',
                    line=dict(width=0.5, color=self.color[i]),
                    name=self.categories[i],
                    stackgroup='one'  # sets the normalization for the sum of the stackgroup
                ))
        fig.update_layout(
            showlegend=True,
            xaxis_type='category',
            yaxis=dict(
                type='linear',
                range=[1, 100],
                ticksuffix='%'),
            xaxis_title="Semana - início em 17/01/2021 até 20/06/2021",
            yaxis_title="Vacinas (%)",
            font=dict(size=25)
        )
        return fig


class StackedAreaDataset:
    @staticmethod
    def update(estado: str):
        df = StackedAreaDataset.load()
        if estado != "Todos":
            df = df[df['Estado'] == estado]

        semanas = df['Semana de aplicação'].tolist()
        convert = {1: 7, 2: 8, 3: 9, 4: 10, 5: 11, 6: 12, 7: 13, 8: 14, 9: 15, 10: 16, 11: 17, 12: 18, 13: 19,
                   14: 20, 15: 21, 16: 22, 17: 23, 18: 24, 19: 25, 20: 26, 21: 27, 22: 28, 23: 29, 24: 30, 33: 1,
                   38: 2, 40: 3, 51: 4, 52: 5, 53: 6}
        for i in range(len(semanas)):
            semanas[i] = convert[semanas[i]] - 1
        df['Semana de aplicação'] = np.array(semanas) - 2
        semana_aplicaca_por_vacina = df.groupby(by=['Semana de aplicação', 'Nome da vacina']).apply(
            lambda e: pd.DataFrame({'Total (semana)': [e['Total (semana)'].sum()]})).reset_index()

        semana_aplicaca_por_vacina = semana_aplicaca_por_vacina[
            ['Semana de aplicação', 'Total (semana)', 'Nome da vacina']]

        return semana_aplicaca_por_vacina

    @staticmethod
    def load():
        df = pd.read_csv("areas_empilhadas.csv")
        df = df[df['Semana de aplicação'] != 25]
        return df


class StackedAreaDash(StackedArea):
    def __init__(self, app: dash.Dash):
        df = StackedAreaDataset.update("Todos")
        super().__init__(df, "Nome da vacina", 'Semana de aplicação', 'Total (semana)')
        opcoes = [{'label': i, 'value': i} for i in
                  (['Todos'] + StackedAreaDataset.load()['Estado'].unique().tolist())]
        self.component_html = html.Div([
            html.Hr(),
            html.H4('Porcentagem de aplicação por semana para cada tipo de vacina'),
            html.Label("Selecione o estado"),
            html.Div([
                dcc.Dropdown(
                    id='estado',
                    options=opcoes,
                    value='Todos',
                )
            ],
                style={'width': '48%', 'display': 'inline-block'}),
            dcc.Graph(id='areas-empilhadas')
        ])
        app.callback(Output('areas-empilhadas', 'figure'), Input('estado', 'value'))(self.callback)

    @staticmethod
    def callback(estado: str):
        print(estado)
        return StackedArea(StackedAreaDataset.update(estado), "Nome da vacina", 'Semana de aplicação',
                               'Total (semana)').fig
