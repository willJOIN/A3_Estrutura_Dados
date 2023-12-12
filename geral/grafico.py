import random as rd

import dash_cytoscape as cyto
from dash import Input, Output, html

from modelos.autor_coautor import SourceTarget

# pior caso: O(mno) -> o big O depende do numero de grafos (m), dos vertices em cada grafo (n) e das arestas de cada vertice(o)
# melhor caso: Ω(mno)
def plotar_topicos_relevantes(app, tokens):
    graficos = []

    textos = [texto.replace(".", "_") for texto in tokens.textos]

    for idx, grafo in enumerate(tokens.grafos):
        texto = textos[idx]

        nodes = []
        edges = []
        pesos_vertices = {}

        for vertice in grafo.lista_vertices:
            peso_vertice = vertice.peso

            if vertice.id not in nodes:
                nodes.append(vertice.id)
                pesos_vertices[f"{vertice.id.lower()}_{texto}"] = peso_vertice

            for aresta in vertice.adjacentes:
                peso_aresta = aresta.peso

                if aresta.y.id not in nodes:
                    nodes.append(aresta.y.id)
                    pesos_vertices[f"{aresta.y.id.lower()}_{texto}"] = aresta.y.peso

                edges.append(
                    [
                        f"{vertice.id.lower()}_{texto}",
                        f"{aresta.y.id.lower()}_{texto}",
                        peso_aresta,
                    ]
                )

        nodes = [
            {
                "data": {"id": short, "label": label},
                "classes": short,
            }
            for short, label in [
                (f"{vertice.lower()}_{texto}", vertice) for vertice in nodes
            ]
        ]

        edges = [
            {
                "data": {
                    "source": source,
                    "label": label,
                    "target": target,
                    "size": label,
                }
            }
            for source, target, label in [
                (aresta[0], aresta[1], aresta[2]) for aresta in edges
            ]
        ]

        edges_repetidos = {}

        for idx, edge in enumerate(edges):
            source_target = SourceTarget(
                edge["data"]["source"],
                edge["data"]["target"],
                int(edge["data"]["label"]),
            )

            if source_target not in edges_repetidos:
                edges_repetidos[source_target] = [idx, source_target.peso_aresta]

            else:
                if source_target.peso_aresta > edges_repetidos[source_target][1]:
                    edges[edges_repetidos[source_target][0]]["data"]["label"] = str(
                        source_target.peso_aresta
                    )
                    edges_repetidos[source_target] = [idx, source_target.peso_aresta]
                else:
                    edges[idx]["data"]["label"] = str(edges_repetidos[source_target][1])

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
                    "width": f"{3.5 * pesos_vertices[node_id] + 30}px",
                    "height": f"{3.5 * pesos_vertices[node_id] + 30}px",
                },
            }
            for node_id in [(vertice["classes"]) for vertice in nodes]
        ]

        stylesheet.extend(default_stylesheet)

        buttons_style = {"width": "8rem", "height": "3rem"}

        elements = nodes + edges

        graficos.append(
            cyto.Cytoscape(
                id=f"grafo-{texto}",
                elements=elements,
                style={
                    "width": "100%",
                    "height": "45rem",
                    "display": f"{'none' if len(graficos) > 0 else 'block'}",
                },
                stylesheet=stylesheet,
                layout={"name": "breadthfirst"},
            )
        )

    app.layout = html.Div(
        [
            html.Div(
                [
                    html.Span(
                        f"Grafo de Tópicos: Arquivo '{tokens.textos[0]}'",
                        id="grafo-titulo",
                        style={
                            "marginTop": "20px",
                            "fontWeight": "bold",
                            "fontSize": "2rem",
                        },
                    ),
                    html.Span(
                        f"* Tópicos Importantes * '{tokens.resultado[tokens.textos[0]]}'",
                        id="grafo-topicos",
                        style={"fontStyle": "italic", "fontSize": "1rem"},
                    ),
                ],
                style={
                    "marginBottom": "20px",
                    "display": "flex",
                    "flexDirection": "column",
                    "gap": "1rem",
                    "alignItems": "center",
                },
            ),
            html.Div(
                graficos,
                style={
                    "width": "95%",
                    "border": "2px solid black",
                    "borderRadius": "10px",
                    "marginTop": "-2rem",
                },
            ),
            html.Div(
                [
                    html.Button("Anterior", id="button_1", style=buttons_style),
                    html.Button("Próxima", id="button_2", style=buttons_style),
                    html.Div(id="hidden-div", style={"display": "none"}),
                ],
                style={
                    "width": "100%",
                    "display": "flex",
                    "justifyContent": "center",
                    "gap": "2rem",
                },
            ),
        ],
        style={
            "display": "flex",
            "flexDirection": "column",
            "alignItems": "center",
            "gap": "1.5rem",
        },
    )

    resultado = {chave: str(valor) for chave, valor in tokens.resultado.items()}

    app.clientside_callback(
        "function() {\n"
        + f"  const first = 'grafo-{textos[0]}'\n"
        + f"  const final = 'grafo-{textos[-1]}'\n"
        + f"  const arquivosTopicos = {resultado}\n"
        + """
            console.log(arquivosTopicos)
            const ctx = window.dash_clientside.callback_context
            const triggered_id = ctx.triggered[0].prop_id
            
            if ("button_1.n_clicks" == triggered_id) {
                if (grafoAtual(idxGrafoAtual) != first) {
                    document.getElementById(grafoAtual(idxGrafoAtual)).style['display'] = 'none'
                    idxGrafoAtual -= 1
                    document.getElementById(grafoAtual(idxGrafoAtual)).style['display'] = 'block'
                }
            }

            else if ("button_2.n_clicks" == triggered_id) {
                if (grafoAtual(idxGrafoAtual) != final) {
                    document.getElementById(grafoAtual(idxGrafoAtual)).style['display'] = 'none'
                    idxGrafoAtual += 1
                    document.getElementById(grafoAtual(idxGrafoAtual)).style['display'] = 'block'

                }
            }

            const arquivo = `arq_${idxGrafoAtual}.txt`

            document.getElementById("grafo-topicos").innerText = `* Tópicos Importantes * '${arquivosTopicos[arquivo]}'`

            return `Grafo de Tópicos: Arquivo ${grafoAtual(idxGrafoAtual).replace('grafo-','')}`
        }""",
        Output("grafo-titulo", "children"),
        [Input("button_1", "n_clicks"), Input("button_2", "n_clicks")],
        prevent_initial_call=True,
    )

    app.run_server(debug=True, use_reloader=False)

# pior caso: O(mn)
# melhor caso: Ω(mn)
def plotar_coautoria(app, coautoria):
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

            autor_coautor = SourceTarget(
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
        autor_coautor = SourceTarget(
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

    elements = nodes + edges

    resultado = [
        f"({chave},{len(valor['coautores'])})" for chave, valor in coautoria.items()
    ][:20]

    app.layout = html.Div(
        [
            html.Div(
                [
                    html.Div(
                        "Grafo de Coautoria",
                        style={
                            "margin": "20px",
                            "fontWeight": "bold",
                            "fontSize": "2rem",
                        },
                    ),
                    html.Span(
                        f"* Coautoria * '{resultado}'",
                        id="grafo-topicos",
                        style={
                            "width": "90%",
                            "fontStyle": "italic",
                            "fontSize": "1rem",
                        },
                    ),
                ],
                style={
                    "marginBottom": "20px",
                    "display": "flex",
                    "flexDirection": "column",
                    "gap": "1rem",
                    "alignItems": "center",
                },
            ),
            html.Div(
                [
                    cyto.Cytoscape(
                        id="grafo-1",
                        elements=elements,
                        style={"width": "100%", "height": "45rem"},
                        stylesheet=stylesheet,
                        layout={"name": "breadthfirst"},
                    ),
                ],
                style={
                    "width": "95%",
                    "border": "2px solid black",
                    "borderRadius": "10px",
                    "marginTop": "-2rem",
                },
            ),
        ],
        style={
            "display": "flex",
            "flexDirection": "column",
            "alignItems": "center",
            "gap": "2rem",
        },
    )

    app.run_server(debug=True, use_reloader=False)
