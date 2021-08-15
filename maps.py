#Author: Claudio Moises Valiense de Andrade. Licence: MIT. Objective: Visualizar dados do covid
import claudio_funcoes_usage as cv # function usage geral
import matplotlib.pyplot as plt # plot static
import plotly.express as px # plot dynamic
import datetime # time
import statistics # function statistics
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly
#maps
import json
from urllib.request import urlopen
import pandas as pd
import numpy

def read_data():
    """Read data"""
    #filtered.csv': paciente_datanascimento;paciente_enumsexobiologico;paciente_racacor_codigo;paciente_endereco_uf;vacina_grupoatendimento_codigo;vacina_dataaplicacao;vacina_descricao_dose;vacina_codigo
    dados = cv.arquivo_para_corpus_delimiter(f'dataset/vacinaOpenDataSUS/filtered.csv', ';', 1000) # arquivo com os dados     
    grupo_categoria = cv.arquivo_para_corpus_delimiter(f'dataset/vacinaOpenDataSUS/grupo-categoria.csv', ';') # 4 vacina_grupoatendimento_codigo[ vacina_grupoatendimento_codigo;vacina_grupoatendimento_nome;vacina_categoria_nome ]
    #grupo = cv.arquivo_para_corpus_delimiter(f'dataset/vacinaOpenDataSUS/grupo.csv', ';')
    raca = cv.arquivo_para_corpus_delimiter(f'dataset/vacinaOpenDataSUS/raca.csv', ';') # paciente_racacor_codigo, 2
    tipos_vacina = cv.arquivo_para_corpus_delimiter(f'dataset/vacinaOpenDataSUS/vacina.csv', ';') # vacina_codigo 7
    
    vacinas_estado = dict()
    for index in range(1,len(dados)):        
        age = int( ( datetime.datetime.today() - datetime.datetime.strptime(dados[index][0], '%Y-%m-%d')).days / 365.25 )
        if vacinas_estado.get( dados[index][3] ) == None: 
            vacinas_estado[ dados[index][3] ] = {'qtd' : 0, 'age' : [] }
        vacinas_estado[ dados[index][3] ] ['qtd'] +=1  # estado    
        vacinas_estado[ dados[index][3] ] ['age'].append(age)  # idade    
    
    vacinas_estado = cv.remove_key_dict(vacinas_estado, 'XX'); vacinas_estado = cv.remove_key_dict(vacinas_estado, 'paciente_endereco_uf')    
    for k in vacinas_estado:        
        vacinas_estado[k]['age_media'] = statistics.mean( vacinas_estado[k]['age'] )  
        vacinas_estado[k]['age_histogram'] = numpy.histogram(vacinas_estado[k]['age'], bins=10) 
    
    dados = {'sigla': list(vacinas_estado.keys()), 'age_media' : [vacinas_estado[k]['age_media'] for k in vacinas_estado], 'age_histogram' : [vacinas_estado[k]['age_histogram'] for k in vacinas_estado]}
    dados = pd.DataFrame(dados  )
    
    brasil = json.load(open( 'dataset/mapa_brasil'))
    
    #print(brasil)
    for feature in brasil['features']:                
        feature['id'] = feature['properties']['sigla']    
    
    fig = px.choropleth(dados,
        locations='sigla',
        geojson = brasil,
        color='age_media',
        #hover_data=['age_histogram'],
        scope='south america'
    )    
    #fig.show()
        
    #fig = px.bar(x=list(vacinas_estado.keys()), y=[vacinas_estado[k]['qtd'] for k in vacinas_estado]) 
    #fig.update_layout(xaxis_title='Estados', yaxis_title='Quantidade de vacinas')
    #fig.show()    
    fig.write_html("html/mapa.html")


if __name__ == "__main__":
    #with urlopen('https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson') as response:
    #brazil = json.load(response) # Javascrip object notation 
    #json.dump(brazil, open('dataset/mapa_brasil', 'w'))
    
    
    
    
    
    read_data()

# backup -----------------

#print(brasil)
#soybean = pd.read_csv('https://raw.githubusercontent.com/nayanemaia/Dataset_Soja/main/soja%20sidra.csv')
#print(soybean)
#print(dados)

''' # gráfico estatico
plt.bar(vacinas_estado.keys(), vacinas_estado.values())
plt.xlabel('Estados')
plt.ylabel('Quantidade de vacinas')
plt.show()'''

'''  # uso de dash  
import dash
import dash_core_components as dcc
import dash_html_components as html
from base64 import b64encode
import io
app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig),
    dcc.Graph(figure=fig2)
])    
app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter
'''

''' # salvar figura em html separado
fig2 = px.bar(x=list(vacinas_estado.keys()), y=[vacinas_estado[k]['qtd'] for k in vacinas_estado]) 
fig2.update_layout(xaxis_title='Estados', yaxis_title='Quantidade de vacinas')
fig2.show()    
fig2.write_html("html/vacina_estado.html")
'''

''' # exemplo com subplot
figsub = make_subplots(rows=2, cols=1)        
figsub.add_trace( go.Bar(x=list(vacinas_estado.keys()), y=[vacinas_estado[k]['qtd'] for k in vacinas_estado]), 1, 1) 
figsub.add_trace( go.Bar(x=list(vacinas_estado.keys()), y=[vacinas_estado[k]['age'] for k in vacinas_estado]), 2, 1) 
figsub.update_xaxes(title_text="Estados", row=1, col=1); figsub.update_yaxes(title_text="Quantidade de vacinas", row=1, col=1)
figsub.update_xaxes(title_text="Estados", row=2, col=1); figsub.update_yaxes(title_text="Média da idade dos vacinados", row=2, col=1)        
figsub.update_layout(showlegend=False) 
figsub.show() 
figsub.write_html("html/vacina.html")
'''