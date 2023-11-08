import os
from avaliador import avaliar
from tokenization import Topicos
from grafo import Grafo
from vertice import Vertice

if __name__ == "__main__":
  textos = sorted(
      os.listdir("textos/"),
      key=lambda item: int(item.replace("arq_", "").replace(".txt", "")))
  tokens_arquivos = Topicos(textos[:2]) # Pra testar um arquivo, limitar para textos[:1]
  #avaliar(tokens_arquivos.topicos_tokens)
