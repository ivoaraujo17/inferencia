import numpy as np
from scipy import stats
import pandas as pd

def teste_bartlett(caminho_do_arquivo, alfa):
    try:
        amostras = []
        df = pd.read_csv(caminho_do_arquivo)
        for i in range(len(df.columns)):
            lista_de_valores = df.iloc[:, i]
            lista_de_valores = lista_de_valores.dropna()
            amostras.append(lista_de_valores)
        resultado = []
        k = len(amostras)
        # Encontrando a soma de todas as amostras
        N = np.sum([len(amostra) for amostra in amostras])
        # Encontrando o valor de Sp
        soma_numerador = 0
        soma_denominador = 0
        for amostra in amostras:
            numerador_de_cada_amostra = (len(amostra) - 1) * np.var(amostra, ddof = 1)
            soma_numerador += numerador_de_cada_amostra
            denominador_de_cada_amostra = len(amostra) - 1
            soma_denominador += denominador_de_cada_amostra
        Sp = soma_numerador / soma_denominador
        # O valor da soma (ni - 1) é o mesmo do denomianador de cada amostra
        soma_ni = soma_denominador
        # Encontrando o valor de q
        q = soma_ni * np.log(Sp) - np.sum([(len(amostra) - 1) * np.log(np.var(amostra, ddof = 1)) for amostra in amostras])
        # Encontrando o valor de c (x²)
        X = 1 + (1 / (3 * (k - 1))) * np.sum([1 / (len(amostra) - 1) - 1/(N - k) for amostra in amostras])
        # Encontrando o Bcalc
        Bcalc = q/X
        # Encontrando o Bcrit
        Bcrit = stats.chi2.ppf(1 - alfa, k - 1) # Valor da estatística crítica com k-1 graus de liberdade

        lista_aux = []
        lista_aux.append(True)
        lista_aux.append(f"Bcalc = {Bcalc} -------- Bcrit = {Bcrit} ")

        if Bcalc < Bcrit:
            lista_aux.append(f"Bcalc = {Bcalc} < Bcrit = {Bcrit}")
            lista_aux.append(f"Aceito a hipótese H0 em que as variâncias populacionais são homogêneas")
        else:
            lista_aux.append(f"Bcalc = {Bcalc} > Bcrit = {Bcrit}")
            lista_aux.append(f"Rejeito a hipótese H0 em que as variâncias populacionais são homogêneas")
        
        resultado.append(lista_aux)
        return resultado

    except Exception as e:
        return [[False, e]]



