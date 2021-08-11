import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from stacked_area import stacked_area
from overlaid import overlaid_area

import numpy as np
import pandas as pd


def grafico_total_vacinas_tipo_dose(app):
    df = pd.read_csv("total_dose.csv")
    df = df[df['Semana de aplicação'] != 25]
    estados = ['Todos'] + df['Estado'].unique().tolist()
    opcoes = [{'label': i, 'value': i} for i in estados]

    component_html = html.Div([
        html.Hr(),
        html.H4('Total acumulado de vacinas aplicadas a cada semana'),
        html.Label("Selecione o estado"),
        html.Div([
            dcc.Dropdown(
                id='estado-total-vacinas-dose',
                options=opcoes,
                value='Todos',
            )
        ],
            style={'width': '48%', 'display': 'inline-block'}),
        dcc.Graph(id='total-vacinas-dose')
    ])

    @app.callback(
        Output('total-vacinas-dose', 'figure'),
        Input('estado-total-vacinas-dose', 'value'))
    def update_total_vacinas_tipo_dose(estado):
        df = pd.read_csv("total_dose.csv")
        df = df[df['Semana de aplicação'] != 25]
        if estado != "Todos":
            df = df[df['Estado'] == estado]

        df['Semana de aplicação'] = semana(df['Semana de aplicação'].tolist()) - 2
        # df = pd.concat([df, pd.DataFrame(
        #     {'Semana de aplicação': [i for i in range(30)], 'Dose': ['Vacinação completa'] * 30})],
        #                ignore_index=True)
        # df = pd.concat([df, pd.DataFrame(
        #     {'Semana de aplicação': [i for i in range(30)], 'Dose': ['Primeira dose'] * 30})],
        #                ignore_index=True)
        semana_aplicacao_dose = df.groupby(by=['Semana de aplicação', 'Dose']).apply(
            lambda e: pd.DataFrame({'Total (semana)': [e['Total (semana)'].sum()]})).reset_index()[
            ['Semana de aplicação', 'Dose', 'Total (semana)']]

        fig = overlaid_area(semana_aplicacao_dose, x_column='Semana de aplicação', y_column='Total (semana)',
                            filename='total_dose_semana.html', category='Dose')

        return fig

    return component_html


def areas_empilhadas(app):
    df = pd.read_csv("areas_empilhadas.csv")
    df = df[df['Semana de aplicação'] != 25]
    estados = ['Todos'] + df['Estado'].unique().tolist()
    opcoes = [{'label': i, 'value': i} for i in estados]

    component_html = html.Div([
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

    @app.callback(
        Output('areas-empilhadas', 'figure'),
        Input('estado', 'value'))
    def update_areas_empilhadas(estado):
        df = pd.read_csv("areas_empilhadas.csv")
        df = df[df['Semana de aplicação'] != 25]
        if estado != "Todos":
            df = df[df['Estado'] == estado]

        df['Semana de aplicação'] = semana(df['Semana de aplicação'].tolist()) - 2
        semana_aplicaca_por_vacina = \
            df.groupby(by=['Semana de aplicação', 'Nome da vacina']).apply(
                lambda e: pd.DataFrame({'Total (semana)': [e['Total (semana)'].sum()]})).reset_index()

        semana_aplicaca_por_vacina = semana_aplicaca_por_vacina[
            ['Semana de aplicação', 'Total (semana)', 'Nome da vacina']]

        fig = stacked_area(semana_aplicaca_por_vacina, x_column='Semana de aplicação', y_column='Total (semana)',
                           category="Nome da vacina", filename='semana_aplicacao_nome_vacina.html')

        return fig

    return component_html


def semana(l):
    convert = {1: 7, 2: 8, 3: 9, 4: 10, 5: 11, 6: 12, 7: 13, 8: 14, 9: 15, 10: 16, 11: 17, 12: 18, 13: 19, 14: 20,
               15: 21, 16: 22, 17: 23, 18: 24, 19: 25, 20: 26, 21: 27, 22: 28, 23: 29, 24: 30, 33: 1, 38: 2, 40: 3,
               51: 4, 52: 5, 53: 6}

    for i in range(len(l)):
        l[i] = convert[l[i]] - 1

    return np.array(l)


def graficos_capanema(app):
    components_html = []

    components_html.append(areas_empilhadas(app))

    components_html.append(grafico_total_vacinas_tipo_dose(app))

    return components_html
