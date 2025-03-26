import requests
from bs4 import BeautifulSoup

#Request da url e obtencao do texto parseado

url = 'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

#Localizando links e filtrando pelo texto 'Anexo'
a = soup.find_all('a', string=lambda text: text and 'Anexo' in text.strip())

i = 0

#Baixando o conteudo para inserir nos arquivos PDF
for link in a:
    if ('.pdf' in link.get('href', [])):
        i += 1
        print("Baixando PDF Anexo", i)
        response = requests.get(link.get('href'))

        pdf = open("Anexo"+str(i)+".pdf", 'wb')
        pdf.write(response.content)
        pdf.close()
        print("Anexo", i, "baixado.")

print("Download Finalizado")

