import os
from avaliador import avaliar
from tokenization import Topicos


if __name__ == "__main__":
  textos = sorted(
      os.listdir("textos/"),
      key=lambda item: int(item.replace("arq_", "").replace(".txt", "")))
  tokens_arquivos = Topicos(textos[:1]) # todo tirar limite
  avaliar(tokens_arquivos.topicos_tokens)
