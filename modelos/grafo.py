from geral.util import limpar_terminal

class Aresta:
    # pior caso: O(1)
    # melhor caso: Ω(1)  
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.peso = 1

    # pior caso: O(1)
    # melhor caso: Ω(1)  
    def __str__(self) -> str:
        return f"V({self.x.id}) - V({self.y.id}):{self.peso}"

    # pior caso: O(1)
    # melhor caso: Ω(1)  
    def __repr__(self):
        return str(self)

    # pior caso: O(1)
    # melhor caso: Ω(1)  
    def __hash__(self) -> int:
        return hash((self.x, self.y))

    # pior caso: O(1)
    # melhor caso: Ω(1)  
    def __eq__(self, obj: object) -> bool:
        return isinstance(obj, Aresta) and self.x == obj.x and self.y == obj.y

    # pior caso: O(1)
    # melhor caso: Ω(1)  
    def addPeso(self) -> None:
        self.peso += 1

    # pior caso: O(1)
    # melhor caso: Ω(1)  
    def minusPeso(self) -> None:
        if self.peso != 0:
            self.peso -= 1

    # pior caso: O(1)
    # melhor caso: Ω(1)  
    def getVerticeFinal(self):
        return self.y

class Vertice:
    # pior caso: O(1)
    # melhor caso: Ω(1)  
    def __init__(self, id):
        self.peso = 1
        self.id = id
        self.adjacentes: list[Aresta] = []

    # pior caso: O(1)
    # melhor caso: Ω(1)  
    def __str__(self) -> str:
        return f"Vertice {self.id} -> {self.adjacentes if len(self.adjacentes) > 0 else '-- SEM ARESTAS --'}\n"

    # pior caso: O(1)
    # melhor caso: Ω(1)  
    def __repr__(self):
        return str(self)

    # pior caso: O(1)
    # melhor caso: Ω(1)  
    def __hash__(self) -> int:
        return hash(self.id)

    # pior caso: O(1)
    # melhor caso: Ω(1)  
    def __eq__(self, obj: object) -> bool:
        return isinstance(obj, Vertice) and self.id == obj.id

    # pior caso: O(1)
    # melhor caso: Ω(1)
    def add_adjacente(self, adjacente):
        aresta = Aresta(self, adjacente)

        if aresta not in self.adjacentes:
            self.adjacentes.append(aresta)
        else:
            self.adjacentes[self.adjacentes.index(aresta)].addPeso()

    # pior caso: O(1)
    # melhor caso: Ω(1)
    def remove_adjacente(self, adjacente):
        if adjacente in self.adjacentes:
            aresta = self.adjacentes[self.adjacentes.index(adjacente)]

            if aresta.peso >= 0:
                aresta.minusPeso()
    # pior caso: O(1)
    # melhor caso: Ω(1)
    def delete_adjacente(self, adjacente):
        if adjacente in self.adjacentes:
            aresta = self.adjacentes[self.adjacentes.index(adjacente)]

            self.adjacentes.remove(aresta)
    # pior caso: O(1)
    # melhor caso: Ω(1)
    def find_adjacente(self, adjacente: Aresta):
        return adjacente in self.adjacentes
    # pior caso: O(1)
    # melhor caso: Ω(1)
    def increment_peso(self) -> None:
        self.peso += 1

class Grafo:
    # pior caso: O(1)
    # melhor caso: Ω(1)
    def __init__(self) -> None:
        self.lista_vertices: list[Vertice] = []
        self.num_vertices = 0

    # pior caso: O(n)
    # melhor caso: Ω(n)
    def __str__(self) -> str:
        if len(self.lista_vertices) == 0:
            limpar_terminal()
            return "----- GRAFO VAZIO -----"

        final = ""

        for vertice in self.lista_vertices:
            final += str(vertice)

        return final

    # pior caso: O(1)
    # melhor caso: Ω(1)
    def add_vertice(self, valor: str) -> Vertice:
        vertice = Vertice(valor)

        if vertice not in self.lista_vertices:
            self.lista_vertices.append(vertice)
            self.num_vertices += 1
        else:
            idx = self.lista_vertices.index(vertice)
            self.lista_vertices[idx].increment_peso()

        return vertice

    # pior caso: O(nm)
    # melhor caso: Ω(nm)
    def remove_vertice(self, vertice_x: str) -> None:
        vertice_remover = Vertice(vertice_x)

        for vertice in self.lista_vertices.copy():
            if vertice == vertice_remover:
                self.lista_vertices.remove(vertice)
                self.num_vertices -= 1
            else:
                # TODO iterar arestas de vertice pra deletar arestas + vertice
                arestas = vertice.adjacentes
                for idx in range(len(arestas)):
                    if arestas[idx].getVerticeFinal() == vertice_remover:
                        vertice.adjacentes.remove(arestas[idx])

    # pior caso: O(n)
    # melhor caso: Ω(n)
    def add_aresta(self, vertice_x: Vertice, vertice_y: Vertice) -> None:
        for vertice in self.lista_vertices:
            if vertice.id == vertice_x.id:
                vertice.add_adjacente(vertice_y)
            if vertice.id == vertice_y.id:
                vertice.add_adjacente(vertice_x)
    
    # pior caso: O(n)
    # melhor caso: Ω(n)
    def remove_aresta(self, vertice_x: Vertice, vertice_y: Vertice) -> None:
        for vertice in self.lista_vertices:
            if vertice.id == vertice_x.id:
                vertice.remove_adjacente(vertice_y)
            if vertice.id == vertice_y.id:
                vertice.remove_adjacente(vertice_x)

    # pior caso: O(n)
    # melhor caso: Ω(1)
    def find_aresta(self, vertice_x: Vertice, vertice_y: Vertice) -> bool:
        aresta = Aresta(vertice_x, vertice_y)

        for vertice in self.lista_vertices:
            if vertice.find_adjacente(aresta):
                return True

        return False

    # pior caso: O(n)
    # melhor caso: Ω(1)
    def find_vertice(self, vertice_id):
        for vertice in self.lista_vertices:
            if vertice.id == vertice_id:
                return vertice

    # pior caso: O(nm)
    # melhor caso: Ω(nm)
    # devolve uma lista dos 10 vertices mais pesados do grafo
    def get_lista_topicos_importantes(self):
        lista_topicos_importantes = []
        vertices = self.lista_vertices

        for idx in range(len(vertices)):
            lista_topicos_importantes.append(vertices[idx])

        palavras_dict = {}

        for vertice in lista_topicos_importantes:
            arestas = sorted(
                vertice.adjacentes, key=lambda item: item.peso, reverse=True
            )

            for aresta in arestas:
                if palavras_dict.get(aresta.y.id):
                    palavras_dict[aresta.y.id] += aresta.peso
                else:
                    palavras_dict[aresta.y.id] = aresta.peso

        lista = sorted(palavras_dict.items(), key=lambda item: item[1], reverse=True)[
            :10
        ]

        return lista

    def get_lista_coautoria(self):
        lista_coautoria = []
        vertices = self.lista_vertices

        for idx in range(len(vertices)):
            lista_coautoria.append(vertices[idx])

        palavras_dict = {}

        for vertice in lista_coautoria:
            arestas = sorted(
                vertice.adjacentes, key=lambda item: item.peso, reverse=True
            )

            for aresta in arestas:
                if palavras_dict.get(vertice.id):
                    
                    palavras_dict[vertice.id]["coautores"].append({"nome":aresta.y.id,"peso":aresta.y.peso})
                else:
                    palavras_dict[vertice.id] = {"coautores":[{"nome":aresta.y.id,"peso":aresta.y.peso}],"peso":aresta.peso}
        
            palavras_dict[vertice.id]["peso"] = len(palavras_dict[vertice.id]["coautores"])
        coautoria = dict(sorted(palavras_dict.items(), key=lambda item: item[1]["peso"], reverse=True))

        return coautoria