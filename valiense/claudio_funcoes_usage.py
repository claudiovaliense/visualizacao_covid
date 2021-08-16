#Author: Claudio Moises Valiense de Andrade. Licence: MIT. Objective: Create general purpose library
import csv  # Manipular csv
from scipy.stats import norm
import collections # quantifica elementos em listas e conjuntos
import scipy.stats as stats # Calcular intervalo de confiança

def remove_key_dict(mydict, keys):
    """Return new dict sem as keys"""
    new_dict = dict()
    for key in mydict:
        if key not in keys:
            new_dict[key] = mydict[key]
    return new_dict

def arquivo_para_corpus(file_corpus, id_column):
    """ Return uma lista que é formada pela coluna do arquivo csv. Example: arquivo_para_corpus(name.csv, 1) """
    corpus = []
    with open(file_corpus, 'r', newline='') as out:
        csv_reader = csv.reader(out, delimiter=',')
        # next(csv_reader)  # Pular cabecalho
        for row in csv_reader:
            corpus.append(row[id_column])
    return corpus

def arquivo_para_corpus_delimiter(file_corpus, delimiter=',', limit_lines=-1):
    """ Returns a 'list' from a csv.  Example: arquivo_para_corpus_delimiter('name.csv', ','); Return=[lines_csv] """
    corpus = []
    with open(file_corpus, 'r', newline='') as out:
        csv_reader = csv.reader(out, delimiter=delimiter)
        # next(csv_reader)  # Pular cabecalho
        cont=0
        for row in csv_reader:
            if cont==limit_lines: 
                break
            corpus.append(row)
            cont+=1
    return corpus

