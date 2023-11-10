import os
import time
from datetime import datetime
import re

from util import limpar_terminal, string_lista_identada


class Avaliado:
    def __init__(
        self,
        arquivo: str,
        topicos: list[str],
        relevantes: list[str],
        nao_relevantes: list[str],
    ) -> None:
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

    quantidade = 0
    total_documentos = len(os.listdir("textos/"))

    while True:
        limpar_terminal()

        try:
            print("Escolha quantos textos deseja avaliar:")
            print("OBS: Não digite nada para avaliar todos os textos!\n")
            quantidade_str = input("")

            if quantidade_str.strip() == "":
                quantidade = total_documentos
                break

            quantidade = int(quantidade_str)

            if quantidade <= 0 and quantidade > total_documentos:
                raise Exception()

        except ValueError:
            print("\nDigite uma quantidade válida (Apenas números são aceitos)")
            time.sleep(4)
        except Exception:

            print(
                "\nDigite uma quantidade válida (Não há esse número de textos na pasta 'avaliacoes/')"
            )
            time.sleep(4)
        
        break
    
    tokens_arquivos = {chave: tokens_arquivos_dict[chave] for chave in list(tokens_arquivos_dict)[:quantidade]}

    for arquivo, tokens in tokens_arquivos.items():
        print()
        opcoes_nao_relevantes: dict[int, str] = {}
        opcoes_relevantes = tokens.copy()

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
                        avaliado = Avaliado(
                            arquivo,
                            tokens,
                            opcoes_relevantes,
                            list(opcoes_nao_relevantes.values()),
                        )
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


def gerar_estatisticas(avaliados: list[Avaliado]):
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

        nao_relevantes_corretos = topicos_identificados.intersection(
            topicos_nao_relevantes
        )
        total_nao_relevantes_corretos += len(nao_relevantes_corretos)

        nao_relevantes_incorretos = topicos_nao_relevantes - nao_relevantes_corretos
        total_nao_relevantes_incorretos += len(nao_relevantes_incorretos)

    precisao = (
        total_relevantes_corretos
        / (total_relevantes_corretos + total_nao_relevantes_corretos)
    ) * 100

    str_total_documentos = f"-    Total de documentos avaliados: {total_documentos}"
    str_total_relevantes_corretos = f"-    Total de tópicos relevantes corretamente identificados: {total_relevantes_corretos}"
    str_total_relevantes_incorretos = f"-    Total de tópicos relevantes incorretamente identificados: {total_relevantes_incorretos}"
    str_total_nao_relevantes_corretos = f"-    Total de tópicos não relevantes corretamente identificados: {total_nao_relevantes_corretos}"
    str_total_nao_relevantes_incorretos = f"-    Total de tópicos não relevantes incorretamente identificados: {total_nao_relevantes_incorretos}"
    str_precisao = f"-    Precisão: {precisao:.2f} %"

    data = datetime.now().strftime("%d-%m-%Y")

    with open(f"avaliacoes/avaliacao_{data}.txt", "w", encoding="utf-8") as f:
        f.write(
            "-----------------------------LOG DE AVALIAÇÃO-----------------------------\n\n"
        )
        f.write(f"Avaliação feita na data: {data.replace('-','/')}\n\n")
        f.write("ESTATÍSTICAS FINAIS:\n\n")
        f.write(f"{str_total_documentos}\n")
        f.write(f"{str_total_relevantes_corretos}\n")
        f.write(f"{str_total_relevantes_incorretos}\n")
        f.write(f"{str_total_nao_relevantes_corretos}\n")
        f.write(f"{str_total_nao_relevantes_incorretos}\n")
        f.write(f"{str_precisao}\n\n")
        f.write("ARQUIVOS AVALIADOS:\n")

        for avaliado in avaliados:
            f.write(
                f"\n======================== INICIO -> {avaliado.arquivo} ========================"
            )

            topicos_relevantes = string_lista_identada(
                sorted(
                    set(avaliado.topicos_relevantes),
                    key=lambda item: item[1],
                    reverse=True,
                )
            )
            topicos_nao_relevantes = string_lista_identada(
                sorted(
                    set(avaliado.topicos_nao_relevantes),
                    key=lambda item: item[1],
                    reverse=True,
                ),
                " " * 4,
            )
            topicos_identificados = string_lista_identada(
                sorted(
                    set(avaliado.topicos),
                    key=lambda item: item[1],
                    reverse=True,
                ),
                " ",
            )

            f.write(f"\n\n=    Tópicos encontrados: {topicos_identificados}")
            f.write(f"\n\n=    Tópicos relevantes: {topicos_relevantes}")
            f.write(f"\n\n=    Tópicos não relevantes: {topicos_nao_relevantes}")
            f.write(
                f"\n\n========================= FIM -> {avaliado.arquivo} ==========================\n"
            )

        f.write(
            "\n--------------------------------------------------------------------------"
        )
