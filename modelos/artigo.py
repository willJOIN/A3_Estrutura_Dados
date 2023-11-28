class Artigo:
    def __init__(self, texto: str):
        with open(f"textos/atividade2/{texto}", "r", encoding="utf-8") as f:
            txt = f.readlines()

            self.titulo = txt[0]
            # Segunda 'linha' contém o conteúdo do texto
            self.conteudo = txt[1:-2]

            self.coautores = []
            # Terceira 'linha' contem uma lista com as palavras-chave
            self.palavras_chaves = txt[-2].split(";")

            # Terceira 'linha' contem uma lista com as palavras-chave
            self.autores = txt[-1].split(",")
            self.autor = self.autores[0]

            for idx in range(1, len(self.autores)):
                self.coautores.append(self.autores[idx])

    def __str__(self) -> str:
        return f"{self.titulo}\n{self.conteudo}\nautor: {self.autor}\tcoautor:{self.coautores}"

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
