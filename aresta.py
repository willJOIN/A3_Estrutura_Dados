class Aresta:
  def __init__(self, x, y):
      self.x = x
      self.y = y
      self.peso = 1

  def __str__(self) -> str:
      return f"V({self.x.id}) - V({self.y.id}):{self.peso}"

  def __repr__(self):
      return str(self)

  def __hash__(self) -> int:
      return hash((self.x, self.y))

  def __eq__(self, obj: object) -> bool:
      return isinstance(obj, Aresta) and self.x == obj.x and self.y == obj.y

  def addPeso(self) -> None:
      self.peso += 1

  def minusPeso(self) -> None:
      if self.peso != 0:
          self.peso -= 1

  def getVerticeFinal(self):
      return self.y
