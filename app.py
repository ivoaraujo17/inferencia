import customtkinter as ctk
import tkinter as tk
from tkinter.filedialog import askopenfilename
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from kolmogorov_smirnov import kolmogorov_smirnov, kolmogorov_smirnov_
from shapiro_wilk import shapiro_wilk

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
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.hover_color_bt = ("green", "darkgreen")

        # Cria os elementos da janela
        self.file_name = tk.StringVar() # variavel que armazena o nome do arquivo selecionado
        self.radio_var = tk.IntVar(value=0) # variavel que armazena o valor do radio button selecionado
        # radio buttons com a lista de testes
        self.teste_1 = ctk.CTkRadioButton(master=self, text="Kolmogorov", command=self.remove_tabview, font=self.my_font, variable=self.radio_var, value=1)
        self.teste_2 = ctk.CTkRadioButton(master=self, text="Shapiro_Wilk", command=self.remove_tabview, font=self.my_font, variable=self.radio_var, value=2)
        # botão de seleção do arquivo excel
        self.button_select_file = ctk.CTkButton(master=self, text="Selecionar arquivo", font=self.my_font, command=self.button_select_file_event, hover_color=self.hover_color_bt)
        # label que mostra o caminho do arquivo selecionado
        self.label_file_select = ctk.CTkLabel(master=self, text="Nenhum arquivo selecionado", font=self.my_font_low)
        # botão de execução
        self.button_executar = ctk.CTkButton(master=self, text="Executar", font=self.my_font, command=self.button_executar_event, hover_color=self.hover_color_bt)
        # tabela de resultados
        self.tabview = ctk.CTkTabview(master=self, width=1100, height=320)
        
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
        alfa = 0.05
        if self.radio_var.get() == 1:
            resultados = kolmogorov_smirnov(self.file_name.get(), alfa)
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
                    canvas = FigureCanvasTkAgg(fig, self.tabview.tab(nome))
                    # grafico com o resultado
                    canvas.get_tk_widget().grid(row=2, column=0)

        elif self.radio_var.get() == 2:
            resultados = shapiro_wilk(self.file_name.get(), alfa)
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
                    canvas = FigureCanvasTkAgg(fig, self.tabview.tab(nome))
                    # grafico com o resultado
                    canvas.get_tk_widget().grid(row=2, column=0)
        else:
            print("nenhum teste selecionado")
    
    def button_select_file_event(self):
        self.remove_tabview()
        filename = askopenfilename()
        self.label_file_select.configure(text=filename)
        self.file_name.set(filename)
    
    def run(self):
        # Coloca cada elemento em seu devido lugar
        ## titulos
        ctk.CTkLabel(master=self, text="Inferência de dados", font=self.my_font).place(x=50, y=20)
        ctk.CTkLabel(master=self, text="Escolha o tipo de teste:", font=self.my_font).place(x=50, y=70)
        # Botão de selecao dos testes
        self.teste_1.place(x=65, y=120)
        self.teste_2.place(x=65, y=170)
        # Titulos da seleção do arquivo excel
        ctk.CTkLabel(master=self, text="""Escolha o arquivo Excel""", font=self.my_font, anchor='w').place(x=600, y=70)
        ctk.CTkLabel(master=self, text="O arquivo deve conter apenas uma coluna com as amostras", font=self.my_font_low, anchor='w').place(x=600, y=110)
        # Botão de seleção do arquivo excel
        self.button_select_file.place(x=600, y=145)
        # Label que mostra o caminho do arquivo selecionado
        self.label_file_select.place(x=600, y=175)
        # Botão de execução
        self.button_executar.place(x=300, y=220)
        # Tabela de resultados
        self.tabview.place(x=50, y=250)
        

        # loop principal
        self.mainloop()
    
    def window_close(self):
        self.destroy()


app = App()
app.run()
