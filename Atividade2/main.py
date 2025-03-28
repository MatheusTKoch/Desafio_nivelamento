import requests
from bs4 import BeautifulSoup
import camelot
import time
import tabula
import pandas as pd

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
    tables = camelot.read_pdf('Anexo I.pdf', pages='3-181', table_areas=['0,1000,1000,0'], split_text=True, line_scale=40)

    combined_df = pd.concat([table.df for table in tables])
    combined_df = combined_df[~combined_df.apply(lambda row: row.astype(str).str.strip().eq('').all(), axis=1)]
    combined_df = combined_df.reset_index(drop=True)
        
    combined_df.to_csv('Anexo I.csv', index=False, encoding='utf-8-sig', sep=';')
        
    print('Arquivo CSV salvo com sucesso')
except Exception as e:
    print(f"Erro ao processar o PDF: {str(e)}")


