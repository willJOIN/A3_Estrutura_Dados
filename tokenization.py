import util
import re
from grafo import Grafo
from vertice import Vertice
from util import limpar_terminal
from consts import ATIVIDADE


class Tokens:
    def __init__(self, textos: list, nome_pasta_arquivos: str) -> None:
        self.textos = textos
        self.nome_pasta_arquivos = nome_pasta_arquivos
        self.resultado = {}
        self.grafos = []

        limpar_terminal()
        print("Executando algoritmo...")

        for nome_texto in self.textos:
            grafo = Grafo()

            with open(
                f"textos/{nome_pasta_arquivos}/{nome_texto}", "r", encoding="ISO-8859-1"
            ) as f:
                # le o arquivo e armazena em linha
                for line in f.readlines():
                    self.adicionar_grafo(self.execucao_linha(line), grafo)

            self.grafos.append(grafo)

            self.resultado[nome_texto] = (
                grafo.get_lista_topicos_importantes()
                if ATIVIDADE == "TÓPICOS_RELEVANTES"
                else grafo.get_lista_coautoria()
            )

    def __str__(self) -> str:
        string = ""

        titulo_atividade = (
            "Tópicos mais importantes"
            if ATIVIDADE == "TÓPICOS_RELEVANTES"
            else "Rede de Coautoria"
        )

        for idx, grafo in enumerate(self.grafos):
            string += "---------------------------------------------------------------------------\n"
            string += f"Texto -> {self.textos[idx]}          * {titulo_atividade} * \n"
            string += "---------------------------------------------------------------------------\n"
            string += f"{grafo.get_lista_topicos_importantes() if ATIVIDADE == 'TÓPICOS_RELEVANTES' else grafo.get_lista_coautoria()}\n"
            string += "---------------------------------------------------------------------------\n\n"

        return string

    def execucao_linha(self, linha):
        linha_temp = util.limpar_linha(linha)
        linha_temp = util.substituir_acentos(linha_temp)
        linha_temp = util.remover_stop_words(linha_temp)
        linha_temp = util.remover_numeros_romanos(linha_temp)
        linha_temp = util.remover_numeros_extenso(linha_temp)
        linha_temp = util.remover_numeros_ordinais(linha_temp)

        return re.split(" +", linha_temp)

    # adicionar vertices no grafo a partir de uma lista de palavras
    def adicionar_grafo(self, lista_palavras, graph: Grafo):
        for index in range(1, len(lista_palavras)):
            # se palavra nao esta no grafo:
            if not graph.find_vertice(lista_palavras[index - 1]):
                # se for a primeira palavra adiciona-la no grafo
                # adicionar a palavra no grafo e fazer uma conexao de aresta com a ultima palavra
                vertice_x = graph.add_vertice(lista_palavras[index - 1])
                vertice_y = graph.add_vertice(lista_palavras[index])
                graph.add_aresta(vertice_x, vertice_y)

            # se a palavra esta no grafo aumenta o peso e cria uma aresta com a ultima palavra
            else:
                graph.find_vertice(lista_palavras[index - 1]).increment_peso()
                graph.add_aresta(
                    Vertice(lista_palavras[index - 1]), Vertice(lista_palavras[index])
                )