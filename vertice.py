from aresta import Aresta


class Vertice:

  def __init__(self, id):
    self.id = id
    self.adjacentes: list[Aresta] = []

  def add_adjacente(self, adjacente):
    aresta = Aresta(self, adjacente)
    
    if adjacente not in self.adjacentes:
      self.adjacentes.append(aresta)
    else:
      self.adjacentes[self.adjacentes.index(aresta)].addPeso()

  def remove_adjacente(self, adjacente):
    if adjacente in self.adjacentes:
      if adjacente.peso >= 0: adjacente.minusPeso()
      else: self.adjacentes.remove(aresta)

  def find_adjacente(self, adjacente):
    return adjacente in self.adjacentes
