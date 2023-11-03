from scipy import stats
import numpy as np

def t_student_diferenca_media(amostra, media_populacional_prevista, alpha, bilateral = True):
    try:
        resultado = []
        tamanho_da_amostra = len(amostra)
        # Encontrando o Zcalc
        numerador_zcalc = np.mean(amostra) - media_populacional_prevista
        denominador_zcalc = np.std(amostra, ddof = 1) / np.sqrt(tamanho_da_amostra)
        Zcalc = numerador_zcalc / denominador_zcalc

        # Encontrando o Zcrit
        Zcrit = stats.t.ppf(1 - alpha/2, tamanho_da_amostra - 1) if bilateral else stats.t.ppf(1 - alpha, 
                                                                                            tamanho_da_amostra - 1)
        """stats.t.ppf(1 - alpha/2, tamanho_da_amostra - 1) calcula o valor crítico de uma distribuição t-Student 
        bilateral com (tamanho_da_amostra - 1) graus de liberdade e um nível de significância de alpha/2. Caso seja
        um teste unilateral, basta utilizar (1 - alpha)"""
        
        # Imprimindo os resultados
        lista_aux = []
        lista_aux.append(True)
        lista_aux.append(f"Zcalc = {Zcalc} -------- Zcrit = {Zcrit} ")


        if abs(Zcalc) < abs(Zcrit):
            lista_aux.append(f"|Zcalc| = {abs(Zcalc)} < |Zcrit| = {abs(Zcrit)}")
            lista_aux.append(f"Aceito a hipótese H0 em que a média populacional é = {media_populacional_prevista}")
        else:
            lista_aux.append(f"|Zcalc| = {abs(Zcalc)} > |Zcrit| = {abs(Zcrit)}")
            lista_aux.append(f"Rejeito a hipótese H0 em que a média populacional é = {media_populacional_prevista}")

        resultado.append(lista_aux)
        return resultado

    except Exception as e:
        return [[False, e]]
    

def t_student_comparacao_media_independente(amostra1, amostra2):
    # Calculando a variancia populacional de cada amostra
    variancia_pop_amostra1 = np.var(amostra1, ddof=0)
    variancia_pop_amostra2 = np.var(amostra2, ddof=0)
    # calculando 

def t_student_comparacao_media_emparelhada():
    pass