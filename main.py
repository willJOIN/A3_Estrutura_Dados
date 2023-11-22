import os
from avaliador import avaliar
from tokenization import Tokens
from grafo import Grafo
from vertice import Vertice
from artigo import Artigo

if __name__ == "__main__":
    textos = sorted(
        os.listdir("textos/atividade2/"),
        key=lambda item: int(item.replace("artigo_", "").replace(".txt", "")),
    )

    artigos = [ Artigo(texto) for texto in textos ]
    
    tokens = Tokens(textos,"atividade2")

    print(tokens)
    avaliar(tokens.resultado)
