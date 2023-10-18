from vertice import Vertice


class Aresta():

  def __init__(self, x: Vertice, y: Vertice):
    self.x = x
    self.y = y
    self.peso = 1

  def addPeso(self) -> None:
    self.peso += 1

  def minusPeso(self) -> None:
    if self.peso != 0: self.peso -= 1

  def __hash__(self) -> int:
    return hash((self.x, self.y))

  def __eq__(self, obj: object) -> bool:
    return isinstance(obj, Aresta) and self.x == obj.x and self.y == obj.y
