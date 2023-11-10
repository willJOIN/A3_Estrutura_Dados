import os
from avaliador import avaliar
from tokenization import Topicos
from grafo import Grafo
from vertice import Vertice

if __name__ == "__main__":

# # teste
#   grafo = Grafo()
#   # criar 11 vertices
#   grafo.add_vertice('palavra1')
#   grafo.add_vertice('palavra1')
  
#   grafo.add_vertice('palavra2')
#   grafo.add_vertice('palavra2')

#   grafo.add_vertice('palavra3')
#   grafo.add_vertice('palavra3')
  
#   grafo.add_vertice('palavra4')
#   grafo.add_vertice('palavra4')

#   grafo.add_vertice('palavra5')
#   grafo.add_vertice('palavra5')

#   grafo.add_vertice('palavra6')
#   grafo.add_vertice('palavra6')

#   grafo.add_vertice('palavra7')
#   grafo.add_vertice('palavra7')

#   grafo.add_vertice('palavra8')
#   grafo.add_vertice('palavra11')

#   grafo.add_vertice('palavra9')
#   grafo.add_vertice('palavra9')

#   grafo.add_vertice('palavra10')
#   grafo.add_vertice('palavra10')

#   grafo.add_vertice('palavra11')

#   print(grafo.get_lista_topicos_importantes())

  textos = sorted(
      os.listdir("textos/"),
      key=lambda item: int(item.replace("arq_", "").replace(".txt", "")))
  
  topicos = Topicos(textos) 

  print(topicos)
  #avaliar(topicos.arquivos_topicos)
  
