import os
from avaliador import avaliar
from tokenization import Topicos


if __name__ == "__main__":
  textos = sorted(
      os.listdir("textos/"),
      key=lambda item: int(item.replace("arq_", "").replace(".txt", "")))
  tokens_arquivos = Topicos(textos) # Para testar 1 arquivo, textos[:1]
  avaliar(tokens_arquivos.topicos_tokens)
