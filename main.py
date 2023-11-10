import os
from avaliador import avaliar
from tokenization import Topicos
from grafo import Grafo
from vertice import Vertice

if __name__ == "__main__":
  textos = sorted(
      os.listdir("textos/"),
      key=lambda item: int(item.replace("arq_", "").replace(".txt", "")))
  
  topicos = Topicos(textos) 

  print(topicos)
  avaliar(topicos.arquivos_topicos)
