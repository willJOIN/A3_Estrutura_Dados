import util
import re
from grafo import Grafo

class Topicos:

  def __init__(self, textos: list) -> None:
    self.textos = textos
    self.gerar()
  
  def __str__(self) -> str:
    string = ""
  
    for arquivo, token_list in self.topicos_tokens.items():
      string += f"\n\n10 palavras mais frequentes em {arquivo}:\n{token_list}"
  
    return string
  
  def execucao_linha(self, linha):
  
    linha_temp = util.limpar_linha(linha)
    linha_temp = util.substituir_acentos(linha_temp)
    linha_temp = util.remover_stop_words(linha_temp)
    linha_temp = util.remover_numeros_romanos(linha_temp)
    linha_temp = util.remover_numeros_extenso(linha_temp)
    linha_temp = util.remover_numeros_ordinais(linha_temp)
  
    return re.split(" +", linha_temp)
  
# função que adiciona o texto tratado no grafo
  def adicionar_grafo(self,lista_palavras, graph: Grafo):
    for index in range(1,len(lista_palavras)):
      # se palavra está no grafo:
      if not graph.find_vertice(lista_palavras[index - 1]):
        # se for a primeira palavra adiciona-la no grafo
        if index - 1 == 0:
          graph.add_vertice(lista_palavras[index - 1])
        # se nao for a primeira palavra da lista
        else:
          # adicionar a palavra no grafo e fazer uma conexão de aresta com a última palavra
          graph.add_vertice(lista_palavras[index - 1])
          graph.add_aresta(graph.find_vertice(lista_palavras[index - 1]),graph.find_vertice(lista_palavras[index]))
      # se a palavra nao está no grafo
      else:
        graph.add_aresta(lista_palavras[index - 1],lista_palavras[index])

  def gerar(self):
    for nome_texto in self.textos:
      grafo = Grafo()
    
      with open(f"textos/{nome_texto}", "r", encoding="ISO-8859-1") as f:
        # le o arquivo e armazena em linha
        for line in f.readlines():
          self.adicionar_grafo(self.execucao_linha(line), grafo)
    
    print(grafo)