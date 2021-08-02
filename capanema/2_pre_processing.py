import numpy as np
import pandas as pd
import plotly as p

from configurations import FILTERED, VACINA
from utils import join
from graphs import bar, stacked_area, overlaid_area

def grafico_areas_empilhadas(df):
    semana_aplicaca_por_vacina = \
        df.groupby(by=['Semana de aplicação', 'Nome da vacina', 'Estado']).apply(
            lambda e: pd.DataFrame({'Total (semana)': [len(e)]})).reset_index()

    #print("original", semana_aplicaca_por_vacina)
    semana_aplicaca_por_vacina = semana_aplicaca_por_vacina[
            ['Estado', 'Semana de aplicação', 'Total (semana)', 'Nome da vacina']]

    semana_aplicaca_por_vacina.to_csv("areas_empilhadas.csv", index=False)

def grafico_total_vacinas_tipo_dose(df):
    # df = pd.concat([df, pd.DataFrame(
    #     {'Semana de aplicação': [i for i in range(30)], 'Dose': ['Vacinação completa'] * 30})], sort=True,
    #                ignore_index=True)
    # df = pd.concat([df, pd.DataFrame(
    #     {'Semana de aplicação': [i for i in range(30)], 'Dose': ['Primeira dose'] * 30})], sort=True,
    #                ignore_index=True)
    semana_aplicacao_dose = df.groupby(by=['Estado', 'Semana de aplicação', 'Dose']).apply(
        lambda e: pd.DataFrame({'Total (semana)': [len(e)]})).reset_index()[
        ['Estado', 'Semana de aplicação', 'Dose', 'Total (semana)']]

    semana_aplicacao_dose.to_csv("total_dose.csv", index=False)

if __name__ == "__main__":

    file = "vacina_preprocessado.csv"
    saida = "vacina_preprocessado_2.csv"
    n = 0
    # ['Dose', 'Semana de aplicação', 'Nome da vacina', 'Estado]
    df = pd.read_csv(file, encoding='UTF-8')

    #grafico_areas_empilhadas(df)

    grafico_total_vacinas_tipo_dose(df)
