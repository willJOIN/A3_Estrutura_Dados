from parser.roman import rom_parse
import re
import os


def criar_tabela_substituicao():
  chars_acentuados = "ÁÉÍÓÚÀÈÌÒÙÃẼĨÕŨÂÊÎÔÛÄËÏÖÜÇ"
  chars = "AEIOUAEIOUAEIOUAEIOUAEIOUC"

  # cria um "mapa" sendo o char com acento a value e o seu correspondente a chave
  tabela = {
      ord(acento): ord(sem_acento)
      for acento, sem_acento in zip(chars_acentuados, chars)
  }
  return tabela


def substituir_acentos(linha_com_acentos):
  return linha_com_acentos.translate(criar_tabela_substituicao())


def remover_numeros_extenso(linha_numero_extenso):

  linha = linha_numero_extenso.split(" ")
  numeros_extenso = []

  with open("numeros_extenso.txt", "r") as f:
    numeros_extenso = f.readlines()

  numeros_extenso = [
      numero.replace("\n", "").strip() for numero in numeros_extenso
  ]

  numero_removidos = 0

  for idx in range(len(linha)):
    if linha[idx - numero_removidos] in numeros_extenso:
      linha.remove(linha[idx - numero_removidos])
      numero_removidos += 1

  return " ".join(linha)


def remover_numeros_ordinais(linha_numeros_ordinais):
  linha = linha_numeros_ordinais.split(" ")
  linha = [palavra for palavra in linha if "ESIMO" not in palavra]

  ordinais = []

  with open("numeros_ordinais.txt", "r") as f:
    ordinais = f.readlines()

  ordinais = [numero.replace("\n", "").strip() for numero in ordinais]

  numero_removidos = 0

  for idx in range(len(linha)):
    if linha[idx - numero_removidos] in ordinais:
      linha.remove(linha[idx - numero_removidos])
      numero_removidos += 1

  return " ".join(linha)


def remover_numeros_romanos(linha_com_romanos):
  linha = linha_com_romanos.split(" ")

  for idx in range(len(linha)):
    try:
      rom_parse(linha[idx])
      linha.remove(linha[idx])
    except Exception:
      continue

  return " ".join(linha)


def remover_stop_words(linha_crua):
  linha = linha_crua.strip()

  stop_words = []

  with open("stop_words.txt", "r") as f:
    for line in f.readlines():
      for stop_word in line.split(", "):
        stop_words.append(substituir_acentos(stop_word.upper()))

  stop_words = list(set(stop_words))

  linha = " ".join([
      palavra.strip() for palavra in re.split(" +", linha)
      if palavra.strip() not in stop_words
  ])

  return linha


def limpar_linha(linha_com_espacos):
  especiais = "°ªº!@#$%¨&*=+-_()[]{}´`~^:;.,/?\|'"
  numeros = [str(valor) for valor in range(0, 10)]

  linha = linha_com_espacos

  for especial in especiais:
    linha = linha.replace(especial, "")

  for numero in numeros:
    linha = linha.replace(numero, "")

  return linha.replace("\n", "").upper()


def limpar_terminal():
  if os.name == "posix":
    os.system("clear")
  else:
    os.system("cls")
