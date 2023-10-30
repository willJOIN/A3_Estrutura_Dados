from vertice import Vertice
from aresta import Aresta
import os


class Grafo():

  def __init__(self) -> None:
    self.lista_vertices:list[Vertice] = []
    self.num_vertices = 0

  def __str__(self) -> str:

    if len(self.lista_vertices) == 0:
      os.system("cls")
      return "----- GRAFO VAZIO -----"

    final = ""

    for vertice in self.lista_vertices:
      final += str(vertice)

    return final

  def add_vertice(self, valor: int) -> Vertice:
    vertice = Vertice(valor)

    if vertice not in self.lista_vertices:
      self.lista_vertices.append(vertice)
      self.num_vertices += 1

    return vertice

  def remove_vertice(self, vertice_x: int) -> None:
    for vertice in self.lista_vertices:
      if vertice.id == vertice_x:
        self.lista_vertices.remove(vertice)
        self.num_vertices -= 1
      else:
        vertice.delete_adjacente(vertice_x)

  def add_aresta(self, vertice_x: Vertice, vertice_y: Vertice) -> None:

    for vertice in self.lista_vertices:
      if vertice.id == vertice_x.id:
        vertice.add_adjacente(vertice_y)
      if vertice.id == vertice_y.id:
        vertice.add_adjacente(vertice_x)

  def remove_aresta(self, vertice_x: Vertice, vertice_y: Vertice) -> None:
    for vertice in self.lista_vertices:
      if vertice.id == vertice_x.id:
        vertice.remove_adjacente(vertice_y)
      if vertice.id == vertice_y.id:
        vertice.remove_adjacente(vertice_x)

  def find_aresta(self, vertice_x: Vertice, vertice_y: Vertice) -> bool:
    aresta = Aresta(vertice_x, vertice_y)

    for vertice in self.lista_vertices:
      if vertice.find_adjacente(aresta): return True

    return False
