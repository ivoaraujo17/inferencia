import numpy as np
import pandas as pd

#Lendo e processando as tabelas de coeficientes
coeficientes_Ain = pd.read_csv('Coeficiente_Ain_Shapiro.csv', sep=';', decimal=',')
tabela_Wcrit = pd.read_csv('tabela_Wcrit_Shapiro.csv', sep=';', decimal=',')
tabela_Wcrit = tabela_Wcrit.drop(['Unnamed: 10'], axis=1)
tabela_Wcrit = tabela_Wcrit.drop(28)
tabela_Wcrit["tamanho n"] = tabela_Wcrit["tamanho n"].astype(int)

def shapiro_wilk(caminho_do_arquivo, alpha, Tabela_Wcrit = tabela_Wcrit, tabela_de_coeficientes_Ain = coeficientes_Ain):
    try:
        resultado = []
        # Lendo o arquivo csv
        df = pd.read_csv(caminho_do_arquivo)
        for i in range(len(df.columns)):
            lista_de_valores = df.iloc[:, i]
            lista_de_valores = lista_de_valores.dropna()
            lista_de_valores = sorted(lista_de_valores)
            # Encontrando o valor de n (tamanho da amostra)
            n = len(lista_de_valores)
            if n > 30 or n < 3:
                return 'Erro: Amostra maior que 30 ou menor que 3.'
            # Encontrando o valor de i
            i_ = [i for i in range(1, (n//2) + 1)]
            # Encontrando o valor de n - (i - 1)
            n_menos_i_menos_1 = []
            for i in i_:
                n_menos_i_menos_1.append(n - (i -1))
            # Encontrando o valor de Ai,n
            Ain = []
            for i in range(1, (n//2) + 1):
                Ain.append(tabela_de_coeficientes_Ain.loc[(i-1, str(n))])
            """Primeiro índice é a linha, o segundo é a coluna. Se i = 1 e n = 24 então na tabela será o valor
            A1,24. (i = 1 corresponde a linha 0)"""

            # Encontrando o valor de X(n-(i-1)) na lista de valores
            X_n_menos_i_menos_1 = []
            for i in range(1, (n//2) + 1):
                X_n_menos_i_menos_1.append(lista_de_valores[n - (i - 1) - 1]) 
            """-1 pois o índice começa em 0, não existe o 24"""


            # Encontrando o valor de Xi na lista de valores
            Xi = []
            for i in i_:
                Xi.append(lista_de_valores[i - 1])

            # Encontrando o valor de Ai,n vezes (X(n-(i-1)) - Xi))))
            
            valores_Bi = []
            soma_Bi = 0
            for i in range(1, (n//2) + 1):
                valores_Bi.append(Ain[i-1] * (X_n_menos_i_menos_1[i-1] - Xi[i-1]))
                soma_Bi += valores_Bi[i-1]
            
            # Encontrando o valor amostral dos desvios absolutos ao quadrado (ou a variância vezes n-1)
            denominador_do_Wcalc = np.var(lista_de_valores, ddof=1) * (n - 1) #ddof=1 para usar a variância amostral
            # Encontrando o valor do Wcalculado
            Wcalc = (soma_Bi**2) / denominador_do_Wcalc
            # Encontrando o valor do Wtabelado (Wcritico)
            Wcrit = Tabela_Wcrit.loc[(n-3, str(alpha))] 
            """"n-3 pois estou pegando pelo índice criado pelo dataframe, que começa em 0. Uma amostra de tamanho
            3 corresponde ao índice 0, uma de tamanho 4 corresponde ao índice 1, e assim por diante."""
            
            lista_aux = []
            if Wcrit < Wcalc:
                lista_aux.append("Wcrit = %.4f < Wcalc = %.4f" % (Wcrit, Wcalc))
                lista_aux.append("Aceito a hipótese H0 que a amostra segue uma distribuição normal.")
            else:
                lista_aux.append("Wcrit = %.4f > Wcalc = %.4f" % (Wcrit, Wcalc))
                lista_aux.append("Rejeito a hipótese H0 que a amostra segue uma distribuição normal")

            resultado.append(lista_aux)
        
            # Criando um dataframe no pandas com todas as colunas
            #df = pd.DataFrame({'i' : i_, 'n - (i - 1)' : n_menos_i_menos_1, 'Ai,n' : Ain, 'X(n-(i-1))' : X_n_menos_i_menos_1,
                                #'Xi' : Xi, 'Valores Bi' : valores_Bi})
        return resultado
    except Exception as e:
        return [False, e]