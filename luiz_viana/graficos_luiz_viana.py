import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


import pandas as pd
from .barras_fx_etaria import barras_fx_etaria, barras_sub_plot_vacina

def grafico_total_vacinas_idade(app):
    df = pd.read_csv("luiz_viana/data_set_consolidado_vacina.csv")
    df = df[df['paciente_endereco_uf'] != 'XX']
    
    estados = df['paciente_endereco_uf'].unique().tolist()
    estados.sort()
    estados = ['Todos'] + estados
    opcoes = [{'label': i, 'value': i} for i in estados]
    
    sexo = ['Masculino', 'Feminino']
    opcoes_sexo = [{'label': i, 'value': i[0]} for i in sexo]
    
    
    fx_etaria = df['faixa_etaria'].unique().tolist()
    fx_etaria = [int(item) for item in fx_etaria]
    fx_etaria.sort()
    opcoes_fx_etaria = [{'label': 'de {} a {}'.format(i, i+10 ), 'value': i} 
                                                for i in fx_etaria]
    
    component_html = html.Div([
            html.Hr(),
            html.H4('Vacinas Aplicadas por dia de acordo com a Faixa Etária'),
            html.H6('teste'),
            html.Label("Filtros"),
            html.Div(
            [   
                    html.Div([
                        html.Label("Sexo:"),
                        html.Label("Faixa Etária:"),
                        #html.Label("Estado"),
                        ], style={'width': '10%', 'display': 'inline-block'}),
                    
                    html.Div(
                    [
                    dcc.Checklist(
                        id='sexo-filter2',
                        options=opcoes_sexo,
                        value=['M','F'],
                        labelStyle={'display': 'inline-block'}
                    ),
                    
                    dcc.Checklist(
                        id='fx_etaria-filter',
                        options=opcoes_fx_etaria,
                        value=fx_etaria,
                        labelStyle={'display': 'inline-block'}
                    ),
                    
                    ], style={'width': '90%', 'display': 'inline-block'}),
            ], className="row"),
            html.Div(
            [   
                html.Div(
                [   
                    html.Label("Estado"),
                ], style={'width': '10%', 'display': 'inline-block'}),
                
                html.Div([
                    dcc.Dropdown(
                        id='estado-filter',
                        options=opcoes,
                        value='Todos',
                        style={"width": "40%"}
                    ),
                    
                 ], style={'width': '90%', 'display': 'inline-block'}),
            ]),
            html.Div(
            [
                dcc.Graph(id='vacinas-fx_etaria')
            ])
        ])

    @app.callback(
        Output('vacinas-fx_etaria', 'figure'),
        Input('estado-filter', 'value'),
        Input('sexo-filter', 'value'),
        Input('fx_etaria-filter', 'value'))
    def update_dataset_fx_etaria(estado, sexo, fx_etaria):

        df = pd.read_csv("luiz_viana/data_set_consolidado_vacina.csv")
        df = df[df['paciente_endereco_uf'] != 'XX']
        r_min = 0
        r_max = df.groupby(['vacina_dataaplicacao'], 
             as_index=False)['quantidade'].sum()['quantidade'].max() + 100000
        
        fx_etaria_opts = df['faixa_etaria'].unique().tolist()
        

        if estado != "Todos":
            df = df[df['paciente_endereco_uf'] == estado]
            
            r_min = 0
            r_max = df.groupby(['vacina_dataaplicacao'], 
             as_index=False)['quantidade'].sum()['quantidade'].max() + 100000
        
        for sx in ('M','F'):
           if sx not in sexo:
               df = df[df['paciente_enumsexobiologico'] != sx]    
        
        if fx_etaria is not None:
            for fx in fx_etaria_opts:
                if fx not in fx_etaria:
                    df = df[df['faixa_etaria'] != fx]    


        data_fx = df.groupby(['vacina_dataaplicacao', 'faixa_etaria'], 
                                           as_index=False)['quantidade'].sum()
        
        fx0 = [{'vacina_dataaplicacao': '2021-01-31', 'faixa_etaria': 0,
                                'quantidade': 0}]
        
        fx100 = [{'vacina_dataaplicacao': '2021-01-31', 'faixa_etaria': 100,
                                'quantidade': 0}]
        
        data_fx.loc[len(data_fx.index)]=list(fx0[0].values())
        data_fx.loc[len(data_fx.index)]=list(fx100[0].values())
        

        fig = barras_fx_etaria(data_fx, r_min, r_max)

        return fig

    return component_html

def grafico_sub_plot_vacinas_idade(app):
    df = pd.read_csv("luiz_viana/data_set_consolidado_vacina.csv")
    df = df[df['paciente_endereco_uf'] != 'XX']
    
    estados = df['paciente_endereco_uf'].unique().tolist()
    estados.sort()
    estados = ['Todos'] + estados
    opcoes = [{'label': i, 'value': i} for i in estados]
    
    sexo = ['Masculino', 'Feminino']
    opcoes_sexo = [{'label': i, 'value': i[0]} for i in sexo]
    
    
    fx_etaria = df['faixa_etaria'].unique().tolist()
    fx_etaria = [int(item) for item in fx_etaria]
    fx_etaria.sort()
    opcoes_fx_etaria = [{'label': 'de {} a {}'.format(i, i+10 ), 'value': i} 
                                                for i in fx_etaria]
    
    component_html = html.Div([
            html.Hr(),
            html.H4('Vacinas Aplicadas por dia de acordo com a Faixa Etária'),
            html.H6('Nesta visualização são exibidos cinco gráficos '+
                    'onde podemos verificar ao longo de todo o período qual '+
                    'vacina foi predominantemente aplicada ' +
                    'por faixa etária.'),
            html.Label("Filtros"),
            html.Div(
            [   
                    html.Div([
                        html.Label("Sexo:"),
                        html.Label("Faixa Etária:"),
                        #html.Label("Estado"),
                        ], style={'width': '10%', 'display': 'inline-block'}),
                    
                    html.Div(
                    [
                    dcc.Checklist(
                        id='sexo-filter',
                        options=opcoes_sexo,
                        value=['M','F'],
                        labelStyle={'display': 'inline-block'}
                    ),
                    
                    dcc.Checklist(
                        id='fx_etaria-filter',
                        options=opcoes_fx_etaria,
                        value=fx_etaria,
                        labelStyle={'display': 'inline-block'}
                    ),
                    
                    ], style={'width': '90%', 'display': 'inline-block'}),
            ], className="row"),
            html.Div(
            [   
                html.Div(
                [   
                    html.Label("Estado"),
                ], style={'width': '10%', 'display': 'inline-block'}),
                
                html.Div([
                    dcc.Dropdown(
                        id='estado-filter',
                        options=opcoes,
                        value='Todos',
                        style={"width": "40%"}
                    ),
                    
                 ], style={'width': '90%', 'display': 'inline-block'}),
            ]),
            html.Div(
            [
                dcc.Graph(id='vacinas-fx_etaria')
            ])
        ])

    @app.callback(
        Output('vacinas-fx_etaria', 'figure'),
        Input('estado-filter', 'value'),
        Input('sexo-filter', 'value'),
        Input('fx_etaria-filter', 'value'))
    def update_dataset_fx_etaria(estado, sexo, fx_etaria):

        df = pd.read_csv("luiz_viana/data_set_consolidado_vacina.csv")
        df = df[df['paciente_endereco_uf'] != 'XX']
        r_min = 0
        r_max = df.groupby(['vacina_dataaplicacao'], 
             as_index=False)['quantidade'].sum()['quantidade'].max() * 1.1
        
        fx_etaria_opts = df['faixa_etaria'].unique().tolist()
        

        if estado != "Todos":
            df = df[df['paciente_endereco_uf'] == estado]
            
            r_min = 0
            r_max = df.groupby(['vacina_dataaplicacao'], 
             as_index=False)['quantidade'].sum()['quantidade'].max() * 1.1
        
        for sx in ('M','F'):
           if sx not in sexo:
               df = df[df['paciente_enumsexobiologico'] != sx]    
        
        if fx_etaria is not None:
            for fx in fx_etaria_opts:
                if fx not in fx_etaria:
                    df = df[df['faixa_etaria'] != fx]    


        data_fx = df.groupby(['vacina_dataaplicacao', 'faixa_etaria',
                                                  'vacina_nome'], 
                                           as_index=False)['quantidade'].sum()
        
      

        fig = barras_sub_plot_vacina(data_fx, r_min, r_max)

        return fig


    return component_html



def graficos_luiz_viana(app):

    components_html = []

    #components_html.append(grafico_total_vacinas_idade(app))
    
    components_html.append(grafico_sub_plot_vacinas_idade(app))

    return components_html