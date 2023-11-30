import os
import random as rd

import dash_cytoscape as cyto
from dash import Dash, Input, Output, callback, html

from geral.avaliador import avaliar
from geral.tokenization import Tokens
from modelos.artigo import Artigo

app = Dash(__name__)


def atividade_topicos_relevantes():
    textos = sorted(
        os.listdir("textos/atividade1/"),
        key=lambda item: int(item.replace("arq_", "").replace(".txt", "")),
    )

    tokens = Tokens(textos=textos, nome_pasta_arquivos="atividade1")

    print(tokens)
    avaliar(tokens.resultado)


def atividade_coautoria():
    textos = sorted(
        os.listdir("textos/atividade2/"),
        key=lambda item: int(item.replace("artigo_", "").replace(".txt", "")),
    )

    artigos = [Artigo(texto) for texto in textos]
    tokens = Tokens(textos=textos, nome_pasta_arquivos="atividade2", artigos=artigos)

    return tokens.grafos[0].get_lista_coautoria()

    # print(tokens.grafos[0])
    # print(artigos[0])
    # avaliar(tokens.resultado)


if __name__ == "__main__":
    # user_input = input('Por favor, insira o número da atividade que você deseja executar:\n1 - Tópicos\n2 - Coautoria')
    # if '1' in user_input:
    #   atividade_topicos_relevantes()
    # elif '2' in user_input:
    #   atividade_coautoria()

    coautoria = atividade_coautoria()

    nodes = []

    edges = []

    pesos_arestas = {}
    pesos_vertices = {}

    for autor, valores in coautoria.items():
        peso_vertice = valores["peso"]
        coautores = valores["coautores"]

        if autor not in nodes:
            nodes.append(autor)

        pesos_vertices[autor] = peso_vertice

        for coautor in coautores:
            nome_coautor = coautor["nome"]
            peso_aresta = coautor["peso"]  # possivelmente usado pra peso da aresta

            pesos_arestas[autor] = peso_aresta

            if coautor not in nodes:
                nodes.append(nome_coautor)
                edges.append((autor.lower(), nome_coautor.lower()))

    nodes = [
        {
            "data": {"id": short.replace(" ", "_"), "label": label, "size": size},
            "classes": short.replace(" ", "_"),
        }
        for short, label, size in [
            (autor.lower(), autor, 3.5 * pesos_vertices[autor] + 50) for autor in nodes
        ]
    ]

    edges = [
        {"data": {"source": source, "label": label, "target": target}}
        for source, label, target in [
            (
                aresta[0].replace(" ", "_"),
                str(pesos_arestas[autor]),
                aresta[1].replace(" ", "_"),
            )
            for aresta in edges
        ]
    ]

    default_stylesheet = [
        {
            "selector": f".{node_id}",
            "style": {
                "background-color": "#{:06x}".format(rd.randint(0, 0xFFFFFF)),
                "border-width": "2",
                "width": "55px",
                "height": "55px",
            },
        }
        for node_id in [(autor["classes"]) for autor in nodes]
    ]

    stylesheet = [
        {
            "selector": "node",
            "style": {"label": "data(label)"},
        },
        {
            "selector": "edge",
            "style": {"line-color": "#000000", "width": "1px", "label": "data(label)"},
        },
    ]

    stylesheet.extend(default_stylesheet)

    elements = nodes + edges

    app.layout = html.Div(
        [
            html.Div(
                [
                    cyto.Cytoscape(
                        id="cytoscape-callbacks-1",
                        elements=elements,
                        style={"width": "100%", "height": "70rem"},
                        stylesheet=stylesheet,
                        layout={"name": "breadthfirst"},
                    ),
                    cyto.Cytoscape(
                        id="cytoscape-callbacks-2",
                        elements=elements,
                        style={"display": "none", "width": "100%", "height": "800px"},
                        stylesheet=stylesheet,
                        layout={"name": "preset"},
                    ),
                ]
            ),
            html.Div(
                [
                    html.Button("Botao", id="button_1"),
                    html.Div(
                        "Grafo de Coautoria",
                        style={"margin": "20px"},
                    ),
                ],
                style={
                    "width": "100%",
                    "display": "flex",
                    "flex-direction": "column",
                    "align-items": "center",
                },
            ),
        ]
    )

    # layouts disponiveis
    # preset
    # random
    # grid
    # circle
    # concentric
    # breadthfirst
    # cose

    # @callback(Input('cytoscape-event-callbacks-1', 'tapNodeData'))
    # def displayTapNodeData(data):
    #     return json.dumps(data, indent=2)

    app.run_server(debug=True)
