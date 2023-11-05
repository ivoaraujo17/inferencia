import customtkinter as ctk
import tkinter as tk
from tkinter.filedialog import askopenfilename
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from kolmogorov_smirnov import kolmogorov_smirnov, kolmogorov_smirnov_
from shapiro_wilk import shapiro_wilk
from teste_z import teste_z
from teste_Tstudent import t_student_media, t_student_comparacao_media_independente, t_student_diferenca_media_emparelhada
from teste_bartlett import teste_bartlett


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Configurações gerais da janela
        self.font_title = ("Arial", 20, "bold")
        self.font_info = ("Arial", 16, "bold")
        self.title("Inferencia de dados")
        self.maxsize(width=1200, height=600)
        self.minsize(width=1200, height=600)
        self.my_font = ctk.CTkFont(family="Courier", size=20)
        self.my_font_low = ctk.CTkFont(family="Courier", size=14)
        self.protocol("WM_DELETE_WINDOW", self.window_close)
        ctk.set_appearance_mode("white")
        ctk.set_default_color_theme("dark-blue")
        self.hover_color_bt = ("green", "darkgreen")

        # Cria os elementos da janela
        self.file_name = tk.StringVar() # variavel que armazena o nome do arquivo selecionado
        self.radio_var = tk.IntVar(value=0) # variavel que armazena o valor do radio button selecionado
        # radio buttons com a lista de testes
        self.teste_1 = ctk.CTkRadioButton(master=self, text="Kolmogorov", command=self.remove_tabview, font=self.my_font, variable=self.radio_var, value=1)
        self.teste_2 = ctk.CTkRadioButton(master=self, text="Shapiro_Wilk", command=self.remove_tabview, font=self.my_font, variable=self.radio_var, value=2)
        self.teste_3 = ctk.CTkRadioButton(master=self, text="Teste_Z", command=self.remove_tabview, font=self.my_font, variable=self.radio_var, value=3)
        self.teste_4 = ctk.CTkRadioButton(master=self, text="T_student_media", command=self.remove_tabview, font=self.my_font, variable=self.radio_var, value=4)
        self.teste_5 = ctk.CTkRadioButton(master=self, text="T_student_comparacao", command=self.remove_tabview, font=self.my_font, variable=self.radio_var, value=5)
        self.teste_6 = ctk.CTkRadioButton(master=self, text="T_student_diferenca", command=self.remove_tabview, font=self.my_font, variable=self.radio_var, value=6)
        self.teste_7 = ctk.CTkRadioButton(master=self, text="Bartlett", command=self.remove_tabview, font=self.my_font, variable=self.radio_var, value=7)
        # botão de seleção do arquivo excel
        self.button_select_file = ctk.CTkButton(master=self, text="Selecionar arquivo", font=self.my_font, command=self.button_select_file_event, hover_color=self.hover_color_bt)
        # label que mostra o caminho do arquivo selecionado
        self.label_file_select = ctk.CTkLabel(master=self, text="Nenhum arquivo selecionado", font=self.my_font_low)
        # botão de execução
        self.button_executar = ctk.CTkButton(master=self, text="Executar", font=self.my_font, command=self.button_executar_event, hover_color=self.hover_color_bt)
        # tabela de resultados
        self.tabview = ctk.CTkTabview(master=self, width=1100, height=320)
        #valor alpha
        self.valor_alpha = ctk.CTkEntry(master=self, width=80, placeholder_text='alpha')
        #valor média populacional prevista
        self.valor_media_populacional_prevista = ctk.CTkEntry(master=self, width=80, placeholder_text='media pop')
        

    def remove_tabview(self):
        indice = 1
        while True:
            try:
                self.tabview.delete(f'amostra_{indice}')
                indice += 1
            except:
                break


    def button_executar_event(self):
        self.remove_tabview()
        alfa = None
        if self.valor_alpha.get() == '':
            return
        else:
            try:
                alfa = float(self.valor_alpha.get())
            except:
                return
        
        # Teste 1: Kolmogorov
        if self.radio_var.get() == 1 and self.file_is_valid():
            if "amostras_normais.csv" in self.file_name.get():
                resultados, Xis = kolmogorov_smirnov(self.file_name.get(), alfa)
                grafico = 1
            elif "amostra_kolmogorov_do_pdf.csv" in self.file_name.get():
                resultados, Xis = kolmogorov_smirnov(self.file_name.get(), alfa)
                grafico = 2
            else:
                resultados, Xis, freq_abs = kolmogorov_smirnov_(self.file_name.get(), alfa)
                grafico = 3
            self.remove_tabview()
            if not resultados[0][0]:
                self.tabview.add("amostra_1")
                ctk.CTkLabel(master=self.tabview.tab("amostra_1"), text="Erro", font=self.my_font_low).grid(row=0, column=0)
                ctk.CTkLabel(master=self.tabview.tab("amostra_1"), text=resultados[0][1], font=self.my_font_low).grid(row=1, column=0)
            else:
                for i, resultado in enumerate(resultados):
                    nome = str(f'amostra_{i+1}')
                    self.tabview.add(nome)
                    ctk.CTkLabel(master=self.tabview.tab(nome), text=resultado[1], font=self.my_font_low).grid(row=0, column=0)
                    ctk.CTkLabel(master=self.tabview.tab(nome), text=resultado[2], font=self.my_font_low).grid(row=1, column=0)
                    # prepara o canva do grafico
                    fig = plt.Figure(figsize=(4, 2), dpi=100)
                    ax = fig.add_subplot(111)
                    ax.xaxis.set_label_position("top")
                    ax.set_xlabel('Valores')  
                    ax.set_ylabel('Frequência Absoluta')  
                    if grafico == 1:
                        ax.hist(Xis[i], bins = len(Xis[i]), density = False)
                    elif grafico == 2:
                        ax.hist(Xis[i], bins = 10, density = False)
                    else:
                        ax.bar(Xis[i], freq_abs[i])
                    canvas = FigureCanvasTkAgg(fig, self.tabview.tab(nome))
                    # grafico com o resultado
                    canvas.get_tk_widget().grid(row=2, column=0)
                self.tabview.tab('amostra_1').focus_force()

        # Teste 2: Shapiro-Wilk
        elif self.radio_var.get() == 2 and self.file_is_valid():
            resultados, valores_grafico = shapiro_wilk(self.file_name.get(), alfa)
            if not resultados[0][0]:
                self.tabview.add("amostra_1")
                ctk.CTkLabel(master=self.tabview.tab("amostra_1"), text="Erro", font=self.my_font_low).grid(row=0, column=0)
                ctk.CTkLabel(master=self.tabview.tab("amostra_1"), text=resultados[0][1], font=self.my_font_low).grid(row=1, column=0)
            else:
                for i, resultado in enumerate(resultados):
                    nome = str(f'amostra_{i+1}')
                    self.tabview.add(nome)
                    ctk.CTkLabel(master=self.tabview.tab(nome), text=resultado[1], font=self.my_font_low).grid(row=0, column=0)
                    ctk.CTkLabel(master=self.tabview.tab(nome), text=resultado[2], font=self.my_font_low).grid(row=1, column=0)
                    # prepara o canva do grafico
                    fig = plt.Figure(figsize=(4, 2), dpi=100)
                    ax = fig.add_subplot(111)
                    ax.xaxis.set_label_position("top")
                    ax.set_xlabel('Valores')  
                    ax.set_ylabel('Frequência Absoluta')  
                    ax.hist(valores_grafico[i], bins = len(valores_grafico[i]), density = False)
                    canvas = FigureCanvasTkAgg(fig, self.tabview.tab(nome))
                    # grafico com o resultado
                    canvas.get_tk_widget().grid(row=2, column=0)

        # Teste 3: Teste Z
        elif self.radio_var.get() == 3 and self.file_is_valid():
            if self.valor_media_populacional_prevista.get() == '':
                return
            try:
                media_populacional = float(self.valor_media_populacional_prevista.get())
            except:
                return
            resultados, info_amostra = teste_z(self.file_name.get(), media_populacional, alfa)
            if not resultados[0][0]:
                self.tabview.add("amostra_1")
                ctk.CTkLabel(master=self.tabview.tab("amostra_1"), text="Erro", font=self.my_font_low).grid(row=0, column=0)
                ctk.CTkLabel(master=self.tabview.tab("amostra_1"), text=resultados[0][1], font=self.my_font_low).grid(row=1, column=0)
            else:
                for i, resultado in enumerate(resultados):
                    nome = str(f'amostra_1')
                    self.tabview.add(nome)
                    ctk.CTkLabel(master=self.tabview.tab(nome), text=info_amostra[0], font=self.my_font_low).grid(row=0, column=0)
                    ctk.CTkLabel(master=self.tabview.tab(nome), text=resultado[1], font=self.my_font_low).grid(row=1, column=0)
                    ctk.CTkLabel(master=self.tabview.tab(nome), text=resultado[2], font=self.my_font_low).grid(row=2, column=0)
                    ctk.CTkLabel(master=self.tabview.tab(nome), text=resultado[3], font=self.my_font_low).grid(row=3, column=0)

        # Teste 4: T-student media
        elif self.radio_var.get() == 4 and self.file_is_valid():
            if self.valor_media_populacional_prevista.get() == '':
                return
            try:
                media_populacional = float(self.valor_media_populacional_prevista.get())
            except:
                return
            resultados, info_amostra = t_student_media(self.file_name.get(), media_populacional, alfa)
            if not resultados[0][0]:
                self.tabview.add("amostra_1")
                ctk.CTkLabel(master=self.tabview.tab("amostra_1"), text="Erro", font=self.my_font_low).grid(row=0, column=0)
                ctk.CTkLabel(master=self.tabview.tab("amostra_1"), text=resultados[0][1], font=self.my_font_low).grid(row=1, column=0)
            else:
                for i, resultado in enumerate(resultados):
                    nome = str(f'amostra_1')
                    self.tabview.add(nome)
                    ctk.CTkLabel(master=self.tabview.tab(nome), text=info_amostra[0], font=self.my_font_low).grid(row=0, column=0)
                    ctk.CTkLabel(master=self.tabview.tab(nome), text=resultado[1], font=self.my_font_low).grid(row=1, column=0)
                    ctk.CTkLabel(master=self.tabview.tab(nome), text=resultado[2], font=self.my_font_low).grid(row=2, column=0)
                    ctk.CTkLabel(master=self.tabview.tab(nome), text=resultado[3], font=self.my_font_low).grid(row=3, column=0)

        # Teste 5: T-student comparacao medias independentes
        elif self.radio_var.get() == 5 and self.file_is_valid():
            resultados, info_amostra1, info_amostra2 = t_student_comparacao_media_independente(self.file_name.get(), alfa)
            if not resultados[0][0]:
                self.tabview.add("amostra_1")
                ctk.CTkLabel(master=self.tabview.tab("amostra_1"), text="Erro", font=self.my_font_low).grid(row=0, column=0)
                ctk.CTkLabel(master=self.tabview.tab("amostra_1"), text=resultados[0][1], font=self.my_font_low).grid(row=1, column=0)
            else:
                for i, resultado in enumerate(resultados):
                    nome = str(f'amostra_1')
                    self.tabview.add(nome)
                    ctk.CTkLabel(master=self.tabview.tab(nome), text=info_amostra1[0], font=self.my_font_low).grid(row=0, column=0)
                    ctk.CTkLabel(master=self.tabview.tab(nome), text=info_amostra2[0], font=self.my_font_low).grid(row=1, column=0)
                    ctk.CTkLabel(master=self.tabview.tab(nome), text=resultado[1], font=self.my_font_low).grid(row=2, column=0)
                    ctk.CTkLabel(master=self.tabview.tab(nome), text=resultado[2], font=self.my_font_low).grid(row=3, column=0)
                    ctk.CTkLabel(master=self.tabview.tab(nome), text=resultado[3], font=self.my_font_low).grid(row=4, column=0)

        # Teste 6: T-student diferença de medias emparelhadas
        elif self.radio_var.get() == 6 and self.file_is_valid():
            resultados, info_amostra1, info_amostra2 = t_student_diferenca_media_emparelhada(self.file_name.get(), alfa)
            if not resultados[0][0]:
                self.tabview.add("amostra_1")
                ctk.CTkLabel(master=self.tabview.tab("amostra_1"), text="Erro", font=self.my_font_low).grid(row=0, column=0)
                ctk.CTkLabel(master=self.tabview.tab("amostra_1"), text=resultados[0][1], font=self.my_font_low).grid(row=1, column=0)
            else:
                for i, resultado in enumerate(resultados):
                    nome = str(f'amostra_1')
                    self.tabview.add(nome)
                    ctk.CTkLabel(master=self.tabview.tab(nome), text=info_amostra1[0], font=self.my_font_low).grid(row=0, column=0)
                    ctk.CTkLabel(master=self.tabview.tab(nome), text=info_amostra2[0], font=self.my_font_low).grid(row=1, column=0)
                    ctk.CTkLabel(master=self.tabview.tab(nome), text=resultado[1], font=self.my_font_low).grid(row=2, column=0)
                    ctk.CTkLabel(master=self.tabview.tab(nome), text=resultado[2], font=self.my_font_low).grid(row=3, column=0)
                    ctk.CTkLabel(master=self.tabview.tab(nome), text=resultado[3], font=self.my_font_low).grid(row=4, column=0)
        
        #Teste 7: Bartlett
        elif self.radio_var.get() == 7 and self.file_is_valid():
            resultados, info_amostra, qtd_amostras = teste_bartlett(self.file_name.get(), alfa)
            if not resultados[0][0]:
                self.tabview.add("amostra_1")
                ctk.CTkLabel(master=self.tabview.tab("amostra_1"), text="Erro", font=self.my_font_low).grid(row=0, column=0)
                ctk.CTkLabel(master=self.tabview.tab("amostra_1"), text=resultados[0][1], font=self.my_font_low).grid(row=1, column=0)
            else:
                for i, resultado in enumerate(resultados):
                    nome = str(f'amostra_1')
                    self.tabview.add(nome)
                    for j in range(qtd_amostras):
                        ctk.CTkLabel(master=self.tabview.tab(nome), text=info_amostra[j], font=self.my_font_low).grid(row=j, column=0)
                    ctk.CTkLabel(master=self.tabview.tab(nome), text=resultado[1], font=self.my_font_low).grid(row=j+1, column=0)
                    ctk.CTkLabel(master=self.tabview.tab(nome), text=resultado[2], font=self.my_font_low).grid(row=j+2, column=0)
                    ctk.CTkLabel(master=self.tabview.tab(nome), text=resultado[3], font=self.my_font_low).grid(row=j+3, column=0)
        else:
            print("nenhum teste selecionado")
    
    def button_select_file_event(self):
        self.remove_tabview()
        filename = askopenfilename()
        self.label_file_select.configure(text=filename)
        self.file_name.set(filename)
    
    def file_is_valid(self):
        if self.file_name.get() == '':
            return False
        else:
            return True
    
    def run(self):
        # Coloca cada elemento em seu devido lugar
        ## titulos
        ctk.CTkLabel(master=self, text="Inferência de dados", font=self.my_font).place(x=50, y=20)
        ctk.CTkLabel(master=self, text="Escolha o tipo de teste:", font=self.my_font).place(x=50, y=50)
        # Botão de selecao dos testes
        self.teste_1.place(x=65, y=80)
        self.teste_2.place(x=65, y=110)
        self.teste_3.place(x=65, y=140)
        self.teste_4.place(x=65, y=170)
        self.teste_5.place(x=65, y=200)
        self.teste_6.place(x=65, y=225)
        self.teste_7.place(x=250, y=80)
        # Titulos da seleção do arquivo excel
        ctk.CTkLabel(master=self, text="""Escolha o arquivo Excel""", font=self.my_font, anchor='w').place(x=600, y=70)
        ctk.CTkLabel(master=self, text="O arquivo deve conter apenas uma coluna com as amostras", font=self.my_font_low, anchor='w').place(x=600, y=110)
        # Botão de seleção do arquivo excel
        self.button_select_file.place(x=600, y=145)
        # Label que mostra o caminho do arquivo selecionado
        self.label_file_select.place(x=600, y=175)
        # 
        self.valor_alpha.place(x=340, y=180)
        # botao da média populacional prevista
        self.valor_media_populacional_prevista.place(x=340, y=140)
        # Botão de execução
        self.button_executar.place(x=340, y=220)
        # Tabela de resultados
        self.tabview.place(x=50, y=250)
        

        # loop principal
        self.mainloop()
    
    def window_close(self):
        self.destroy()

app = App()
app.run()
