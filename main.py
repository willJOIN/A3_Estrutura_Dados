import os
import random as rd

import dash_cytoscape as cyto
from dash import Dash, Input, Output, callback, html

from geral.avaliador import avaliar
from geral.tokenization import Tokens
from modelos.artigo import Artigo
from modelos.autor_coautor import AutorCoautor

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

    pesos_vertices = {}

    for autor, valores in coautoria.items():
        peso_vertice = valores["peso"]
        coautores = valores["coautores"]

        if autor not in nodes:
            nodes.append(autor)

        pesos_vertices[autor] = peso_vertice

        for coautor in coautores:
            nome_coautor = coautor["nome"]
            peso_aresta = coautor["peso"]

            if nome_coautor not in nodes:
                nodes.append(nome_coautor)

            autor_coautor = AutorCoautor(
                autor.lower().replace(" ", "_"),
                nome_coautor.lower().replace(" ", "_"),
                peso_aresta,
            )

            edges.append(autor_coautor)

    nodes = [
        {
            "data": {"id": short, "label": label},
            "classes": short,
        }
        for short, label in [
            (autor.lower().replace(" ", "_"), autor) for autor in nodes
        ]
    ]

    edges = [
        {"data": {"source": source, "label": label, "target": target, "size": label}}
        for source, target, label in [
            (aresta.autor, aresta.coautor, aresta.peso_aresta) for aresta in edges
        ]
    ]

    edges_repetidos = {}

    for idx, edge in enumerate(edges):
        autor_coautor = AutorCoautor(
            edge["data"]["source"], edge["data"]["target"], int(edge["data"]["label"])
        )

        if autor_coautor not in edges_repetidos:
            edges_repetidos[autor_coautor] = [idx, autor_coautor.peso_aresta]

        else:
            if autor_coautor.peso_aresta > edges_repetidos[autor_coautor][1]:
                edges[edges_repetidos[autor_coautor][0]]["data"]["label"] = str(
                    autor_coautor.peso_aresta
                )
                edges_repetidos[autor_coautor] = [idx, autor_coautor.peso_aresta]
            else:
                edges[idx]["data"]["label"] = str(edges_repetidos[autor_coautor][1])

    default_stylesheet = [
        {
            "selector": "node",
            "style": {
                "label": "data(label)",
            },
        },
        {
            "selector": "edge",
            "style": {
                "line-color": "#000000",
                "width": "data(size)",
                "label": "data(label)",
                "color": "red",
                "fontWeight": "bold",
            },
        },
    ]

    stylesheet = [
        {
            "selector": f".{node_id}",
            "style": {
                "background-color": "#{:06x}".format(rd.randint(0, 0xFFFFFF)),
                "border-width": "2",
                "width": f"{3.5 * pesos_vertices[node_id.replace('_',' ').upper()] + 30}px",
                "height": f"{3.5 * pesos_vertices[node_id.replace('_',' ').upper()] + 30}px",
            },
        }
        for node_id in [(autor["classes"]) for autor in nodes]
    ]

    stylesheet.extend(default_stylesheet)

    buttons_style = {"width":"8rem","height":"3rem"}

    elements = nodes + edges

    app.layout = html.Div(
        [
            html.Div(
                "Grafo de Coautoria",
                style={"margin": "20px","fontWeight":"bold","fontSize":"2rem"},
            ),
            html.Div(
                [
                    cyto.Cytoscape(
                        id="cytoscape-callbacks-1",
                        elements=elements,
                        style={"width": "100%", "height": "45rem"},
                        stylesheet=stylesheet,
                        layout={"name": "breadthfirst"},
                    ),
                    cyto.Cytoscape(
                        id="cytoscape-callbacks-2",
                        elements=elements,
                        style={"display": "none", "width": "100%", "height": "700px"},
                        stylesheet=stylesheet,
                        layout={"name": "preset"},
                    ),
                ],
                style={
                    "width": "95%",
                    "border": "2px solid black",
                    "borderRadius": "10px",
                    "marginTop":"-2rem"
                },
            ),
            html.Div(
                [
                    html.Button("Anterior", id="button_1",style=buttons_style),
                    html.Button("Próxima", id="button_2",style=buttons_style),
                ],
                style={
                    "width": "100%",
                    "display": "flex",
                    "justifyContent": "center",
                    "gap":"2rem"
                },
            ),
            # html.P(id="cytoscape-mouseoverNodeData-output"),
        ],
        style={
            "display": "flex",
            "flexDirection": "column",
            "alignItems": "center",
            "gap": "2rem",
        },
    )

    # for i in range(1, 2):

    #     @callback(
    #         Output("cytoscape-mouseoverNodeData-output", "children"),
    #         Input(f"cytoscape-callbacks-{i}", "mouseoverNodeData"),
    #     )
    #     def displayTapNodeData(data):
    #         if data:
    #             return "You recently hovered over the city: " + data["label"]

    app.run_server(debug=True)
