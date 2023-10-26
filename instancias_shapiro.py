import numpy as np
import random

def amostra_normal():
    # Especifique as médias e desvios padrão para cada amostra
    medias = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105]
    desvios_padrao = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
    tamanho_da_amostra = [random.randint(5, 20) for _ in range(20)]
    amostras_normais = []

    # Gere 20 amostras de tamanhos diferentes com médias e desvios padrão diferentes
    for tamanho_amostra, media, desvio in zip(tamanho_da_amostra, medias, desvios_padrao):
        amostra = np.random.normal(loc=media, scale=desvio, size=tamanho_amostra)
        amostras_normais.append(amostra)
        
    return amostras_normais


def amostra_gamma():
    parametros = [(2, 1.5), (2, 1), (2, 2), (1, 1.5), (1.5, 1.5), (3, 2), (3, 1), (1, 1), 
                  (2, 3), (4, 2)]
    tamanhos_amostra = [30 for _ in range(10)]
    amostras_gamma = []

    for (a, b), tamanho in zip(parametros, tamanhos_amostra):
        amostra = np.random.gamma(shape=a, scale=b, size=tamanho)
        amostras_gamma.append(amostra)
    
    return amostras_gamma


def amostra_quiquadrada():
    graus_de_liberdade = [random.randint(1, 3) for _ in range(10)]
    tamanhos_amostra = [25 for _ in range(10)]
    amostras_quiquad = []

    for grau, tamanho in zip(graus_de_liberdade, tamanhos_amostra):
        amostra = np.random.chisquare(df=grau, size=tamanho)
        amostras_quiquad.append(amostra)

    return amostras_quiquad

