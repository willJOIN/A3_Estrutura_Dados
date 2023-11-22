class Artigo:
    def __init__(self, titulo:str, autor:str, coautores:list[str] ,descricao:str):
        self.descricao = descricao
        self.autor = autor
        self.coautores = coautores
        self.titulo = titulo

    def __str__(self) -> str:
        return (
            f"{self.titulo}\n{self.texto}\nautor: {self.autor}\tcoaturo:{self.coautor}"
        )

    def __repr__(self):
        return str(self)

    def __hash__(self) -> int:
        return hash(self.titulo)

    def __eq__(self, obj: object) -> bool:
        return (
            isinstance(obj, Artigo)
            and self.titulo == obj.titulo
            and self.autor == obj.autor
            and self.coautor == obj.coautor
        )