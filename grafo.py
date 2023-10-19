from vertice import Vertice
from aresta import Aresta
import os


class Grafo():

  def __init__(self) -> None:
    self.lista_vertices = []
    self.num_vertices = 0

  def __str__(self) -> str:

    if len(self.lista_vertices) == 0:
      os.system("cls")
      return "----- GRAFO VAZIO -----"

    final = ""

    for vertice in self.lista_vertices:
      final += f"Vertice {vertice.id} -> {vertice.adjacentes if len(vertice.adjacentes) > 0 else '-- SEM ARESTAS --'}\n"

    return final

  def add_vertice(self, valor: int) -> None:
    vertice = Vertice(valor)
    self.lista_vertices.append(vertice)
    self.num_vertices += 1

  def remove_vertice(self, vertice_x: int) -> None:
    for vertice in self.lista_vertices:
      if vertice.id == vertice_x:
        self.lista_vertices.remove(vertice)
        self.num_vertices -= 1
      else:
        vertice.delete_adjacente(vertice_x)

  def add_aresta(self, vertice_x: Vertice, vertice_y: Vertice) -> None:
    for vertice in self.lista_vertices:
      if vertice.id == vertice_x:
        vertice.add_adjacente(vertice_y)
      if vertice.id == vertice_y:
        vertice.add_adjacente(vertice_x)

  def remove_aresta(self, vertice_x: Vertice, vertice_y: Vertice) -> None:
    for vertice in self.lista_vertices:
      if vertice.id == vertice_x:
        vertice.remove_adjacente(vertice_y)
      if vertice.id == vertice_y:
        vertice.remove_adjacente(vertice_x)

  def find_aresta(self, vertice_x: Vertice, vertice_y: Vertice) -> bool:
    aresta = Aresta(vertice_x, vertice_y)

    for vertice in self.lista_vertices:
      if vertice.find_adjacente(aresta): return True

    return False
