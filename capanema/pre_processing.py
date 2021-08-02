import numpy as np
import pandas as pd
import plotly as p

from configurations import FILTERED, VACINA
from utils import join
from graphs import bar, stacked_area, overlaid_area

def preprocessar_nome_vacina(l):

    for i in range(len(l)):
        l[i] = l[i].replace("Vacina Covid-19 - ", "").replace("Covid-19-", "").replace("Vacina covid-19 - ", "").replace("BNT162b2 - ", "").replace("Covishield", "AstraZeneca").replace("Pendente Identificação", "Vacina sem identificação").replace("Vacina covid-19 - Ad26.COV2.S - Janssen-Cilag", "Janssen").replace("BioNTech/Fosun Pharma/Pfizer", "Pfizer").replace("Coronavac-Sinovac/Butantan", "Coronavac").replace("Ad26.COV2.S - Janssen-Cilag", "Janssen")

    return np.array(l)

def preprocessar_nome_vacina_descricao(l):

    n_l = []
    for i in range(len(l)):
        e = l[i].replace("\xa0\xa0\xa0\xa01ª\xa0Dose", "Primeira dose").replace("\xa0\xa0\xa0\xa02ª\xa0Dose", "Vacinação completa").replace("\xa0\xa0\xa0\xa03ª\xa0Dose", "Vacinação completa").replace("Única", "Vacinação completa").replace("\xa0\xa0\xa0\xa0Dose\xa0Inicial\xa0", "Primeira dose").replace("Vacinação completa\xa0Revacinação\xa0", "Vacinação completa").replace("\xa0\xa0\xa0\xa0Vacinação completa\xa0", "Vacinação completa").replace("\xa0\xa0\xa0\xa0Dose\xa0", "Vacinação completa")
        n_l.append(e)

    return np.array(n_l)

def grafico_total_vacinas_tipo_dose(df):
    semana_aplicacao_dose = df.groupby(by=['Semana de aplicação', 'Dose']).apply(
        lambda e: pd.DataFrame({'Total (semana)': [len(e)]})).reset_index()[
        ['Semana de aplicação', 'Dose', 'Total (semana)']]
    overlaid_area(semana_aplicacao_dose, x_column='Semana de aplicação', y_column='Total (semana)',
                  filename='total_dose_semana.html', category='Dose')

if __name__ == "__main__":

    file = "vacina_preprocessado.csv"
    n = 0
    vacina = pd.read_csv(VACINA, delimiter=';', encoding='UTF-8')
    print(vacina)
    minima = None
    for dados in pd.read_csv(FILTERED, delimiter=';', chunksize=1000000, encoding="UTF-8"):
        df = dados[['vacina_dataaplicacao', 'vacina_codigo', 'vacina_descricao_dose', 'paciente_endereco_uf']]
        df = df.join(vacina.set_index('vacina_codigo'), on='vacina_codigo')
        df['Nome da vacina'] = preprocessar_nome_vacina(df['vacina_nome'].tolist())

        df['vacina_dataaplicacao'] = pd.to_datetime(df['vacina_dataaplicacao'], infer_datetime_format=True)
        df['vacina_dataaplicacao'] = df[df['vacina_dataaplicacao'] >= pd.Timestamp(year=2020, month=1, day=1)]
        df['vacina_descricao_dose'] = preprocessar_nome_vacina_descricao(df['vacina_descricao_dose'].tolist())
        df['Dose'] = df['vacina_descricao_dose']
        df['Semana de aplicação'] = df['vacina_dataaplicacao'].dt.weekofyear
        df['Estado'] = df['paciente_endereco_uf']
        df = df[['Dose', 'Semana de aplicação', 'Nome da vacina', 'Estado']]
        print(df)

        if n == 0:
            df.to_csv(file)
        else:
            df.to_csv(file, header=False, mode='a')
        n += 1

        # if n == 2:
        #     break

