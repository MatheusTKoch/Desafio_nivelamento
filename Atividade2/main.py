import requests
from bs4 import BeautifulSoup
import camelot
import time
import pandas as pd
import re

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

time.sleep(2)
try:
    # Extrai a tabela principal com procedimentos
    tables_procedimentos = camelot.read_pdf(
        'Anexo I.pdf', 
        pages='3-10',
        table_areas=['0,1000,1000,0'], 
        split_text=True, 
        line_scale=60
    )
    
    # Extrai a tabela de capítulos que está em outra parte do PDF
    tables_capitulos = camelot.read_pdf(
        'Anexo I.pdf', 
        pages='1-2',
        table_areas=['0,1000,1000,0'], 
        split_text=True, 
        line_scale=60
    )

    combined_df = pd.concat([table.df for table in tables_procedimentos])
    combined_df = combined_df[~combined_df.apply(lambda row: row.astype(str).str.strip().eq('').all(), axis=1)]
    combined_df = combined_df.reset_index(drop=True)
    
    columns = [
        ' ', 'PROCEDIMENTO', 'RN(alteração)', 'VIGÊNCIA', 'OD', 'AMB', 'HCO', 
        'HSO', 'REF', 'PAC', 'DUT', 'SUBGRUPO', 'GRUPO', 'CAPÍTULO'
    ]
    

    if len(combined_df.columns) > len(columns):
        combined_df = combined_df.iloc[:, 1:len(columns)+1]
    

    combined_df.columns = columns[:len(combined_df.columns)]
    
    # Filtrar linhas que contêm informações de legenda
    legend_keywords = ['Legenda:', 'HCO:', 'OD:', 'HSO:', 'AMB:', 'REF:']
    

    legend_mask = combined_df.apply(
        lambda row: any(keyword in str(cell) for keyword in legend_keywords for cell in row),
        axis=1
    )
    
    additional_legend_mask = combined_df.apply(
        lambda row: (row.astype(str).str.strip().eq('').sum() > len(row) * 0.7) or
                    ('CONSULTAS, VISITAS HOSPITALARES' in str(row.iloc[0])) or
                    ('ACOMPANHAMENTO DE PACIENTES' in str(row.iloc[0])),
        axis=1
    )
    
    clean_df = combined_df[~(legend_mask | additional_legend_mask)]
    clean_df = clean_df.reset_index(drop=True)
    
    # Ajuste em OD
    if 'OD' in clean_df.columns:
        clean_df['OD'] = clean_df['OD'].apply(
            lambda x: 'Seg. Odontológica' if x == 'OD' or x.strip() == 'OD' else x
        )
    
    # Ajuste em AMB
    if 'AMB' in clean_df.columns:
        clean_df['AMB'] = clean_df['AMB'].apply(
            lambda x: 'Seg. Ambulatorial' if x == 'AMB' or x.strip() == 'AMB' else x
        )
    
    if tables_capitulos:
        capitulos_df = pd.concat([table.df for table in tables_capitulos])

        capitulos_df = capitulos_df[~capitulos_df.apply(lambda row: row.astype(str).str.strip().eq('').all(), axis=1)]

        capitulos_mask = capitulos_df.apply(
            lambda row: bool(re.search(r'CAPÍTULO', str(row.iloc[0]), re.IGNORECASE)),
            axis=1
        )
        
        capitulos_clean_df = capitulos_df[capitulos_mask].reset_index(drop=True)
        
        if not capitulos_clean_df.empty:
            capitulos_clean_df.to_csv('Capitulos.csv', index=False, encoding='utf-8-sig', sep=';')
            print(f'Arquivo de Capítulos salvo com sucesso. Total de linhas: {len(capitulos_clean_df)}')
    
    if 'SUBGRUPO' in clean_df.columns:
        clean_df['SUBGRUPO'] = clean_df['SUBGRUPO'].fillna(method='ffill')

    clean_df.to_csv('Anexo I.csv', index=False, encoding='utf-8-sig', sep=';')
    
    print(f'Arquivo CSV salvo com sucesso. Total de linhas: {len(clean_df)}')
    print(f'Número de colunas: {len(clean_df.columns)}')
    
    print("\nPrimeiras 5 linhas do arquivo:")
    print(clean_df.head(5))
    
except Exception as e:
    print(f"Erro ao processar o PDF: {str(e)}")
    import traceback
    traceback.print_exc()