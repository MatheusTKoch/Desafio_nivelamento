import requests
from bs4 import BeautifulSoup


#Request da url e obtencao do texto parsed
url = 'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

#Localizando links e filtrando pelo texto 'Anexo'

a = soup.find('a', string=lambda text: text and 'Anexo I.' in text.strip())
href = a.get('href')

#Baixando o conteudo e inserindo nos arquivos PDF

print("Baixando PDF")
response = requests.get(href)
pdf = open("Anexo I.pdf", 'wb')
pdf.write(response.content)
pdf.close()
print("Download Finalizado")




