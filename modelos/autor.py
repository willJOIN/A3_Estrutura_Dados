from artigo import Artigo


class Autor:
    # pior caso: O(1)
    # melhor caso: Ω(1)
    def __init__(self, nome):
        # lista de artigos
        self.nome = nome
        self.artigos: list[Artigo] = []

    # pior caso: O(1)
    # melhor caso: Ω(1)
    def __str__(self) -> str:
        return f"autor:{self.nome}"

    # pior caso: O(1)
    # melhor caso: Ω(1)
    def __repr__(self):
        return str(self)

    # pior caso: O(1)
    # melhor caso: Ω(1)
    def __hash__(self) -> int:
        return hash(self.nome)

    # pior caso: O(1)
    # melhor caso: Ω(1)
    def __eq__(self, obj: object) -> bool:
        return isinstance(obj, Autor) and self.nome == obj.nome

    # pior caso: O(1)
    # melhor caso: Ω(1)
    def add_artigo(self, texto):
        art = Artigo(texto)
        if art not in self.artigos:
            self.artigos.append(art)
        else:
            raise Warning(
                f"artigo ja está na lista de artigos desse autor - autor: {self.nome}"
            )
