# -*- coding: utf-8 -*-
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

class GraficoChaves:
    
    def comparativo_casos(self, app):
        df = pd.read_csv("casos.csv")
        estados = ['Todos'] + [e.upper() for e in pd.unique(df['Estado'])]
        opcoes = [{'label': e, 'value': e} for e in estados]
        
        component_html = html.Div([
            html.Hr(),
            html.H4('Pirâmide etária de casos confirmados até 11/08/2021'),
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
                    dcc.Graph(id = 'piramide-casos2')            
                ], style={'width': '47%', 'display': 'inline-block', 'align': 'right'})
            ])
        ])
        
        @app.callback(
            Output('piramide-casos1', 'figure'),
            Input('drop_estados1', 'value')
        )
        
        def update_piramide1(estado):
            df = pd.read_csv("casos.csv")
            if estado == 'Todos':
                e = 'br'
            else:
                e = estado.lower()
            
            df = df.loc[df["Estado"] == e]
            
            fig = [go.Bar(y = pd.unique(df.Idade),
                           x=df.Casos_F, 
                           name = "Mulheres",
                           orientation ='h',
                           hoverinfo='x',
                           marker=dict(color="lightpink")
                          ),
                    go.Bar(y = pd.unique(df.Idade),
                           x=-df.Casos_M, 
                           name = "Homens",
                           orientation ='h',
                           hoverinfo='x',
                           marker=dict(color="dodgerblue")
                          )]
            return {'data':fig}
        
        @app.callback(
            Output('piramide-casos2', 'figure'),
            Input('drop_estados2', 'value')
        )
        
        def update_piramide2(estado):
            df = pd.read_csv("casos.csv")
            if estado == 'Todos':
                e = 'br'
            else:
                e = estado.lower()
            
            df = df.loc[df["Estado"] == e]
            
            fig = [go.Bar(y = pd.unique(df.Idade),
                           x=df.Casos_F, 
                           name = "Mulheres",
                           orientation ='h',
                           hoverinfo='x',
                           marker=dict(color="lightpink")
                          ),
                    go.Bar(y = pd.unique(df.Idade),
                           x=-df.Casos_M, 
                           name = "Homens",
                           orientation ='h',
                           hoverinfo='x',
                           marker=dict(color="dodgerblue")
                          )]
            return {'data':fig}
        
        return [component_html]