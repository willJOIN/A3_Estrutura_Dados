from aresta import Aresta
from artigo import Artigo


class Autor:
    def __init__(self, id):
        # nome do autor
        self.id = id
        # quantidade de vezes adicionadas no grafo
        self.peso = 1
        # lista de coautores
        self.adjacentes: list[Aresta] = []
        # lista de artigos
        self.artigos: list[Artigo] = []
        # quantidades de referencia a esse vertice
        self.peso = 1

    def __str__(self) -> str:
        return f"autor:{self.id}"

    def __repr__(self):
        return str(self)

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, obj: object) -> bool:
        return isinstance(obj, Autor) and self.id == obj.id

    def add_artigo(self, titulo, texto, coautor):
        art = Artigo(titulo, texto, self.id, coautor)
        if art not in self.artigos:
            self.artigos.append((titulo, texto, coautor))
        else:
            raise Warning(
                f"artigo ja está na lista de artigos desse autor - autor: {self.id}"
            )

    def add_adjacente(self, adjacente):
        aresta = Aresta(self, adjacente)

        if aresta not in self.adjacentes:
            self.adjacentes.append(aresta)
        else:
            self.adjacentes[self.adjacentes.index(aresta)].addPeso()

    def remove_adjacente(self, adjacente):
        if adjacente in self.adjacentes:
            aresta = self.adjacentes[self.adjacentes.index(adjacente)]

            if aresta.peso >= 0:
                aresta.minusPeso()

    def delete_adjacente(self, adjacente):
        if adjacente in self.adjacentes:
            aresta = self.adjacentes[self.adjacentes.index(adjacente)]

            self.adjacentes.remove(aresta)

    def find_adjacente(self, adjacente: Aresta):
        return adjacente in self.adjacentes

    def increment_peso(self) -> None:
        self.peso += 1
