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

## Observações

- Certifique-se que o servidor Flask esteja rodando antes de acessar a interface web
- Verifique se todas as dependências foram instaladas corretamente