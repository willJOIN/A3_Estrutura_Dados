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

    colors = ["red"]

    # ('la', 'Los Angeles', 34.03, -118.25),
    # ('nyc', 'New York', 40.71, -74),
    # ('to', 'Toronto', 43.65, -79.38),
    # ('mtl', 'Montreal', 45.50, -73.57),
    # ('van', 'Vancouver', 49.28, -123.12),
    # ('chi', 'Chicago', 41.88, -87.63),
    # ('bos', 'Boston', 42.36, -71.06),
    # ('hou', 'Houston', 29.76, -95.37)

    nodes = [
        # {
        #     'data': {'id': short, 'label': label},
        #     'position': {'x': 20 * lat, 'y': -20 * long}
        # }
        # for short, label, long, lat in [
        #     (autor.lower(),autor,rd.uniform(28,60),rd.uniform(-70,-120)) for autor in coautoria.keys())
        # ]
    ]

    edges = [
        # {'data': {'source': source, 'target': target}}
        # for source, target in [
        # #   (autor,valores["coautores"][0]) for autor,valores in coautoria.items()
        # ]
    ]

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

            if coautor not in nodes:
                nodes.append(nome_coautor)
                edges.append((autor.lower(), nome_coautor.lower()))

    nodes = [
        {
            "data": {"id": short, "label": label, "size": size},
        }
        for short, label, size in [
            (autor.lower(), autor, pesos_vertices[autor]) for autor in nodes
        ]
    ]

    edges = [
        {"data": {"source": source, "target": target}}
        for source, target in [(aresta[0], aresta[1]) for aresta in edges]
    ]

    # ('van', 'la'),
    # ('la', 'chi'),
    # ('hou', 'chi'),
    # ('to', 'mtl'),
    # ('mtl', 'bos'),
    # ('nyc', 'bos'),
    # ('to', 'hou'),
    # ('to', 'nyc'),
    # ('la', 'nyc'),
    # ('nyc', 'bos')

    default_stylesheet = [
        {
            "selector": "node",
            "style": {
                "background-color": "#BFD7B5",
                "label": "data(label)",
                "width": "",
                "height": "",
            },
        },
        {"selector": "edge", "style": {"line-color": "#A3C4BC"}},
    ]

    elements = nodes + edges

    app.layout = html.Div(
        [
            html.Div(
                [
                    cyto.Cytoscape(
                        id="cytoscape-callbacks-1",
                        elements=elements,
                        style={"width": "100%", "height": "70rem"},
                        stylesheet=default_stylesheet,
                        layout={"name": "breadthfirst"},
                    ),
                    cyto.Cytoscape(
                        id="cytoscape-callbacks-2",
                        elements=elements,
                        style={"display": "none", "width": "100%", "height": "800px"},
                        stylesheet=default_stylesheet,
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
                style={"width":"100%","display": "flex","flex-direction":"column","align-items": "center"},
            ),
        ]
    )

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
