#PARTE DA VISÃO (MVC)
#RESPONSÁVEL PELA PARTE GRÁFICA (CANVAS E WIDGETS)

from tkinter import *
from tkinter import ttk
from tkinter import colorchooser
from tkinter import filedialog, messagebox


class VisaoDesenho:
    def __init__(self, root):
        self.root = root
        self.root.title('Projeto terceira unidade - Victor Gabriel e Lucas André')

        self.frame = Frame(root)
        paddings = {'padx': 5, 'pady': 5}

        
        label = ttk.Label(self.frame, text='Escolha qual figura irá desenhar ->')
        label.grid(column=0, row=0, sticky=W, **paddings)

        # MENU
        self.tipo_figura_var = StringVar(root)
        option_menu = ttk.OptionMenu(self.frame, self.tipo_figura_var,
                                      'Linha', 'Linha', 'Rabisco', 'Retângulo', 'Círculo', 'Oval', 'Polígono')
        option_menu.grid(column=1, row=0, sticky=W, **paddings)

        # Seletor de cor do traço
        self.cor_var = StringVar(root, value='black')
        label_cor = ttk.Label(self.frame, text='Cor do traço:')
        label_cor.grid(column=2, row=0, sticky=W, **paddings)
        self.botao_cor = Button(self.frame, bg='black', width=3, command=self._escolher_cor)
        self.botao_cor.grid(column=3, row=0, sticky=W, **paddings)

        # Seletor de cor de preenchimento
        self.cor_preenchimento_var = StringVar(root, value='')
        self.sem_preenchimento_var = BooleanVar(root, value=True)
        label_preenchimento = ttk.Label(self.frame, text='Preenchimento:')
        label_preenchimento.grid(column=4, row=0, sticky=W, **paddings)
        self.botao_cor_preenchimento = Button(self.frame, bg='white', text='∅', width=3,
                                               command=self._escolher_cor_preenchimento)
        self.botao_cor_preenchimento.grid(column=5, row=0, sticky=W, **paddings)
        self.check_sem_preenchimento = ttk.Checkbutton(
            self.frame, text='Sem preenchimento', variable=self.sem_preenchimento_var,
            command=self._toggle_sem_preenchimento
        )
        self.check_sem_preenchimento.grid(column=6, row=0, sticky=W, **paddings)

        # Área de desenho
        self.canvas = Canvas(self.frame, bg='white', width=600, height=600)
        self.canvas.grid(column=0, row=1, columnspan=7, sticky=W, **paddings)

        # Botões de Salvar e Abrir (centralizados embaixo do canvas)
        self.frame_botoes_arquivo = Frame(self.frame)
        self.frame_botoes_arquivo.grid(column=0, row=2, columnspan=7, pady=5)
        self.botao_salvar = ttk.Button(self.frame_botoes_arquivo, text='Salvar...')
        self.botao_salvar.pack(side=LEFT, padx=5)
        self.botao_abrir = ttk.Button(self.frame_botoes_arquivo, text='Abrir...')
        self.botao_abrir.pack(side=LEFT, padx=5)

        self.frame.pack()

    # REGISTRA OS CLIQUES DO MOUSE 
    def registrar_eventos(self, ao_pressionar, ao_arrastar, ao_soltar, ao_mover, ao_duplo_clique):
        self.canvas.bind('<ButtonPress-1>', ao_pressionar)
        self.canvas.bind('<B1-Motion>', ao_arrastar)
        self.canvas.bind('<ButtonRelease-1>', ao_soltar)
        self.canvas.bind('<Motion>', ao_mover)
        self.canvas.bind('<Double-Button-1>', ao_duplo_clique)

    # LIGA OS BOTÕES "SALVAR..." E "ABRIR..." (EMBAIXO DO CANVAS) AOS CALLBACKS DO CONTROLADOR
    def registrar_botoes_arquivo(self, ao_salvar, ao_abrir):
        self.botao_salvar.config(command=lambda: self._pedir_arquivo_para_salvar(ao_salvar))
        self.botao_abrir.config(command=lambda: self._pedir_arquivo_para_abrir(ao_abrir))

    # ABRE A CAIXA DE DIÁLOGO "SALVAR COMO" E REPASSA O CAMINHO ESCOLHIDO
    def _pedir_arquivo_para_salvar(self, ao_salvar):
        caminho = filedialog.asksaveasfilename(
            defaultextension='.json',
            filetypes=[('Arquivo de desenho', '*.json')],
            title='Salvar desenho',
        )
        if not caminho:
            return
        try:
            ao_salvar(caminho)
        except Exception as erro:
            messagebox.showerror('Erro ao salvar', str(erro))

    # ABRE A CAIXA DE DIÁLOGO "ABRIR" E REPASSA O CAMINHO ESCOLHIDO
    def _pedir_arquivo_para_abrir(self, ao_abrir):
        caminho = filedialog.askopenfilename(
            defaultextension='.json',
            filetypes=[('Arquivo de desenho', '*.json')],
            title='Abrir desenho',
        )
        if not caminho:
            return
        try:
            ao_abrir(caminho)
        except Exception as erro:
            messagebox.showerror('Erro ao abrir', str(erro))

    # LEUITURA DO QUE O USUARIO ESCOLHEU
    def tipo_figura_selecionado(self):
        return self.tipo_figura_var.get()

    def cor_selecionada(self):
        return self.cor_var.get()

    def cor_preenchimento_selecionada(self):
        if self.sem_preenchimento_var.get():
            return ''
        return self.cor_preenchimento_var.get() or ''

    
    def redesenhar(self, figuras, figura_em_construcao=None):
        self.canvas.delete("all")
        for fig in figuras:
            fig.desenhar(self.canvas)
        if figura_em_construcao is not None:
            figura_em_construcao.desenhar(self.canvas, pontilhado=True)

    
    def _escolher_cor(self):
        cor = colorchooser.askcolor(color=self.cor_var.get(), title="Escolha a cor do traço")
        if cor[1]:
            self.cor_var.set(cor[1])
            self.botao_cor.config(bg=cor[1])

    def _escolher_cor_preenchimento(self):
        cor_atual = self.cor_preenchimento_var.get() or '#ffffff'
        cor = colorchooser.askcolor(color=cor_atual, title="Escolha a cor de preenchimento")
        if cor[1]:
            self.cor_preenchimento_var.set(cor[1])
            self.sem_preenchimento_var.set(False)
            self.botao_cor_preenchimento.config(bg=cor[1], text='')

    def _toggle_sem_preenchimento(self):
        if self.sem_preenchimento_var.get():
            self.botao_cor_preenchimento.config(bg='white', text='∅')
        else:
            cor = self.cor_preenchimento_var.get() or '#ffffff'
            self.botao_cor_preenchimento.config(bg=cor, text='')
