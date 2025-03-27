import requests
from bs4 import BeautifulSoup
import camelot
import time
import tabula

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
with open("Anexo I.pdf", 'wb') as pdf:
    pdf.write(response.content)
print("Download Finalizado")

#Extraindo dados e convertendo para csv
time.sleep(2)
try:
    tables = tabula.read_pdf('Anexo I.pdf', pages='3-end')
    tabula.convert_into(tables, 'Anexo I.csv', output_format='csv', pages='all')
    # tables = camelot.read_pdf("Anexo I.pdf", pages='3-end', flavor='stream')
    # print("Paginas extraidas: ", tables.n)
    # tables.export("Teste_MatheusTrilhaKoch.csv", f="csv", compress=True)
except Exception as e:
    print(f"Erro ao processar o PDF: {str(e)}")
finally:
    if 'tables' in locals():
        del tables


