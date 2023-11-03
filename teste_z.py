from scipy import stats
import numpy as np

def teste_z(amostra,media_populacional_prevista, alpha, desvio_padrao = 0, bilateral = True):
    try:
        resultado = []
        # Encontrando o Zcalc
        numerador_zcalc = np.mean(amostra) - media_populacional_prevista
        if desvio_padrao == 0:
            desvio_padrao = np.std(amostra, ddof = 1) # Se eu nao sei o desvio padrao da populacao, uso o da amostra
        denominador_zcalc = desvio_padrao / np.sqrt(len(amostra)) # Uso o desvio padrao da populacao informado na funçao
        Zcalc = numerador_zcalc / denominador_zcalc

        # Encontrando o Zcrit
        Zcrit = stats.norm.ppf(1 - alpha/2) if bilateral else stats.norm.ppf(1 - alpha)
        """stats.norm.ppf(1 - alfa/2) calcula o valor crítico Z para um teste bicaudal (bilateral) com um nível de 
        significância de alpha/2 em cada cauda da distribuição normal padrão. Para um teste unicaudal (unilateral),
        basta utilizar (1 - alpha)"""

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