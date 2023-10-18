from unidecode import unidecode

def tokenization():
  texto_com_acento = []
  texto_sem_acento = []
  
  with open("textos/arq_1.txt", 'rb') as f:
    texto_com_acento = f.readlines()

  texto_sem_acento = remover_acentos(texto_com_acento)
  
  print(texto_sem_acento)

def remover_acentos(texto_com_acentos):
  return unidecode(texto_com_acentos)

if __name__ == "__main__":
  tokenization()
