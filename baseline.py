#Author: Claudio Moises Valiense de Andrade. Licence: MIT. Objective: Visualizar dados do covid
import claudio_funcoes_usage as cv
import matplotlib.pyplot as plt
import plotly.express as px

def read_data():
    """Read data"""
    #filtered.csv': paciente_datanascimento;paciente_enumsexobiologico;paciente_racacor_codigo;paciente_endereco_uf;vacina_grupoatendimento_codigo;vacina_dataaplicacao;vacina_descricao_dose;vacina_codigo
    dados = cv.arquivo_para_corpus_delimiter(f'dataset/vacinaOpenDataSUS/filtered.csv', ';', 1000) # arquivo com os dados     
    grupo_categoria = cv.arquivo_para_corpus_delimiter(f'dataset/vacinaOpenDataSUS/grupo-categoria.csv', ';') # 4 vacina_grupoatendimento_codigo[ vacina_grupoatendimento_codigo;vacina_grupoatendimento_nome;vacina_categoria_nome ]
    #grupo = cv.arquivo_para_corpus_delimiter(f'dataset/vacinaOpenDataSUS/grupo.csv', ';')
    raca = cv.arquivo_para_corpus_delimiter(f'dataset/vacinaOpenDataSUS/raca.csv', ';') # paciente_racacor_codigo, 2
    tipos_vacina = cv.arquivo_para_corpus_delimiter(f'dataset/vacinaOpenDataSUS/vacina.csv', ';') # vacina_codigo 7
    
    vacinas_estado = dict()
    for index in range(len(dados)):
        if vacinas_estado.get( dados[index][3] ) == None: 
            vacinas_estado[ dados[index][3] ] = 0
        vacinas_estado[ dados[index][3] ]+=1  # estado    
    vacinas_estado = cv.remove_key_dict(vacinas_estado, 'XX'); vacinas_estado = cv.remove_key_dict(vacinas_estado, 'paciente_endereco_uf')    
    
    fig = px.bar(x=vacinas_estado.keys(), y=vacinas_estado.values())    
    fig.update_layout(xaxis_title='Estados', yaxis_title='Quantidade de vacinas')
    fig.show()    
    fig.write_html("html/vacina_estado.html")


if __name__ == "__main__":
    read_data()

# backup
''' # estatico
plt.bar(vacinas_estado.keys(), vacinas_estado.values())
plt.xlabel('Estados')
plt.ylabel('Quantidade de vacinas')
plt.show()'''