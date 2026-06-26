from tkinter import *
from tkinter import ttk
from tkinter import colorchooser
 
# Quando mouse é pressionado
def iniciar_figura_nova(event): 
    global figura_nova
    if tipo_figura_var.get() == 'Linha':
        figura_nova = ("linha", (event.x, event.y, event.x, event.y))
    elif tipo_figura_var.get() == 'Retângulo':
        figura_nova = ("retangulo", (event.x, event.y, event.x, event.y))
    elif tipo_figura_var.get() == 'Círculo':
        figura_nova = ("circulo", (event.x, event.y, event.x, event.y))
    elif tipo_figura_var.get() == 'Oval':
        figura_nova = ("oval", (event.x, event.y, event.x, event.y))
    else :
        figura_nova = ("rabisco", [(event.x, event.y)])
 
# Quando mouse é movido com o botão pressionado
def atualizar_figura_nova(event):
    global figura_nova
    if figura_nova[0] == "rabisco":
        figura_nova[1].append((event.x, event.y))
    elif figura_nova[0] == "retangulo" or figura_nova[0] == 'oval':
        figura_nova = (figura_nova[0], (figura_nova[1][0], figura_nova[1][1], event.x, event.y))
    elif figura_nova[0] == "circulo":
        x1, y1 = figura_nova[1][0], figura_nova[1][1]
        lado = max(abs(event.x - x1), abs(event.y - y1))  # RAIO IGUAL (PARA NAO SER OVAL)
        if event.x >= x1:
            x2 = x1 + lado
        else :
            x2 = x1 - lado
        if event.y >= y1:
            y2 = y1 + lado
        else :
            y2 = y1 - lado
        figura_nova = ("circulo", (x1, y1, x2, y2))
    else : # figura_nova[0] == "linha"
        figura_nova = ("linha", (figura_nova[1][0], figura_nova[1][1], event.x, event.y))
    desenhar_figuras()
    desenhar_figura_nova()
 
# Quando mouse é solto
def incluir_figura_nova(event): 
    if not incompleta(figura_nova): # para evitar incluir figuras incompletas, como uma linha sem comprimento ou um rabisco com um único ponto
        figuras.append((figura_nova, cor_var.get(), get_fill())) 
    desenhar_figuras()
 
def get_fill():
    if sem_preenchimento_var.get():
        return ''
    return cor_preenchimento_var.get() or ''

def desenhar_figuras():
    canvas.delete("all")
    for (fig, values), cor, fill in figuras:
        if fig == "linha":
            canvas.create_line(values[0], values[1], values[2], values[3], fill=cor)
        elif fig == "retangulo":
            canvas.create_rectangle(values[0], values[1], values[2], values[3], outline=cor, fill=fill)
        elif fig == 'circulo' or fig == 'oval' :
            canvas.create_oval(values[0], values[1], values[2], values[3], outline=cor, fill=fill)
        else : # fig == "rabisco"
            canvas.create_line(values, fill=cor)
 
def desenhar_figura_nova():
    fig, values = figura_nova
    cor = cor_var.get()
    fill = get_fill()
    if fig == "linha":
        canvas.create_line(values[0], values[1], values[2], values[3], dash=(4, 2), fill=cor)
    elif fig == "retangulo":
        canvas.create_rectangle(values[0], values[1], values[2], values[3], dash=(4, 2), outline=cor, fill=fill)
    elif fig == "circulo" or fig == 'oval':
        canvas.create_oval(values[0], values[1], values[2], values[3], dash=(4, 2), outline=cor, fill=fill)
    else : # fig == "rabisco"
        canvas.create_line(values, dash=(4, 2), fill=cor)
 
def incompleta(figura):
    fig, values = figura
    if fig == "rabisco":
        return len(values) <= 1
    else :
        return (values[0], values[1]) == (values[2], values[3])
 
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
 
figuras = []       # Todas as figuras desenhadas: lista de ((fig, values), cor)
figura_nova = None # Figura que está sendo desenhada, mas ainda não foi incluída em figuras
 
root = Tk()
root.title('Projeto terceira unidade - Victor Gabriel e Lucas André')
frame = Frame(root)
 
# Widgets arranjados com Layout grid dentro de frame
paddings = {'padx': 5, 'pady': 5} 
 
# label
label = ttk.Label(frame,  text='Escolha qual figura irá desenhar ->')
label.grid(column=0, row=0, sticky=W, **paddings)
 
# option menu
tipo_figura_var = StringVar(root) # Guarda o tipo de figura selecionado no option menu (linha ou rabisco)
option_menu = ttk.OptionMenu(frame, tipo_figura_var,
                             'Linha', 'Linha', 'Rabisco' , 'Retângulo', 'Círculo', 'Oval' )
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