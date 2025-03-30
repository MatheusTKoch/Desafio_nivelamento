import requests
from bs4 import BeautifulSoup
import tabula
import pandas as pd
import zipfile
import os

# Request da url e obtenção do texto parsed
url = 'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

# Localizando links e filtrando pelo texto 'Anexo'
a = soup.find('a', string=lambda text: text and 'Anexo I.' in text.strip())
href = a.get('href')

print("Baixando PDF")
response = requests.get(href)
with open("Anexo I.pdf", 'wb') as pdf:
    pdf.write(response.content)
print("Download Finalizado")

pdf_path = "Anexo I.pdf"
    
    # Extraindo tabelas do PDF
tables = tabula.read_pdf(
        pdf_path, 
        pages='3-181', 
        multiple_tables=True,
        lattice=True,
        guess=False,
        pandas_options={'header': None}
    )
    
combined_df = pd.concat(tables, ignore_index=True)
    
columns = [
        'PROCEDIMENTO', 'RN(alteração)', 'VIGÊNCIA', 'OD', 'AMB', 'HCO',
        'HSO', 'REF', 'PAC', 'DUT', 'SUBGRUPO', 'GRUPO', 'CAPÍTULO'
    ]
    
combined_df = combined_df[~combined_df.iloc[:, 0].isin(columns)]

if len(combined_df.columns) == len(columns):
    combined_df.columns = columns
    
combined_df = combined_df.dropna(how='all').reset_index(drop=True)
    
# Ajustando valores de OD
if 'OD' in combined_df.columns:
    combined_df['OD'] = combined_df['OD'].apply(lambda x: 'Seg. Odontológica' if pd.notna(x) and str(x).strip() else x)
    
# Ajustando valores de AMB
if 'AMB' in combined_df.columns:
    combined_df['AMB'] = combined_df['AMB'].apply(lambda x: 'Seg. Ambulatorial' if pd.notna(x) and str(x).strip() else x)
    
# Salvando arquivo CSV
arquivo_csv = 'Anexo_I_Completo.csv'
combined_df.to_csv(arquivo_csv, index=False, encoding='utf-8-sig', sep=';')
print(f"CSV created with {len(combined_df)} rows and {len(combined_df.columns)} columns")


arquivo_zip = 'Teste_{Matheus_Trilha_Koch}.zip'
with zipfile.ZipFile(arquivo_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(arquivo_csv)
    print(f"Created ZIP file: {arquivo_zip}")
    
    os.remove(arquivo_csv)
print(f"Removido arquivo original: {arquivo_csv}")
