import re

from geral import util
from modelos.grafo import Grafo, Vertice


class Tokens:
    def __init__(self, textos: list, nome_pasta_arquivos: str, artigos=[]) -> None:
        self.textos = textos
        self.nome_pasta_arquivos = nome_pasta_arquivos
        self.resultado = {}
        self.grafos = []

        util.limpar_terminal()
        print("Executando algoritmo...")
        if nome_pasta_arquivos == "atividade1":
            for nome_texto in self.textos:
                grafo = Grafo()

                with open(
                    f"textos/{nome_pasta_arquivos}/{nome_texto}",
                    "r",
                    encoding="ISO-8859-1",
                ) as f:
                    # le o arquivo e armazena em linha
                    for line in f.readlines():
                        self.adicionar_grafo((self.execucao_linha(line)), grafo)

                self.grafos.append(grafo)

                self.resultado[nome_texto] = grafo.get_lista_topicos_importantes()

            return

        elif nome_pasta_arquivos == "atividade2":
            grafo = Grafo()

            self.adicionar_grafo(
                [
                    valor.replace("-", " ")
                    for valor in self.execucao_linha_autores(artigos)
                ],
                grafo,
            )
            self.grafos.append(grafo)
            self.resultado["*RESULTADO*"] = grafo.get_lista_coautoria()

    def __str__(self) -> str:
        util.limpar_terminal()

        string = ""

        titulo_atividade = (
            "Tópicos mais importantes"
            if self.nome_pasta_arquivos == "atividade1"
            else "Rede de Coautoria"
        )

        for idx, grafo in enumerate(self.grafos):
            string += "---------------------------------------------------------------------------\n"
            string += f"Texto -> {self.textos[idx]}          * {titulo_atividade} * \n"
            string += "---------------------------------------------------------------------------\n"
            string += f"{(grafo.get_lista_topicos_importantes() if self.nome_pasta_arquivos == 'atividade1' else (grafo.get_lista_coautoria() if self.nome_pasta_arquivos == 'atividade2' else None))}\n"
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

    def execucao_linha_autores(self, artigos):
        todos_autores = " ".join(
            [
                " ".join([autor.upper().replace(" ", "-") for autor in artigo.autores])
                for artigo in artigos
            ]
        )
        return re.split(" +", util.substituir_acentos(todos_autores))

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
