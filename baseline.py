#Author: Claudio Moises Valiense de Andrade. Licence: MIT. Objective: Visualizar dados do covid
import claudio_funcoes_usage as cv # function usage geral
import matplotlib.pyplot as plt # plot static
import plotly.express as px # plot dynamic
import datetime # time
import statistics # function statistics

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
        vacinas_estado[k]['age'] = statistics.mean( vacinas_estado[k]['age'] )
        
    
    #''' # vacina idade
    fig = px.bar(x=vacinas_estado.keys(), y=[vacinas_estado[k]['age'] for k in vacinas_estado])    
    fig.update_layout(xaxis_title='Estados', yaxis_title='Média da idade dos vacinados')
    fig.show()    
    fig.write_html("html/vacina_idade_estado.html")
    #'''
    
    ''' # vacina estado
    fig = px.bar(x=vacinas_estado.keys(), y=vacinas_estado.values())    
    fig.update_layout(xaxis_title='Estados', yaxis_title='Quantidade de vacinas')
    fig.show()    
    fig.write_html("html/vacina_estado.html")
    '''
    
    print( datetime.datetime.today() )
    



if __name__ == "__main__":
    read_data()

# backup
''' # estatico
plt.bar(vacinas_estado.keys(), vacinas_estado.values())
plt.xlabel('Estados')
plt.ylabel('Quantidade de vacinas')
plt.show()'''