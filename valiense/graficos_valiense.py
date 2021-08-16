import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import claudio_funcoes_usage as cv # function usage geral
import pandas as pd
#from .barras_fx_etaria import barras_fx_etaria, barras_sub_plot_vacina
#maps
import plotly.express as px # plot dynamic
import datetime # time
import statistics # function statistics
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
        vacinas_estado[k]['age_median'] = statistics.median( vacinas_estado[k]['age'] )  
        vacinas_estado[k]['age_histogram'] = numpy.histogram(vacinas_estado[k]['age'], bins=10) 
    
    dados = {'sigla': list(vacinas_estado.keys()), 'média idade' : [vacinas_estado[k]['age_media'] for k in vacinas_estado],
        'mediana idade' : [vacinas_estado[k]['age_median'] for k in vacinas_estado],
        'age_histogram' : [vacinas_estado[k]['age_histogram'] for k in vacinas_estado]}
    dados = pd.DataFrame(dados  )    
    brasil = json.load(open( 'dataset/mapa_brasil'))
    
    nomes = []
    sigla_nome = {}
    for feature in brasil['features']:                
        feature['id'] = feature['properties']['sigla']    
        #nomes.append( feature['properties']['name'] )
        sigla_nome [ feature['properties']['sigla'] ]  =  feature['properties']['name'] 
    
    nomes_ordem = []    
    for d in dados['sigla']:
        #print(d)
        nomes_ordem.append(sigla_nome[d])
    dados['Nome'] = nomes_ordem
    
    #nomes_estados = ['Acre','Alagoas','Amazonas','Amapá','Bahia','Ceará','Espírito Santo','Goiás','Maranhão','Minas Gerais','Mato Grosso do Sul','Mato Grosso','Pará','Paraíba','Pernambuco','Piauí' ,'Paraná','Rio de Janeiro','Rio Grande do Norte','Rondônia','Roraima','Rio Grande do Sul','Santa Catarina', 'Sergipe', 'São Paulo', 'Tocantins', 'Distrito Federal']
        
    #dados['nomes'] = nomes
    #print(dados)
    
    #print(dados['nomes'])
    #print(dados['sigla'])
    
    fig = px.choropleth(
        dados,
        locations='sigla',
        geojson = brasil,
        color='média idade',
        hover_data=['Nome', 'mediana idade'],
        scope='south america'
    )    
    return fig
    #fig.show()
        
    #fig = px.bar(x=list(vacinas_estado.keys()), y=[vacinas_estado[k]['qtd'] for k in vacinas_estado]) 
    #fig.update_layout(xaxis_title='Estados', yaxis_title='Quantidade de vacinas')
    #fig.show()    
    #fig.write_html("html/mapa.html")



def graficos_valiense(app):
    
    return read_data() 

    components_html = []

    #components_html.append(grafico_total_vacinas_idade(app))
    
    #components_html.append(grafico_sub_plot_vacinas_idade(app))
    components_html.append( read_data() )

    return components_html