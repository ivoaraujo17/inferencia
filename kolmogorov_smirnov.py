import numpy as np
import pandas as pd
from scipy.stats import norm, ksone

def kolmogorov_smirnov(caminho_do_arquivo, alpha):
    try:
        resultado = []
        # Lendo o arquivo csv
        df = pd.read_csv(caminho_do_arquivo)
        for i in range(len(df.columns)):
            lista_de_valores = df.iloc[:, i]
            lista_de_valores = lista_de_valores.dropna()
            # Obtendo a média amostral
            media_amostral = np.mean(lista_de_valores)
            # Obtendo o desvio padrão amostral
            desvio_padrao_amostral = np.std(lista_de_valores, ddof=1)
            # Ordenando a lista de valores sem valores repetidos
            lista_ordenada = sorted(lista_de_valores)
            Xi = sorted(set(lista_ordenada))
            # Calculando a frequência absoluta de cada valor
            freq_abs = [lista_ordenada.count(i) for i in Xi]
            # Calculando a frequência acumulada
            freq_acum = []
            for i in range(len(freq_abs)):
                if i == 0:
                    freq_acum.append(freq_abs[i])
                else:
                    freq_acum.append(freq_acum[i-1] + freq_abs[i])
            # Calculando a frequência relativa acumulada
            freq_rel_acum = []
            for i in range(len(freq_abs)):
                    freq_rel_acum.append(freq_acum[i]/freq_acum[-1])
            # Calculandos os valores de Zi
            Zi = [(x - media_amostral) / desvio_padrao_amostral for x in Xi]
            # Calculando a frequência esperada Fesp (valor de Z na tabela de distribuição normal N(0,1))
            freq_esperada = [norm.cdf(z) for z in Zi] #Funçao de distribuição acumulada da normal
            # Calculando a |Fesp(Xi) - Frac(Xi)| para cada valor de Xi
            Fesp_menos_Frac = [abs(freq_esperada[i] - freq_rel_acum[i]) for i in range(len(Xi))]
            # Calculando a |Fesp(Xi) - Frac(Xi-1)| para cada valor de Xi
            # Como o for não pode começar em 0, então a primeira posição é calculada fora do for
            Fesp_menos_Frac_1 = [freq_esperada[0]] + [abs(freq_esperada[i] - freq_rel_acum[i-1]) for i in range(1, len(Xi))]
            #Calculando o Dcalc
            max_Fesp_menos_Frac = max(Fesp_menos_Frac)
            max_Fesp_menos_Frac_1 = max(Fesp_menos_Frac_1)
            Dcalc = max(max_Fesp_menos_Frac, max_Fesp_menos_Frac_1)

            #Calculando o Dtabelado (D crítico)
            if len(lista_ordenada) > 0 and len(lista_ordenada) <= 35:
                Dtab = ksone.ppf(1 - alpha/2, len(lista_ordenada)) #Calcula o Dcrit de um teste KS
            
            elif len(lista_ordenada) > 35:
                if alpha == 0.2:
                    Dtab = 1.07 / np.sqrt(len(lista_ordenada))
                elif alpha == 0.15:
                    Dtab = 1.14 / np.sqrt(len(lista_ordenada))
                elif alpha == 0.10:
                    Dtab = 1.22 / np.sqrt(len(lista_ordenada))
                elif alpha == 0.05:
                    Dtab = 1.36 / np.sqrt(len(lista_ordenada))
                elif alpha == 0.01:
                    Dtab = 1.63 / np.sqrt(len(lista_ordenada))
            
            lista_aux = []
            lista_aux.append(True)
            if Dcalc < Dtab:
                lista_aux.append("Dcalc = %.4f < Dtab = %.4f" % (Dcalc, Dtab))
                lista_aux.append("Aceito a hipótese H0 que a amostra segue uma distribuição normal.")
            else:
                lista_aux.append("Dcalc = %.4f > Dtab = %.4f" % (Dcalc, Dtab))
                lista_aux.append("Rejeito a hipótese H0 que a amostra segue uma distribuição normal")
                
            resultado.append(lista_aux)

            
            # Criando um dataframe no pandas com todas as colunas das frequencias

            #df = pd.DataFrame({'Xi': Xi, 'FreqAbs': freq_abs, 'FreqAcum': freq_acum, 'FreqRelAcum': freq_rel_acum, 'Zi': Zi, 'Fesp': freq_esperada, '|Fesp - Frac|': Fesp_menos_Frac, '|Fesp - Frac-1|': Fesp_menos_Frac_1})
            #return df
        return resultado
    except Exception as e:
        return [False, e]
    

def kolmogorov_smirnov_(caminho_do_arquivo, alpha):
    try:
        resultado = []
        # Lendo o arquivo csv
        df = pd.read_csv(caminho_do_arquivo)
        # Obtendo a coluna de valores
        for i in range(len(df.columns)):
            lista_de_valores = df.iloc[:, i].values
            # Ordenando a lista de valores sem valores repetidos
            lista_ordenada = sorted(lista_de_valores)
            #Obtendo a amplitude total e a amplitude de cada classe
            k = len(lista_ordenada) // 3 # quantidade de classes
            amplitude_total = max(lista_ordenada) - min(lista_ordenada)
            amplitude_classe = amplitude_total /k
            # Obtendo os limites de cada classe
            limites_classes = [min(lista_ordenada) + i*amplitude_classe for i in range(k + 1)]
            # Colocando os limites de classe na coluna Xi
            Xi = [limites_classes[i] for i in range(k)]
            # Calculando a média dos intervalos
            media_amostral = np.mean(Xi)
            # Calculando o desvio padrao dos intervalos
            desvio_padrao_amostral = np.std(Xi, ddof=1)
            # Calculando a frequência absoluta de cada classe
            freq_abs = []
            for i in range(k):
                freq_abs.append(len([x for x in lista_ordenada if x >= limites_classes[i] and x < limites_classes[i+1]]))

            # Calculando a frequência acumulada
            freq_acum = []
            for i in range(len(freq_abs)):
                if i == 0:
                    freq_acum.append(freq_abs[i])
                else:
                    freq_acum.append(freq_acum[i-1] + freq_abs[i])
            # Calculando a frequência relativa acumulada
            freq_rel_acum = []
            for i in range(len(freq_abs)):
                    freq_rel_acum.append(freq_acum[i]/freq_acum[-1])
            # Calculandos os valores de Zi
            Zi = [(x - media_amostral) / desvio_padrao_amostral for x in Xi]
            # Calculando a frequência esperada Fesp (valor de Z na tabela de distribuição normal N(0,1))
            freq_esperada = [norm.cdf(z) for z in Zi] #Funçao de distribuição acumulada da normal
            # Calculando a |Fesp(Xi) - Frac(Xi)| para cada valor de Xi
            Fesp_menos_Frac = [abs(freq_esperada[i] - freq_rel_acum[i]) for i in range(len(Xi))]
            # Calculando a |Fesp(Xi) - Frac(Xi-1)| para cada valor de Xi
            # Como o for não pode começar em 0, então a primeira posição é calculada fora do for
            Fesp_menos_Frac_1 = [freq_esperada[0]] + [abs(freq_esperada[i] - freq_rel_acum[i-1]) for i in range(1, len(Xi))]
            #Calculando o Dcalc
            max_Fesp_menos_Frac = max(Fesp_menos_Frac)
            max_Fesp_menos_Frac_1 = max(Fesp_menos_Frac_1)
            Dcalc = max(max_Fesp_menos_Frac, max_Fesp_menos_Frac_1)

            #Calculando o Dtabelado (D crítico)
            if len(lista_ordenada) > 0 and len(lista_ordenada) <= 35:
                Dtab = ksone.ppf(1 - alpha/2, len(lista_ordenada)) #Calcula o Dcrit de um teste KS
            
            elif len(lista_ordenada) > 35:
                if alpha == 0.2:
                    Dtab = 1.07 / np.sqrt(len(lista_ordenada))
                elif alpha == 0.15:
                    Dtab = 1.14 / np.sqrt(len(lista_ordenada))
                elif alpha == 0.10:
                    Dtab = 1.22 / np.sqrt(len(lista_ordenada))
                elif alpha == 0.05:
                    Dtab = 1.36 / np.sqrt(len(lista_ordenada))
                elif alpha == 0.01:
                    Dtab = 1.63 / np.sqrt(len(lista_ordenada))
            
            lista_aux = []
            lista_aux.append(True)
            if Dcalc < Dtab:
                lista_aux.append("Dcalc = %.4f < Dtab = %.4f" % (Dcalc, Dtab))
                lista_aux.append("Aceito a hipótese H0 que a amostra segue uma distribuição normal.")
            else:
                lista_aux.append("Dcalc = %.4f > Dtab = %.4f" % (Dcalc, Dtab))
                lista_aux.append("Rejeito a hipótese H0 que a amostra segue uma distribuição normal")

            resultado.append(lista_aux)

            
            # Criando um dataframe no pandas com todas as colunas das frequencias

            #df = pd.DataFrame({'Xi': Xi, 'FreqAbs': freq_abs, 'FreqAcum': freq_acum, 'FreqRelAcum': freq_rel_acum, 'Zi': Zi, 'Fesp': freq_esperada, '|Fesp - Frac|': Fesp_menos_Frac, '|Fesp - Frac-1|': Fesp_menos_Frac_1})
            #return df
        return resultado
    except Exception as e:
        return [False, e]
        