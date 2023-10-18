from vertice import Vertice
from aresta import Aresta

class Grafo():
  def __init__(self) -> None:
    self.lista_vertices = []

  def add_vertice(self, vertice:int) -> None:
    new_vertice = Vertice(vertice)
    self.lista_vertices.append(new_vertice)

  def remove_vertice(self, vertice_x:int) -> None:
    for vertice in self.lista_vertices:
      if vertice.id == vertice_x:
        self.lista_vertices.remove(vertice)
      else:
        vertice.remove_adjacente(vertice_x)
    
  def add_aresta(self, vertice_x:Vertice, vertice_y:Vertice) -> None:
    for vertice in self.lista_vertices:
      if vertice.id == vertice_x:
        vertice.add_adjacente(vertice_y)
      if vertice.id == vertice_y:
        vertice.add_adjacente(vertice_x)

  def remove_aresta(self, vertice_x:int, vertice_y:int) -> None:
    for vertice in self.lista_vertices:
      if vertice.id == vertice_x:
        vertice.remove_adjacente(vertice_y)
      if vertice.id == vertice_y:
        vertice.remove_adjacente(vertice_x)

  def verificar_aresta(self, vertice_x:int, vertice_y:int) -> None:
    for vertice in self.lista_vertices:
      if vertice.id == vertice_x:
        if vertice.verificar_adjacente(vertice_y):
          return True
      if verttice.id == vertice_y:
          if vertice.verificar_adjacente(vertice_x):
            return True
    return False
