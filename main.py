import os

from dash import Dash

from geral.avaliador import avaliar
from geral.grafico import plotar_coautoria, plotar_topicos_relevantes
from geral.tokenization import Tokens
from modelos.artigo import Artigo

app = Dash(__name__)
app.title = "A3 Análise e Est. Dados"

def atividade_topicos_relevantes(avaliar=False):
    textos = sorted(
        os.listdir("textos/atividade1/"),
        key=lambda item: int(item.replace("arq_", "").replace(".txt", "")),
    )

    tokens = Tokens(textos=textos, nome_pasta_arquivos="atividade1")

    if avaliar:
        avaliar(tokens.resultado)
        return

    print(tokens)

    return tokens


def atividade_coautoria():
    textos = sorted(
        os.listdir("textos/atividade2/"),
        key=lambda item: int(item.replace("artigo_", "").replace(".txt", "")),
    )

    artigos = [Artigo(texto) for texto in textos]
    tokens = Tokens(textos=textos, nome_pasta_arquivos="atividade2", artigos=artigos)

    return tokens.grafos[0].get_lista_coautoria()


if __name__ == "__main__":

    # user_input = input('Por favor, insira o número da atividade que você deseja executar:\n1 - Tópicos\n2 - Coautoria')
    # if '1' in user_input:
    #   atividade_topicos_relevantes()
    # elif '2' in user_input:
    #   atividade_coautoria()

    # plotar_coautoria(app, atividade_coautoria())
    
    plotar_topicos_relevantes(app, atividade_topicos_relevantes())
