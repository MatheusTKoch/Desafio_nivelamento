import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys

app = Flask(__name__)
CORS(app)

# Função para carregar os dados
def load_data():
    try:
        os.makedirs('downloads', exist_ok=True)
        
        csv_path = 'downloads/operadoras_ativas.csv'
        
        if not os.path.isfile(csv_path):
            print("Arquivo CSV não encontrado. Executando script de download...")
            if os.path.isfile('downloads/download.py'):
                exit_code = os.system('python downloads/download.py')
                if exit_code != 0:
                    raise Exception("Erro ao executar o script de download")
            else:
                raise Exception("Script de download não encontrado em downloads/download.py")
        
        try:
            df = pd.read_csv(csv_path, sep=';', encoding='latin-1')
            
            df = df.rename(columns={
                'Registro ANS': 'Registro_ANS',
                'Nome Fantasia': 'Nome_Fantasia'
            })
            
            return df
            
        except Exception as e:
            raise Exception(f"Erro ao ler o arquivo CSV: {str(e)}")
    
    except Exception as e:
        print(f"Erro ao carregar dados: {str(e)}", file=sys.stderr)
        return None
    
df = load_data()

@app.route('/search', methods=['GET'])
def search_operadoras():
    if df is None:
        return jsonify({'error': 'Erro ao carregar os dados das operadoras'}), 500
    
    query = request.args.get('q', '').lower().strip()
    
    if not query:
        return jsonify({'error': 'Nenhum termo de busca fornecido'}), 400
    
    try:
        results = df[df.astype(str).apply(
            lambda row: any(query in str(value).lower() for value in row),
            axis=1
        )]
        
        # Converte os resultados para uma lista de dicionários
        results_list = []
        for _, row in results.iterrows():
            results_list.append({
                'Registro_ANS': str(row['Registro_ANS']),
                'Nome_Fantasia': str(row['Nome_Fantasia']),
                'CNPJ': str(row['CNPJ']),
                'Modalidade': str(row['Modalidade'])
            })
        
        return jsonify({
            'results': results_list,
            'total_results': len(results_list)
        })
    
    except Exception as e:
        print(f"Erro na pesquisa: {str(e)}", file=sys.stderr)
        return jsonify({'error': f'Erro ao processar a pesquisa: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)