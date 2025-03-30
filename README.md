## Estrutura do Projeto

O projeto está organizado nas seguintes seções:

1. **Testes de Nivelamento**
2. **Testes de Transformação de Dados**
3. **Testes de Análise de Dados**
4. **Teste da API**

## Pré-requisitos

- Python 3.x
- Ambiente virtual Python (disponível na pasta `env_nivelamento`)

## Configuração do Ambiente

Para executar as atividades 1, 2 e 3, siga as instruções abaixo:

### Ativando o Ambiente Virtual

#### No Windows:
```
cd env_nivelamento\Scripts
activate
cd ..\..
```

#### No Linux/Mac:
```
source env_nivelamento/bin/activate
```

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

## Observações

- Certifique-se de seguir todas as instruções específicas para cada atividade
- Os arquivos de saída devem ser organizados conforme solicitado nos requisitos