from tkinter import *
from tkinter import ttk
from tkinter import colorchooser
from abc import ABC, abstractmethod


# HIERARQUIA DE CLASSES

class Figura(ABC):
    def __init__(self, x, y, cor):
        self.cor = cor

    @abstractmethod
    def atualizar(self, x, y):
        """Atualiza a figura com a posição atual do mouse (botão pressionado)."""

    @abstractmethod
    def desenhar(self, canvas, pontilhado=False):
        """Desenha a figura no canvas."""

    @abstractmethod
    def esta_incompleta(self):
        '''True se a figura é degenerada ex.: rabisco com 1 ponto só.'''

    def _opcoes_traco(self, pontilhado):
        opcoes = {'fill': self.cor}
        if pontilhado:
            opcoes['dash'] = (4, 2)
        return opcoes


class FiguraComXeY(Figura):
    def __init__(self, x, y, cor, preenchimento=''):
        super().__init__(x, y, cor)
        self.x1, self.y1 = x, y
        self.x2, self.y2 = x, y
        self.preenchimento = preenchimento

    def atualizar(self, x, y):
        self.x2, self.y2 = x, y

    def esta_incompleta(self):
        return (self.x1, self.y1) == (self.x2, self.y2)

    def _opcoes_contorno(self, pontilhado):
        opcoes = {'outline': self.cor, 'fill': self.preenchimento}
        if pontilhado:
            opcoes['dash'] = (4, 2)
        return opcoes


class Linha(FiguraComXeY):
    def __init__(self, x, y, cor):
        super().__init__(x, y, cor)  # sem preenchimento

    def desenhar(self, canvas, pontilhado=False):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, **self._opcoes_traco(pontilhado))


class Retangulo(FiguraComXeY):
    def desenhar(self, canvas, pontilhado=False):
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, **self._opcoes_contorno(pontilhado))


class Oval(FiguraComXeY):
    def desenhar(self, canvas, pontilhado=False):
        canvas.create_oval(self.x1, self.y1, self.x2, self.y2, **self._opcoes_contorno(pontilhado))


class Circulo(Oval):
    def atualizar(self, x, y):
        lado = max(abs(x - self.x1), abs(y - self.y1))  # RAIO IGUAL (PARA NAO SER OVAL)
        self.x2 = self.x1 + lado if x >= self.x1 else self.x1 - lado
        self.y2 = self.y1 + lado if y >= self.y1 else self.y1 - lado


class Rabisco(Figura):
    def __init__(self, x, y, cor):
        super().__init__(x, y, cor)
        self.pontos = [(x, y)]

    def atualizar(self, x, y):
        self.pontos.append((x, y))

    def desenhar(self, canvas, pontilhado=False):
        canvas.create_line(self.pontos, **self._opcoes_traco(pontilhado))

    def esta_incompleta(self):
        return len(self.pontos) <= 1


# Fábrica: cria a subclasse correta de Figura a partir do tipo escolhido no option menu
def criar_figura(tipo, x, y, cor, preenchimento):
    if tipo == 'Linha':
        return Linha(x, y, cor)
    elif tipo == 'Retângulo':
        return Retangulo(x, y, cor, preenchimento)
    elif tipo == 'Círculo':
        return Circulo(x, y, cor, preenchimento)
    elif tipo == 'Oval':
        return Oval(x, y, cor, preenchimento)
    else:  # 'Rabisco'
        return Rabisco(x, y, cor)


# CALLBACKS DE EVENTOS DO MOUSE

# Quando mouse é pressionado
def iniciar_figura_nova(event):
    global figura_nova
    figura_nova = criar_figura(tipo_figura_var.get(), event.x, event.y, cor_var.get(), get_fill())

# Quando mouse é movido com o botão pressionado
def atualizar_figura_nova(event):
    figura_nova.atualizar(event.x, event.y)
    desenhar_figuras()
    figura_nova.desenhar(canvas, pontilhado=True)

# Quando mouse é solto
def incluir_figura_nova(event):
    if not figura_nova.esta_incompleta():  # evita incluir figuras incompletas, como um rabisco com um único ponto
        figuras.append(figura_nova)
    desenhar_figuras()

def get_fill():
    if sem_preenchimento_var.get():
        return ''
    return cor_preenchimento_var.get() or ''

def desenhar_figuras():
    canvas.delete("all")
    for fig in figuras:
        fig.desenhar(canvas)

# Abre o seletor de cor e atualiza cor_var e o botão visual
def escolher_cor():
    cor = colorchooser.askcolor(color=cor_var.get(), title="Escolha a cor do traço")
    if cor[1]:
        cor_var.set(cor[1])
        botao_cor.config(bg=cor[1])

# Abre o seletor de cor de preenchimento
def escolher_cor_preenchimento():
    cor_atual = cor_preenchimento_var.get() if cor_preenchimento_var.get() else '#ffffff'
    cor = colorchooser.askcolor(color=cor_atual, title="Escolha a cor de preenchimento")
    if cor[1]:
        cor_preenchimento_var.set(cor[1])
        sem_preenchimento_var.set(False)
        botao_cor_preenchimento.config(bg=cor[1], text='')

def toggle_sem_preenchimento():
    if sem_preenchimento_var.get():
        botao_cor_preenchimento.config(bg='white', text='∅')
    else:
        cor = cor_preenchimento_var.get() or '#ffffff'
        botao_cor_preenchimento.config(bg=cor, text='')




#******* MAIN *******#

figuras = []        # Todas as figuras desenhadas: lista de objetos Figura (Linha, Retangulo, Oval, Circulo, Rabisco)
figura_nova = None  # Figura (objeto) que está sendo desenhada, mas ainda não foi incluída em figuras

root = Tk()
root.title('Projeto terceira unidade - Victor Gabriel e Lucas André')
frame = Frame(root)

# Widgets arranjados com Layout grid dentro de frame
paddings = {'padx': 5, 'pady': 5}

# label
label = ttk.Label(frame,  text='Escolha qual figura irá desenhar ->')
label.grid(column=0, row=0, sticky=W, **paddings)

# option menu
tipo_figura_var = StringVar(root)  # Guarda o tipo de figura selecionado no option menu
option_menu = ttk.OptionMenu(frame, tipo_figura_var,
                             'Linha', 'Linha', 'Rabisco', 'Retângulo', 'Círculo', 'Oval')
option_menu.grid(column=1, row=0, sticky=W, **paddings)

# Seletor de cor
cor_var = StringVar(root, value='black')  # Cor padrão: preto
label_cor = ttk.Label(frame, text='Cor do traço:')
label_cor.grid(column=2, row=0, sticky=W, **paddings)
botao_cor = Button(frame, bg='black', width=3, command=escolher_cor)
botao_cor.grid(column=3, row=0, sticky=W, **paddings)

# Seletor de cor de preenchimento
cor_preenchimento_var = StringVar(root, value='')
sem_preenchimento_var = BooleanVar(root, value=True)
label_preenchimento = ttk.Label(frame, text='Preenchimento:')
label_preenchimento.grid(column=4, row=0, sticky=W, **paddings)
botao_cor_preenchimento = Button(frame, bg='white', text='∅', width=3, command=escolher_cor_preenchimento)
botao_cor_preenchimento.grid(column=5, row=0, sticky=W, **paddings)
check_sem_preenchimento = ttk.Checkbutton(frame, text='Sem preenchimento', variable=sem_preenchimento_var, command=toggle_sem_preenchimento)
check_sem_preenchimento.grid(column=6, row=0, sticky=W, **paddings)

# Área de desenho
canvas = Canvas(frame, bg='white', width=600, height=600)
canvas.grid(column=0, row=1, columnspan=7, sticky=W, **paddings)

frame.pack()

# Eventos de mouse associados ao canvas - com seus callbacks (USO DO MOUSE)
canvas.bind('<ButtonPress-1>', iniciar_figura_nova)
canvas.bind('<B1-Motion>', atualizar_figura_nova)
canvas.bind('<ButtonRelease-1>', incluir_figura_nova)

root.mainloop()