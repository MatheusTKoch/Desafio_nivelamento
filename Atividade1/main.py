import os
import requests
from bs4 import BeautifulSoup
import zipfile
import logging
from typing import List
from urllib.parse import urljoin

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# URL base para busca dos documentos
BASE_URL = 'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos'

session = requests.Session()

try:
    response = session.get(BASE_URL)
    response.raise_for_status()
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')
    pdf_links = []

    links = soup.find_all('a', string=lambda text: text and 'Anexo' in text.strip())
    for link in links:
        href = link.get('href', '')
        if '.pdf' in href.lower():
            full_url = urljoin(BASE_URL, href)
            pdf_links.append(full_url)

    if not pdf_links:
        logging.error("Nenhum PDF encontrado")
        exit(1)

    downloaded_files = []

    # Download dos PDFs
    for i, link in enumerate(pdf_links, 1):
        filename = f"Anexo{i}.pdf"
        logging.info(f"Baixando {filename}...")

        try:
            pdf_response = session.get(link, stream=True)
            pdf_response.raise_for_status()

            if 'application/pdf' not in pdf_response.headers.get('content-type', ''):
                logging.warning(f"O arquivo {filename} pode não ser um PDF válido")
                continue

            with open(filename, 'wb') as pdf_file:
                for chunk in pdf_response.iter_content(chunk_size=8192):
                    if chunk:
                        pdf_file.write(chunk)

            downloaded_files.append(filename)
            logging.info(f"{filename} baixado com sucesso")

        except Exception as e:
            logging.error(f"Erro ao baixar {filename}: {e}")
            continue

    #Compactando arquivos
    if downloaded_files:
        zip_filename = 'Anexos.zip'
        try:
            with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for pdf in downloaded_files:
                    if os.path.exists(pdf):
                        zip_file.write(pdf)
                        os.remove(pdf)
                    else:
                        logging.warning(f"Arquivo {pdf} não encontrado")
            logging.info("Arquivos compactados com sucesso")
        except Exception as e:
            logging.error(f"Erro ao criar ZIP: {e}")
    else:
        logging.error("Nenhum arquivo foi baixado com sucesso")

except requests.RequestException as e:
    logging.error(f"Erro ao acessar a URL: {e}")
except Exception as e:
    logging.error(f"Erro inesperado: {e}")
finally:
    session.close()

