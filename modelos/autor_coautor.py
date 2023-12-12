class SourceTarget:
    # pior caso: O(1)
    # melhor caso: Ω(1)   
    def __init__(self, autor, coautor, peso_aresta):
        # lista de artigos
        self.autor = autor
        self.coautor = coautor
        self.peso_aresta = peso_aresta

    # pior caso: O(1)
    # melhor caso: Ω(1)
    def __str__(self) -> str:
        return f"Autor:{self.autor}\nCoautor:{self.coautor}"

    # pior caso: O(1)
    # melhor caso: Ω(1)
    def __repr__(self):
        return str(self)

    # pior caso: O(n log n)
    # melhor caso: Ω(1)
    def __hash__(self) -> int:
        autores = [self.autor, self.coautor]
        autores.sort()

        return hash((autores[0], autores[1]))

    # pior caso: O(n log n)
    # melhor caso: Ω(1)
    def __eq__(self, obj: object) -> bool:
        if isinstance(obj, SourceTarget):
            autores_obj = [obj.autor, obj.coautor]
            autores_self = [self.autor, self.coautor]

            autores_obj.sort()
            autores_self.sort()

            return (
                autores_self[0] == autores_obj[0] and autores_self[1] == autores_obj[1]
            )

        return False

    # pior caso: O(1)
    # melhor caso: Ω(1)
    def maior_peso_aresta(autorCoautor1, autorCoautor2):
        return (
            autorCoautor1
            if autorCoautor1.peso_aresta > autorCoautor2.peso_aresta
            else autorCoautor2
        )
