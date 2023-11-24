import os
from avaliador import avaliar
from tokenization import Tokens
from artigo import Artigo

def atividade_topicos_relevantes():
    textos = sorted(
      os.listdir("textos/atividade1/"),
      key=lambda item: int(item.replace("arq_", "").replace(".txt", ""))
    )
  
    tokens = Tokens(textos=textos,nome_pasta_arquivos="atividade1") 

    print(tokens)
    avaliar(tokens.resultado)

def atividade_coautoria():
    textos = sorted(
      os.listdir("textos/atividade2/"),
      key=lambda item: int(item.replace("artigo_", "").replace(".txt", ""))
    )

    artigos = [Artigo(texto) for texto in textos]
    tokens = Tokens(textos=textos,nome_pasta_arquivos="atividade2", artigos= artigos) 

    print(tokens.grafos[0])
    #print(artigos[0])
    #avaliar(tokens.resultado)

if __name__ == "__main__":
    #user_input = input('Por favor, insira o número da atividade que você deseja executar:\n1 - Tópicos\n2 - Coautoria')
    #if '1' in user_input:
    #   atividade_topicos_relevantes()
    #elif '2' in user_input:
    #   atividade_coautoria()
    atividade_coautoria()

    pass
