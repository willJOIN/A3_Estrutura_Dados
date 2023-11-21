import os
from avaliador import avaliar
from tokenization import Tokens
from grafo import Grafo
from vertice import Vertice

if __name__ == "__main__":
    textos = sorted(
        os.listdir("textos/atividade1/"),
        key=lambda item: int(item.replace("arq_", "").replace(".txt", "")),
    )

    tokens = Tokens(textos,"atividade1")

    print(tokens)
    avaliar(tokens.resultado)
