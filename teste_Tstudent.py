from scipy import stats
import numpy as np

def t_student_media(amostra, media_populacional_prevista, alpha, bilateral = True):
    try:
        resultado = []
        tamanho_da_amostra = len(amostra)
        # Encontrando o Zcalc
        numerador_tcalc = np.mean(amostra) - media_populacional_prevista
        denominador_tcalc = np.std(amostra, ddof = 1) / np.sqrt(tamanho_da_amostra)
        Tcalc = numerador_tcalc / denominador_tcalc

        # Encontrando o Zcrit
        Tcrit = stats.t.ppf(1 - alpha/2, tamanho_da_amostra - 1) if bilateral else stats.t.ppf(1 - alpha, 
                                                                                            tamanho_da_amostra - 1)
        """stats.t.ppf(1 - alpha/2, tamanho_da_amostra - 1) calcula o valor crítico de uma distribuição t-Student 
        bilateral com (tamanho_da_amostra - 1) graus de liberdade e um nível de significância de alpha/2. Caso seja
        um teste unilateral, basta utilizar (1 - alpha)"""
        
        # Imprimindo os resultados
        lista_aux = []
        lista_aux.append(True)
        lista_aux.append(f"Tcalc = {Tcalc} -------- Tcrit = {Tcrit} ")


        if abs(Tcalc) < abs(Tcrit):
            lista_aux.append(f"|Tcalc| = {abs(Tcalc)} < |Tcrit| = {abs(Tcrit)}")
            lista_aux.append(f"Aceito a hipótese H0 em que a média populacional é = {media_populacional_prevista}")
        else:
            lista_aux.append(f"|Tcalc| = {abs(Tcalc)} > |Tcrit| = {abs(Tcrit)}")
            lista_aux.append(f"Rejeito a hipótese H0 em que a média populacional é = {media_populacional_prevista}")

        resultado.append(lista_aux)
        return resultado

    except Exception as e:
        return [[False, e]]
    

def t_student_comparacao_media_independente(amostra1, amostra2, alfa, bilateral = True):
    try:
        resultado = []
        # Calculando a variancia amostral de cada amostra
        variancia_amostral1 = np.var(amostra1, ddof=1)
        variancia_amostral2 = np.var(amostra2, ddof=1)
        # calculando a média amostral de cada amostra
        media_amostra1 = np.mean(amostra1)
        media_amostra2 = np.mean(amostra2)
        # calculando o tamanho de cada amostra
        n1 = len(amostra1)
        n2 = len(amostra2)
        # calculando o Sp
        numerador_sp = (n1 - 1) * variancia_amostral1 + (n2 - 1) * variancia_amostral2
        denominador_sp = n1 + n2 - 2
        Sp = np.sqrt(numerador_sp / denominador_sp)
        #Calculando o Tcalc
        numerador_tcalc = media_amostra1 - media_amostra2
        denominador_tcalc = Sp * np.sqrt(1/n1 + 1/n2)
        Tcalc = numerador_tcalc / denominador_tcalc
        # Calculando o Tcrit
        Tcrit = stats.t.ppf(1 - alfa/2, n1 + n2 - 2) if bilateral else stats.t.ppf(1 - alfa, n1 + n2 - 2)
        """stats.t.ppf(1 - alfa/2, n1 + n2 - 2) calcula o valor crítico de uma distribuição t-Student bilateral com
        (n1 + n2 - 2) graus de liberdade e um nível de significância de alpha/2. Caso seja um teste unilateral, basta
        utilizar (1 - alpha)"""

        lista_aux = []
        lista_aux.append(True)
        lista_aux.append(f"Tcalc = {Tcalc} -------- Tcrit = {Tcrit} ")


        if abs(Tcalc) < abs(Tcrit):
            lista_aux.append(f"|Tcalc| = {abs(Tcalc)} < |Tcrit| = {abs(Tcrit)}")
            lista_aux.append(f"Aceito a hipótese H0 em que as médias populacionais são iguais")
        else:
            lista_aux.append(f"|Tcalc| = {abs(Tcalc)} > |Tcrit| = {abs(Tcrit)}")
            lista_aux.append(f"Rejeito a hipótese H0 em que as médias populacionais são iguais")

        resultado.append(lista_aux)
        return resultado

    except Exception as e:
        return [[False, e]]
    
def t_student_diferenca_media_emparelhada(amostra1, amostra2, alfa, bilateral = True):
    try:
        resultado = []
        n = len(amostra1)
        # Encontrando a soma das diferenças das amostras
        soma_diferencas = np.sum(np.array(amostra1) - np.array(amostra2)) #Transformando em array do np para fazer a diferença
        # Encontrando a média das diferenças das amostras
        media_diferencas = soma_diferencas / n
        # Encontrando o desvio padrão amostral das diferenças das amostras
        desvio_padrao_diferencas = np.std(np.array(amostra1) - np.array(amostra2), ddof = 1)
        # Encontrando o Tcalc
        Tcalc = media_diferencas / (desvio_padrao_diferencas / np.sqrt(n))
        # Encontrando o Tcrit
        Tcrit = stats.t.ppf(1 - alfa/2, n - 1) if bilateral else stats.t.ppf(1 - alfa, n - 1)

        lista_aux = []
        lista_aux.append(True)
        lista_aux.append(f"Tcalc = {Tcalc} -------- Tcrit = {Tcrit} ")


        if abs(Tcalc) < abs(Tcrit):
            lista_aux.append(f"|Tcalc| = {abs(Tcalc)} < |Tcrit| = {abs(Tcrit)}")
            lista_aux.append(f"Aceito a hipótese H0 em que as médias populacionais são iguais")
        else:
            lista_aux.append(f"|Tcalc| = {abs(Tcalc)} > |Tcrit| = {abs(Tcrit)}")
            lista_aux.append(f"Rejeito a hipótese H0 em que as médias populacionais são iguais")

        resultado.append(lista_aux)
        return resultado
    
    except Exception as e:
        return [[False, e]]