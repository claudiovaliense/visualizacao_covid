# -*- coding: utf-8 -*-
"""
Created on Sun Jul 11 20:13:09 2021

@author: FredChaves
"""
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

estado = str(input("Insira sigla do estado, em letras minúsculas: ")).lower()
nome_do_arquivo = "dados-" + estado + ".csv"
dados = pd.read_csv(nome_do_arquivo, delimiter=";", encoding = "ISO-8859-1")

# Passo 1 - Eliminar colunas sem dados de interesse
dados = dados[['estado', 'municipio', 'idade', 'sexo', 'cbo','profissionalSaude','condicoes','sintomas','dataInicioSintomas', 'dataNotificacao','dataTeste','tipoTeste','estadoTeste','resultadoTeste', 'evolucaoCaso', 'dataEncerramento']]

# Passo 2 - Converter as datas para formato correto
dados["dataInicioSintomas"] = pd.to_datetime(dados["dataInicioSintomas"]).dt.date
dados["dataNotificacao"] = pd.to_datetime(dados["dataNotificacao"]).dt.date
dados["dataTeste"] = pd.to_datetime(dados["dataTeste"]).dt.date
dados["dataEncerramento"] = pd.to_datetime(dados["dataEncerramento"]).dt.date

# Passo 3 - Eliminar linhas na qual a idade não é informada ou é um valor absurdo e transformá-la em numérica
dados = dados[dados.idade != np.nan]
dados["idade"] = pd.to_numeric(dados["idade"])
dados = dados[dados.idade <110]

# Passo 4 - Criar e popular coluna faixa etária
fe = {10:"0-10", 20:"11-20", 30:"21-30", 40:"31-40", 50:"41-50", 60:"51-60", 70:"61-70", 80:"71-80", 500: "80+"}
faixaEtaria = []
for idade in dados["idade"]:
    for i in fe.keys():
        if idade <= i:
            faixaEtaria.append(fe[i])
            break
dados["faixaEtaria"] = faixaEtaria

# Passo 5 - Condensar dados por idade, faixa etária e sexo
idades = []
masculino_i = []
feminino_i = []
for i in range(110):
    idades.append(i)
    masculino_i.append(-len(dados.loc[((dados["sexo"]=="Masculino") & (dados["idade"]==i) & (dados["resultadoTeste"]=="Positivo"))]))
    feminino_i.append(len(dados.loc[((dados["sexo"]=="Feminino") & (dados["idade"]==i) & (dados["resultadoTeste"]=="Positivo"))]))
        
faixas = []
masculino_f = []
feminino_f = []
for f in fe.values():
    faixas.append(f) 
    masculino_f.append(-len(dados.loc[((dados["sexo"]=="Masculino") & (dados["faixaEtaria"]==f) & (dados["resultadoTeste"]=="Positivo"))]))
    feminino_f.append(len(dados.loc[((dados["sexo"]=="Feminino") & (dados["faixaEtaria"]==f) & (dados["resultadoTeste"]=="Positivo"))]))

# Passo 6 - Salvar gráficos de casos  
piramide_casos_i = pd.DataFrame({"idade":idades, "Masculino":masculino_i, "Feminino":feminino_i})
fig1, ax1 = plt.subplots(figsize = (10,15))
yticks = [0, 10,20,30,40,50,60,70,80,90,100, 110]
yticklabels = reversed(["0","10","20","30","40","50","60","70","80","90","100", "110"])
xticks = [-750, -500, -250, 0, 250, 500, 750]
xticklabels = ["750", "500","250","0","250","500","750"]
ordem = list(reversed(range(110)))
bar_plot = sns.barplot(x='Masculino', y='idade', data=piramide_casos_i, orient="horizontal", order = ordem, color = "dodgerblue", label = "Homens", linewidth = 0)
bar_plot = sns.barplot(x='Feminino', y='idade', data=piramide_casos_i, orient="horizontal", order = ordem, color = "lightpink", label = "Mulheres", linewidth = 0)
bar_plot.set(xlabel="Casos confirmados", ylabel="Idade", title = "Casos no dados até 07/07/2021", yticks = yticks, yticklabels= yticklabels, xticks = xticks, xticklabels = xticklabels)
bar_plot.legend()
fig1.savefig("Casos_idade_" + estado + ".png")

piramide_casos_f = pd.DataFrame({"faixa":reversed(faixas), "Masculino":reversed(masculino_f), "Feminino":reversed(feminino_f)})
fig2, ax2 = plt.subplots(figsize = (10,15))
xticks = [-7500, -5000, -2500, 0, 2500, 5000, 7500]
xticklabels = ["7500", "5000","2500","0","2500","5000","7500"]
bar_plot = sns.barplot(ax = ax2, x='Masculino', y='faixa', data=piramide_casos_f, orient="horizontal", color = "dodgerblue", label = "Homens", linewidth = 0)
bar_plot = sns.barplot(ax = ax2, x='Feminino', y='faixa', data=piramide_casos_f, orient="horizontal", color = "lightpink", label = "Mulheres", linewidth = 0)
bar_plot.set(xlabel="Casos confirmados", ylabel="Faixa etária", title = "Casos no dados até 07/07/2021", xticks = xticks, xticklabels = xticklabels)
bar_plot.legend()
fig2.savefig("Casos_faixa_" + estado + ".png")