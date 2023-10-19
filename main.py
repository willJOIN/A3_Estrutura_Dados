import unicodedata
from grafo import Grafo


def tokenization():
  texto_com_acentos = []
  texto_sem_acentos = []

  # TODO loop pra ler cada arq_[i]
  with open("textos/arq_1.txt", 'r', encoding='utf-8') as f:
    texto_com_acentos = f.readlines()

  texto_sem_acentos = [substituir_acentos(line) for line in texto_com_acentos]

  print(texto_sem_acentos)


def substituir_acentos(texto_com_acentos):
  return texto_com_acentos.translate(criar_tabela_substituicao())


def criar_tabela_substituicao():
  tabela = {
      ord(acento): ord(sem_acento)
      for acento, sem_acento in zip('áéíóúàèìòùãẽĩõũâêîôûäëïöüç',
                                    'aeiouaeiouaeiouaeiouaeiouaeiouc')
  }
  return tabela


if __name__ == "__main__":
  #tokenization()

  grafo = Grafo()
  print(grafo)
  grafo.add_vertice(0)

  print(grafo)
