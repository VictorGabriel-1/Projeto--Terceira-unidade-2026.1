#PARTE DAS FIGURAS 

from tkinter import *
from tkinter import ttk
from tkinter import colorchooser
from abc import ABC, abstractmethod


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


class Poligono(Figura):
    """Polígono livre: pontos adicionados por cliques sucessivos, fechado com duplo clique."""

    def __init__(self, x, y, cor, preenchimento=''):
        super().__init__(x, y, cor)
        self.pontos = [(x, y)]
        self.preenchimento = preenchimento
        self.ponto_temporario = None  # posição atual do mouse, para "prévia" do próximo lado

    def atualizar(self, x, y):
        # Aqui "atualizar" apenas guarda a posição do mouse para desenhar a prévia
        # do próximo lado (o polígono não é criado por arraste).
        self.ponto_temporario = (x, y)

    def adicionar_ponto(self, x, y):
        self.pontos.append((x, y))
        self.ponto_temporario = None

    def esta_incompleta(self):
        return len(self.pontos) < 3

    def desenhar(self, canvas, pontilhado=False):
        pontos = self.pontos + ([self.ponto_temporario] if self.ponto_temporario else [])
        if len(pontos) < 2:
            return
        opcoes = {'dash': (4, 2)} if pontilhado else {}
        if len(pontos) >= 3:
            canvas.create_polygon(pontos, outline=self.cor, fill=self.preenchimento, **opcoes)
        else:
            canvas.create_line(pontos, fill=self.cor, **opcoes)


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
    elif tipo == 'Polígono':
        return Poligono(x, y, cor, preenchimento)
    else:  # 'Rabisco'
        return Rabisco(x, y, cor)
