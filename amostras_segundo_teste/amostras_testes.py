import csv
import numpy as np
import random
import pandas as pd
from scipy import stats

def teste_z(i):
    medias = [3,4,5,6]
    desvios_padrao = [1,1,2,1]
    tamanho_da_amostra = [random.randint(40, 50) for _ in range(4)]
    amostra = list(np.random.normal(loc=medias[i], scale=desvios_padrao[i], size=tamanho_da_amostra[i]))
    return amostra

def teste_t_para_media(i):
    medias = [7,8,2,5]
    desvios_padrao = [1,1,2,1]
    tamanho_da_amostra = [random.randint(15, 25) for _ in range(4)]
    amostra = list(np.random.normal(loc=medias[i], scale=desvios_padrao[i], size=tamanho_da_amostra[i]))
    return amostra

def teste_t_para_comparacao_media(i):
    medias1 = [3,4,5,6]
    desvios_padrao1 = [1,1,2,1]
    tamanho_da_amostra1 = [15,20,25,30]
    amostra1 = list(np.random.normal(loc=medias1[i], scale=desvios_padrao1[i], size=tamanho_da_amostra1[i]))
    medias2 = [3,4,5,60]
    desvios_padrao2 = [1,1,2,5]
    tamanho_da_amostra2 = [15,20,25,30]
    amostra2 = list(np.random.normal(loc=medias2[i], scale=desvios_padrao2[i], size=tamanho_da_amostra2[i]))
    lista = []
    lista.append(amostra1)
    lista.append(amostra2)
    return lista

def teste_t_para_diferenca_media(i):
    lista = []
    medias1 = [3,4,5,6]
    desvios_padrao1 = [1,1,2,1]
    tamanho_da_amostra = [15,20,25,30]
    while len(lista) < 2:
        amostra1 = list(np.random.normal(loc=medias1[i], scale=desvios_padrao1[i], size=tamanho_da_amostra[i]))
        amostra2 = list(np.random.normal(loc=0, scale=1, size=tamanho_da_amostra[i]) + amostra1)
        t_statistic, p_value = stats.ttest_rel(amostra1, amostra2)
        if p_value > 0.05:
            lista.append(amostra1)
            lista.append(amostra2)
        return lista
    
def teste_bartlett(i):
    lista = []
    tamanhos = [20,25,30,35]
    medias1 = [10,20,30,40]
    desvio_padrao1 = [1,1,2,1]
    medias2 = [5,10,15,20]
    desvio_padrao2 = [1,1,2,10]
    amostra1 = list(np.random.normal(loc=medias1[i], scale=desvio_padrao1[i], size=tamanhos[i]))
    amostra2 = list(np.random.normal(loc=medias2[i], scale=desvio_padrao2[i], size=tamanhos[i]))
    lista.append(amostra1)
    lista.append(amostra2)
    return lista

def criar_csv(nome_csv, amostras):
    max = 0
    with open(nome_csv, 'w', newline='') as arquivo_csv:
        escritor_csv = csv.writer(arquivo_csv)
        lista_pivotada = []
        for linha in amostras:
            if len(linha) > max:
                max = len(linha)
        for linha_cod in range(max):
            lista_aux = []
            for linhas in amostras:
                try:
                    lista_aux.append(linhas[linha_cod])
                except:
                    lista_aux.append("")
            lista_pivotada.append(lista_aux)
    pd.DataFrame(lista_pivotada).to_csv(nome_csv, index=False, header=False)

def loop_criacao_amostras():
    for i in range(4):
        criar_csv(f"teste_z{i}.csv", [teste_z(i)])
        criar_csv(f"teste_t_para_media{i}.csv", [teste_t_para_media(i)])
        criar_csv(f"teste_t_para_comparacao_media{i}.csv", teste_t_para_comparacao_media(i))
        criar_csv(f"teste_t_para_diferenca_media{i}.csv", teste_t_para_diferenca_media(i))
        criar_csv(f"teste_bartlett{i}.csv", teste_bartlett(i))

loop_criacao_amostras()
