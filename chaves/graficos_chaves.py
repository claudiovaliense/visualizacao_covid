# -*- coding: utf-8 -*-
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import os

class GraficoChaves:
    def atualizar(self, estado, tipo):
        dir_path = os.path.dirname(os.path.realpath(__file__)) + "/"
        df = pd.read_csv(dir_path + "casos.csv")
        if estado == 'Todos':
            e = 'br'
        else:
            e = estado.lower()
            
        df = df.loc[df["Estado"] == e]
        if tipo == "O":
            x_M =-df.Obitos_M
            x_F = df.Obitos_F
        else:
            x_M =-df.Casos_M
            x_F = df.Casos_F
            
        fig = [go.Bar(y = pd.unique(df.Idade),
                       x=x_F, 
                       name = "Mulheres",
                       orientation ='h',
                       hoverinfo='x',
                       marker=dict(color="lightpink")
                      ),
                go.Bar(y = pd.unique(df.Idade),
                       x=x_M, 
                       name = "Homens",
                       orientation ='h',
                       hoverinfo='x',
                       marker=dict(color="dodgerblue")
                      )]
        return {'data':fig}
    
    def comparativo_casos(self, app):
        dir_path = os.path.dirname(os.path.realpath(__file__)) + "/"
        df = pd.read_csv(dir_path + "casos.csv")
        estados = ['Todos'] + [e.upper() for e in pd.unique(df['Estado'])]
        opcoes = [{'label': e, 'value': e} for e in estados]
        
        component_html = html.Div([
            html.Hr(),
            html.H3('Casos e óbitos confirmados até 11/08/2021'),
            html.H5('Nesta visualização são mostradas duas pirâmides etárias, o que facilita comparação entre estados ou casos e óbitos de um mesmo estado. Fonte: OpenDataSUS'),
            html.Div([
                html.Div([
                    html.Div([html.Label('Selecione o estado'),
                    dcc.Dropdown(
                    id = 'drop_estados1',
                    clearable=False,
                    options = opcoes,
                    value = 'Todos',
                    )
                ], style={'width': '50%'}),
                    html.Div([dcc.RadioItems(
                    id = 'tipo1',
                    options=[
                    {'label': "Casos", 'value': 'C'},
                    {'label': 'Óbitos', 'value': 'O'},
                    ], value='C',
                    labelStyle={'display': 'inline-block'})
                    ]),
                    dcc.Graph(id = 'piramide-casos1')
                ], style={'width': '47%', 'display': 'inline-block'}),
                html.Div([
                    html.Div([html.Label('Selecione o estado'),
                    dcc.Dropdown(
                    id = 'drop_estados2',
                    clearable=False,
                    options = opcoes,
                    value = 'Todos',
                    )
                ], style={'width': '50%'}),
                html.Div([dcc.RadioItems(
                    id = 'tipo2',
                    options=[
                    {'label': "Casos", 'value': 'C'},
                    {'label': 'Óbitos', 'value': 'O'},
                    ], value='C',
                    labelStyle={'display': 'inline-block'})
                    ]),
                    dcc.Graph(id = 'piramide-casos2')   
                ], style={'width': '47%', 'display': 'inline-block', 'align': 'right'})
            ])
        ])
        
        @app.callback(
        Output('piramide-casos1', 'figure'),
        Input('drop_estados1', 'value'),
        Input('tipo1', 'value')
        )
        def update_piramide1(estado, tipo):
            return self.atualizar(estado, tipo)
        
        @app.callback(
            Output('piramide-casos2', 'figure'),
            Input('drop_estados2', 'value'),
            Input('tipo2', 'value')
        )
        def update_piramide2(estado, tipo):
            return self.atualizar(estado, tipo)
        
        return [component_html]
