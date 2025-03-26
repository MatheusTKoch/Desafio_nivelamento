import os
import requests
from bs4 import BeautifulSoup
import zipfile


#Request da url e obtencao do texto parsed
url = 'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

#Localizando links e filtrando pelo texto 'Anexo'
a = soup.find_all('a', string=lambda text: text and 'Anexo' in text.strip())

#Baixando o conteudo para inserir nos arquivos PDF
i = 0

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

#Zipando o arquivo e deletando os PDFs descompactados
fileName = 'Anexos.zip'

z = zipfile.ZipFile(fileName, 'w', zipfile.ZIP_DEFLATED)

with os.scandir('./') as it:
    for pdf in it:
        if pdf.name.endswith(".pdf") and pdf.is_file():
            z.write(pdf.name)
            os.remove(pdf)
print("Arquivo compactado")

