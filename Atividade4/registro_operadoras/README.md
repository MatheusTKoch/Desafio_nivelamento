# Atividade 4 - Teste da API

Este projeto consiste em uma interface web desenvolvida com Vue.js que se comunica com um servidor em Python (Flask).

## Pré-requisitos

- Python 3.x
- Node.js e npm
- Ambiente virtual Python (disponível na pasta `env_operadoras`)

## Configuração do Ambiente Backend (Flask)

### Ativando o Ambiente Virtual

#### No Windows:
```
cd env_operadoras\Scripts
activate
cd ..\..
```

#### No Linux/Mac:
```
source env_operadoras/bin/activate
```

### Iniciando o Servidor Flask

Na pasta raiz do projeto:

```
flask run
```

Por padrão, o servidor estará disponível em http://127.0.0.1:5000/

### Instalando Dependências

Após ativar o ambiente virtual, instale as dependências necessárias:

```
pip install -r requirements.txt
```

As principais bibliotecas incluídas são:
- requests: Para requisições HTTP
- beautifulsoup4: Para web scraping
- pandas: Para manipulação de dados
- tabula-py: Para extração de tabelas de PDFs

Para verificar se todas as dependências foram instaladas corretamente:
```
pip list
```

## Consultas pelo Postman

```
{
	"info": {
		"_postman_id": "operadoras-search-collection",
		"name": "Operadoras ANS Search",
		"schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
	},
	"item": [
		{
			"name": "Search Operadoras",
			"request": {
				"method": "GET",
				"header": [],
				"url": {
					"raw": "http://localhost:5000/search?q=Unimed",
					"protocol": "http",
					"host": ["localhost"],
					"port": "5000",
					"path": ["search"],
					"query": [
						{
							"key": "q",
							"value": "Unimed"
						}
					]
				}
			},
			"response": []
		}
	]
    }
```
Collection no Postman: https://matheustk-3846102.postman.co/workspace/Matheus-T-Ks-Workspace~ce16fbef-f2de-47e4-8308-d9417f37ef33/collection/43587672-90aecc7a-9b5e-43cf-8c73-772c874c1f60?action=share&creator=43587672

## Observações

- Certifique-se que o servidor Flask esteja rodando antes de acessar a interface web
- Verifique se todas as dependências foram instaladas corretamente