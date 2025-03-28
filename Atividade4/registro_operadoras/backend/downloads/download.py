import requests
import os

url = 'https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv'
    
try:
    #Verificando destino da pasta e se a pasta existe
    response = requests.get(url)
    os.makedirs('downloads', exist_ok=True)
        
    filepath = 'operadoras_ativas.csv'
    with open(filepath, 'wb') as file:
        file.write(response.content)
        file.close()
    print(f"CSV baixado corretamente em {filepath}")
    
except Exception as e:
    print(f"Erro ao baixar CSV: {str(e)}")
