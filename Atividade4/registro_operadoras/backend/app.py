import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

# Localizar arquivo CSV
df = pd.read_csv('downloads/operadoras_ativas.csv', encoding='latin-1')

app = Flask(__name__)
CORS(app)

@app.route('/search', methods=['GET'])
def search_operadoras():
    query = request.args.get('q', '').lower()
    
    if not query:
        return jsonify({'error': 'No search query provided'}), 400
    
    # Pwesquisa em colunas
    results = df[
        df.apply(lambda row: any(
            str(value).lower().find(query) != -1 
            for value in row if pd.notna(value)
        ), axis=1)
    ]
    
    # Converter listas para dictionaries
    results_list = results.to_dict(orient='records')
    
    return jsonify({
        'total_results': len(results_list),
        'results': results_list
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)