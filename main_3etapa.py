# CODIGO PRINCIPAL ( CHAMA VISAO, FIGURAS E MOUSE)

from tkinter import Tk
from modelo import Desenho
from visao import VisaoDesenho
from controlador import ControladorDesenho


def main():
    root = Tk()
    modelo = Desenho()
    visao = VisaoDesenho(root)
    ControladorDesenho(modelo, visao)
    root.mainloop()


if __name__ == '__main__':
    main()
