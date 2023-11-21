class Artigo:
    def __init__(self, titulo, texto, autor, coautor):
        self.titulo = titulo
        self.texto = texto
        self.autor = autor
        self.coautor = coautor

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
