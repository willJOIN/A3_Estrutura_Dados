from aresta import Aresta


class Vertice:
    def __init__(self, id):
        self.peso = 1
        self.id = id
        self.adjacentes: list[Aresta] = []

    def __str__(self) -> str:
        return f"Vertice {self.id} -> {self.adjacentes if len(self.adjacentes) > 0 else '-- SEM ARESTAS --'}\n"

    def __repr__(self):
        return str(self)

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, obj: object) -> bool:
        return isinstance(obj, Vertice) and self.id == obj.id

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
