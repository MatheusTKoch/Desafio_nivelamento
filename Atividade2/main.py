import requests
from bs4 import BeautifulSoup
import tabula
import pandas as pd
import zipfile
import os
import logging
from typing import List

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


url = 'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos'
session = requests.Session()

# Request da url e obtenção do texto parsed
try:
    response = session.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    a = soup.find('a', string=lambda text: text and 'Anexo I.' in text.strip())
    if not a:
        raise ValueError("Link do Anexo I não encontrado")
    
    href = a.get('href')
    if not href:
        raise ValueError("URL do PDF não encontrada")

    # Download do PDF
    logging.info("Iniciando download do PDF...")
    response = session.get(href)
    response.raise_for_status()

    if 'application/pdf' not in response.headers.get('content-type', ''):
        raise ValueError("O arquivo baixado não é um PDF válido")

    pdf_path = "Anexo I.pdf"
    with open(pdf_path, 'wb') as pdf:
        pdf.write(response.content)
    logging.info("Download do PDF finalizado com sucesso")

    # Extraindo tabelas do PDF
    logging.info("Iniciando extração das tabelas...")
    tables = tabula.read_pdf(
        pdf_path,
        pages='3-181',
        multiple_tables=True,
        lattice=True,
        guess=False,
        pandas_options={'header': None}
    )

    if not tables:
        raise ValueError("Nenhuma tabela encontrada no PDF")

    # Processamento das tabelas
    combined_df = pd.concat(tables, ignore_index=True)
    columns = [
        'PROCEDIMENTO', 'RN(alteração)', 'VIGÊNCIA', 'OD', 'AMB', 'HCO',
        'HSO', 'REF', 'PAC', 'DUT', 'SUBGRUPO', 'GRUPO', 'CAPÍTULO'
    ]

    combined_df = combined_df[~combined_df.iloc[:, 0].isin(columns)]
    if len(combined_df.columns) != len(columns):
        raise ValueError(f"Número incorreto de colunas: esperado {len(columns)}, obtido {len(combined_df.columns)}")

    combined_df.columns = columns
    combined_df = combined_df.dropna(how='all').reset_index(drop=True)

    # Ajuste de OD e AMB
    if 'OD' in combined_df.columns:
        combined_df['OD'] = combined_df['OD'].apply(
            lambda x: 'Seg. Odontológica' if pd.notna(x) and str(x).strip() else x
        )

    if 'AMB' in combined_df.columns:
        combined_df['AMB'] = combined_df['AMB'].apply(
            lambda x: 'Seg. Ambulatorial' if pd.notna(x) and str(x).strip() else x
        )

    arquivo_csv = 'Anexo_I_Completo.csv'
    combined_df.to_csv(arquivo_csv, index=False, encoding='utf-8-sig', sep=';')
    logging.info(f"CSV criado com {len(combined_df)} linhas e {len(combined_df.columns)} colunas")

    # Compactando arquivo final
    arquivo_zip = 'Teste_{Matheus_Trilha_Koch}.zip'
    with zipfile.ZipFile(arquivo_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(arquivo_csv)
        logging.info(f"Arquivo ZIP criado: {arquivo_zip}")

    os.remove(arquivo_csv)
    os.remove(pdf_path)
    logging.info("Arquivos temporários removidos com sucesso")

except requests.RequestException as e:
    logging.error(f"Erro na requisição HTTP: {str(e)}")
except ValueError as e:
    logging.error(f"Erro de validação: {str(e)}")
except Exception as e:
    logging.error(f"Erro inesperado: {str(e)}")
finally:
    session.close()
    logging.info("Processamento finalizado")
