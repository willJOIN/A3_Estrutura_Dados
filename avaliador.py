import time

from util import limpar_terminal

class Avaliado:

  def __init__(self, arquivo: str, topicos: list[str], relevantes: list[str],
               nao_relevantes: list[str]) -> None:
    self.arquivo: str = arquivo
    self.topicos: list[str] = topicos
    self.topicos_relevantes: list[str] = relevantes
    self.topicos_nao_relevantes: list[str] = nao_relevantes

  def __str__(self) -> str:
    return f"Arquivo: {self.arquivo}\nTópicos Encontrados: {self.topicos}\nRelevantes: {self.topicos_relevantes}\nNão Relevantes: {self.topicos_nao_relevantes}"

  def __repr__(self) -> str:
    return str(self)
  

def avaliar(tokens_arquivos_dict: dict):
  avaliados = []

  for arquivo, tokens in tokens_arquivos_dict.items():
    print()
    opcoes_nao_relevantes: dict[int, str] = {}
    opcoes_relevantes = tokens

    while True:
      limpar_terminal()
      print(f"Escolha os tópicos *NÃO* relevantes do arquivo [{arquivo}]:\n")

      for opcao in range(len(opcoes_relevantes)):
        print(f"{opcao + 1}) {opcoes_relevantes[opcao]}")

      print(f"{len(opcoes_relevantes) + 1}) Avaliar")

      if len(opcoes_nao_relevantes) > 0:
        print(f"{len(opcoes_relevantes) + 2}) Desfazer última escolha")

      try:
        opcao = int(input("\nEscolha uma opção: "))

        if opcao < 0 or opcao > len(opcoes_relevantes):

          if len(opcoes_nao_relevantes) > 0:
            if opcao == len(opcoes_relevantes) + 2:
              ultima_opcao = opcoes_nao_relevantes.popitem()
              opcoes_relevantes.insert(ultima_opcao[0], ultima_opcao[1])
              continue
          if opcao == len(opcoes_relevantes) + 1:
            avaliado = Avaliado(arquivo, tokens, opcoes_relevantes,
                                list(opcoes_nao_relevantes.values()))
            avaliados.append(avaliado)
            break

          raise Exception()

        opcoes_nao_relevantes[opcao - 1] = opcoes_relevantes[opcao - 1]
        opcoes_relevantes.remove(opcoes_relevantes[opcao - 1])

      except ValueError:
        print("\nEscolha uma opção válida (Apenas números são aceitos)")
        time.sleep(4)
      except Exception:
        print(
            "\nEscolha uma opção válida (Apenas números dentre as opções são aceitos)"
        )
        time.sleep(4)

  gerar_estatisticas(avaliados)

def gerar_estatisticas(avaliados:list[Avaliado]):
  limpar_terminal()
  print("Gerando dados de avaliação...")

  total_documentos = len(avaliados)
  total_relevantes_corretos = 0
  total_relevantes_incorretos = 0
  total_nao_relevantes_corretos = 0
  total_nao_relevantes_incorretos = 0

  for avaliado in avaliados:
    topicos_relevantes = set(avaliado.topicos_relevantes)
    topicos_nao_relevantes = set(avaliado.topicos_nao_relevantes)
    topicos_identificados = set(avaliado.topicos)

    relevantes_corretos = topicos_identificados.intersection(topicos_relevantes)
    total_relevantes_corretos += len(relevantes_corretos)

    relevantes_incorretos = topicos_identificados - relevantes_corretos
    total_relevantes_incorretos += len(relevantes_incorretos)

    nao_relevantes_corretos = len(avaliado.topicos_nao_relevantes) - len(relevantes_incorretos)
    total_nao_relevantes_corretos += nao_relevantes_corretos

    nao_relevantes_incorretos = len(topicos_nao_relevantes) - nao_relevantes_corretos
    total_nao_relevantes_incorretos += nao_relevantes_incorretos

  precisao = (total_relevantes_corretos / (total_relevantes_corretos + total_nao_relevantes_incorretos)) * 100

  print(f"Total de documentos avaliados: {total_documentos}")
  print(f"Total de tópicos relevantes corretamente identificados: {total_relevantes_corretos}")
  print(f"Total de tópicos relevantes incorretamente identificados: {total_relevantes_incorretos}")
  print(f"Total de tópicos não relevantes corretamente identificados: {total_nao_relevantes_corretos}")
  print(f"Total de tópicos não relevantes incorretamente identificados: {total_nao_relevantes_incorretos}")
  print(f"Precisão: {precisao:.2f} %")
