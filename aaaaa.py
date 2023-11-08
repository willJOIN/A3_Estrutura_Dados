import unicodedata
from grafo import Grafo
from vertice import Vertice
from aresta import Aresta
import re


def tokenization(grafo):

  #cria dicionario vazio
  tokens = {}
  vertices = []

    
  # função que adiciona os 10 vertices mais pesados
  
  

  #abre 1 arquivo de texto no modo leitura f
  with open("texto.txt", 'r', encoding="ISO-8859-1") as f:
    #le o arquivo e armazena em linha
    for line in f.readlines():
      for token in exec(line):
        vertices.append(token)
        if tokens.get(token):
          tokens[token] += 1
        else:
          tokens[token] = 1
          
        # if grafo.lista_vertices.get(token):
        #   if grafo.lista_vertices.get(token).adjacentes.get()
  
  print(tokens)

def exec(linha):

  #substutito todas os chars com acento pelos sem acento correspondente
  def substituir_acentos(linha_com_acentos):
    return linha_com_acentos.translate(criar_tabela_substituicao())
  
  def remover_numeros_extenso(linha_numero_extenso):

        linha = linha_numero_extenso.split(" ")
        numeros_extenso = []

        with open("numeros_extensos.txt", "r") as f:
            numeros_extenso = f.readlines()

        numeros_extenso = [
            numero.replace("\n", "").strip() for numero in numeros_extenso
        ]

        idx_a_remover = []

        for idx in range(len(linha)):
          if linha[idx] in numeros_extenso:
              idx_a_remover.append(idx)

        for idx in idx_a_remover:
          linha.remove(linha[idx])

        return " ".join(linha)
  
  def remover_stop_words(linha_crua):

    linha = linha_crua.strip()

    stop_words = []

    with open("stop_words.txt", "r") as f:
      for line in f.readlines():
        for stop_word in line.split(", "):
          stop_words.append(substituir_acentos(stop_word.upper()))

    stop_words = list(set(stop_words))

    linha = " ".join(
        [palavra.strip() for palavra in re.split(" +",linha) if palavra.strip() not in stop_words])

    return linha

  
  def limpar_linha(linha_com_espacos):
    especiais = "°ªº!@#$%¨&*=+-_()[]{}´`~^:;.,/?\|'"
    numeros = [str(valor) for valor in range(0, 10)]

    linha = linha_com_espacos

    for especial in especiais:
      linha = linha.replace(especial, "")

    for numero in numeros:
      linha = linha.replace(numero, "")

    return linha.replace("\n", "").upper()

  return re.split(" +",remover_numeros_extenso(remover_stop_words(substituir_acentos(limpar_linha(linha)))))


def criar_tabela_substituicao():
  chars_acentuados = "ÁÉÍÓÚÀÈÌÒÙÃẼĨÕŨÂÊÎÔÛÄËÏÖÜÇ"
  chars = "AEIOUAEIOUAEIOUAEIOUAEIOUC"

  #cria um "mapa" sendo o char com acento a value e o seu correspondente a chave
  tabela = {
      ord(acento): ord(sem_acento)
      for acento, sem_acento in zip(chars_acentuados, chars)
  }
  return tabela


if __name__ == "__main__":

  thisdict = {
    "primeira_palavra": 1,
    "segunda": 2,
    "sétima": 7,
    "quarta": 4
  }
  def dez_mais_pesados(dic):
  
    for i in sorted(thisdict, key = thisdict.get):
      print(i, thisdict[i])

  # grafo = Grafo()
  # v1 = grafo.add_vertice(0)
  # v2 = grafo.add_vertice(1)
  # v3 = grafo.add_vertice(0)
  # v4 = Vertice(2)

  # grafo.add_aresta(v1, v2)
  # grafo.add_aresta(v1, v2)

  # tokenization(grafo)




#strip()  tira os espaços em branco do começo e final de uma PALAVRA
#replace substitui todas as ocorrencias do primeiro parametro pro segundo
#re.spit coloca as palavras de uma string em uma lista dado determinado padrao de separacao
# join

#limpar linha:remove todos os caracteres especiais, numeros e espaços
#substituir acentos: substitui todas as letras com acento de uma dada string pela sua correspondente sem acento
#remover stop words: devolve uma string sem as stopwords

# txt = 'meu nome e vinicius  '
# ex = 'esse é meu exemplo de texto \nagora estou escrevendo o segundo paragrafo \n\nesse é o quarto'

# with open('texto.txt', 'r',encoding="ISO-8859-1") as f:
#     i = 1
#     for paragrafo in f.readlines():
#       print(i, paragrafo)
#       i += 1
# print(re.split(' +',txt))

# thisdict = {
#   "brand": "Ford",
#   "model": "Mustang",
#   "year": 1964
# }

# for x in thisdict:
#   print(thisdict[x]