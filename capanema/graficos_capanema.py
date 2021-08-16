import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from .stacked_area import stacked_area
from .overlaid import overlaid_area
import os

import numpy as np
import pandas as pd

def semana(l):
    convert = {1: 7, 2: 8, 3: 9, 4: 10, 5: 11, 6: 12, 7: 13, 8: 14, 9: 15, 10: 16, 11: 17, 12: 18, 13: 19, 14: 20,
               15: 21, 16: 22, 17: 23, 18: 24, 19: 25, 20: 26, 21: 27, 22: 28, 23: 29, 24: 30, 33: 1, 38: 2, 40: 3,
               51: 4, 52: 5, 53: 6}

    # isso é feito porque a função "dt.weekday" do pandas retorna a semana do ano em correspondente á respectiva data.
    # Porém, a vacinação de fato começou na semana 3 de 2020. Mas para não ficar estranho, é necessário fazer um ajuste para a vacinação começar da semana 1
    convert = {1:7, 2:8, 3:9, 4:10, 5:11, 6:12, 7:13, 8:14, 9:15, 10:16, 11:17, 12:18, 13:19, 14:20, 15:21, 16:22, 17:23, 18:24, 19:25, 20:26, 21:27, 22:28, 23:29, 24:30, 33:1, 38:2, 40:3, 51:4, 52:5, 53:6}

    for i in range(len(l)):
        l[i] = convert[l[i]] - 1

    return np.array(l)


class GraficosCapanema:

    def start(self, app):

        return [[self.areas_empilhadas(app)], [self.grafico_total_vacinas_tipo_dose(app)]]

    def areas_empilhadas(self, app):


        # change the current directory
        # to specified directory

        df = pd.read_csv("capanema/areas_empilhadas.csv")
        df = df[df['Semana de aplicação'] != 25]
        estados = ['Todos'] + df['Estado'].unique().tolist()
        opcoes = [{'label': i, 'value': i} for i in estados]

        component_html = html.Div([
            html.Hr(),
            html.H4('Porcentagem de aplicação por semana para cada tipo de vacina'),
            html.H6('Esta visualização exibe a porcentagem semanal de aplicações de cada marca de vacina. Durante a maior parte das semanas, a vacina da Coronavac foi predominante. No entanto, ao longo do tempo a Coronavac tem perdido espaço para a Astrazeneca.'),
            html.Label("Selecione o estado"),
            html.Div([
                dcc.Dropdown(
                    id='estado-areas-empihadas',
                    options=opcoes,
                    value='Todos',
                )
            ],
                style={'width': '48%', 'display': 'inline-block'}),
            dcc.Graph(id='areas-empilhadas')
        ])

        @app.callback(
            Output('areas-empilhadas', 'figure'),
            Input('estado-areas-empihadas', 'value'))
        def update_areas_empilhadas(estado):
            df = pd.read_csv("capanema/areas_empilhadas.csv")
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

    def grafico_total_vacinas_tipo_dose(self, app):
        df = pd.read_csv("capanema/total_dose.csv")
        # a semana 25 é uma semana incompleta e por isso é retirada
        df = df[df['Semana de aplicação'] != 25]
        estados = ['Todos'] + df['Estado'].unique().tolist()
        opcoes = [{'label': i, 'value': i} for i in estados]

        component_html = html.Div([
            html.Hr(),
            html.H4('Total acumulado de vacinas aplicadas a cada semana'),
            html.H6("Esta visualização exibe o total acumulado de aplicações da primeira dose (azul claro) e vacinação completa que inclui a segunda dose ou dose única (azul escuro). É possível observar que apartir da semana 19 a curva da primeira dose se distância da curva da vacinação completa. Neste período, a maior parte das vacinas aplicadas era da Astrazeneca, que exibe um período maior entre a primeira e segunda doses."),
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
            df = pd.read_csv("capanema/total_dose.csv")
            # a semana 25 é uma semana incompleta e por isso é retirada
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