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