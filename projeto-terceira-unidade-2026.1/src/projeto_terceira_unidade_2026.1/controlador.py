#PARTE DO MOUSE (MVC)
# RECEBE OS EVENTOS DO MOUSE 


from modelo import Desenho


class ControladorDesenho:
    def __init__(self, modelo: Desenho, visao):
        self.modelo = modelo
        self.visao = visao
        self.visao.registrar_eventos(
            ao_pressionar=self.ao_pressionar_mouse,
            ao_arrastar=self.ao_arrastar_mouse,
            ao_soltar=self.ao_soltar_mouse,
            ao_mover=self.ao_mover_mouse,
            ao_duplo_clique=self.ao_duplo_clique,
        )
        self.visao.registrar_botoes_arquivo(
            ao_salvar=self.ao_salvar_arquivo,
            ao_abrir=self.ao_abrir_arquivo,
        )

    # Quando o mouse é pressionado
    def ao_pressionar_mouse(self, event):
        tipo = self.visao.tipo_figura_selecionado()
        cor = self.visao.cor_selecionada()
        preenchimento = self.visao.cor_preenchimento_selecionada()

        if tipo == 'Polígono':
            
            if not self.modelo.figura_atual_e_poligono():
                self.modelo.iniciar_figura(tipo, event.x, event.y, cor, preenchimento)
            else:
                self.modelo.adicionar_ponto_poligono(event.x, event.y)
        else:
            self.modelo.iniciar_figura(tipo, event.x, event.y, cor, preenchimento)

        self._redesenhar()

    # Quando o mouse é movido com o botão pressionado
    def ao_arrastar_mouse(self, event):
        if self.modelo.figura_atual_e_poligono():
            return  #POLIGONO NAO USA ARRASTE DO MOUSE (FEITO POR PONTOS)
        self.modelo.atualizar_figura_atual(event.x, event.y)
        self._redesenhar()

    # Quando o mouse é solto
    def ao_soltar_mouse(self, event):
        if self.modelo.figura_atual_e_poligono():
            return  # CONCLUI O POLIGONO COM DUPLO CLIQUE 
        self.modelo.concluir_figura_atual()
        self._redesenhar()

    def ao_mover_mouse(self, event):
        if self.modelo.figura_atual_e_poligono():
            self.modelo.atualizar_figura_atual(event.x, event.y)
            self._redesenhar()

    # FECHA O POLÍGONO COM DUPLO CLIQUE 
    def ao_duplo_clique(self, event):
        if self.modelo.figura_atual_e_poligono():
            self.modelo.concluir_figura_atual()
            self._redesenhar()

    # SALVA O DESENHO ATUAL NO ARQUIVO ESCOLHIDO PELO USUÁRIO
    def ao_salvar_arquivo(self, caminho):
        self.modelo.salvar(caminho)

    # ABRE UM ARQUIVO E CARREGA O DESENHO SALVO NELE
    def ao_abrir_arquivo(self, caminho):
        self.modelo.abrir(caminho)
        self._redesenhar()

    def _redesenhar(self):
        self.visao.redesenhar(self.modelo.figuras, self.modelo.figura_atual)
