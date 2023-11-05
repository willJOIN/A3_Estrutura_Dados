import util
import re

class Topicos:

  def __init__(self, textos: list) -> None:
    self.textos = textos
    self.topicos_tokens = {}
    self.gerar()
  
  def __str__(self) -> str:
    string = ""
  
    for arquivo, token_list in self.topicos_tokens.items():
      string += f"\n\n10 palavras mais frequentes em {arquivo}:\n{token_list}"
  
    return string
  
  def execucao_linha(self, linha):
  
    linha_temp = util.limpar_linha(linha)
    linha_temp = util.substituir_acentos(linha_temp)
    linha_temp = util.remover_stop_words(linha_temp)
    linha_temp = util.remover_numeros_romanos(linha_temp)
    linha_temp = util.remover_numeros_extenso(linha_temp)
    linha_temp = util.remover_numeros_ordinais(linha_temp)
  
    return re.split(" +", linha_temp)
  
  def gerar(self):
  
    print("Encontrando os tópicos mais relevantes dos textos...")
  
    for texto in self.textos:
      try:
        self.topicos_tokens[texto] = self.gerar_mais_relevantes_texto(texto)
      except Exception:
        continue
  
  def gerar_mais_relevantes_texto(self, nome_arquivo_texto: str):
    tokens = {}
  
    with open(f"textos/{nome_arquivo_texto}", "r", encoding="ISO-8859-1") as f:
      # le o arquivo e armazena em linha
      for line in f.readlines():
        for token in self.execucao_linha(line):
          if tokens.get(token):
            tokens[token] += 1
          else:
            tokens[token] = 1
  
      # Ordena tokens em ordem decrescente de frequencia
      sorted_tokens = dict(
          sorted(tokens.items(), key=lambda item: item[1], reverse=True))
  
    return list(sorted_tokens.keys())[:10]