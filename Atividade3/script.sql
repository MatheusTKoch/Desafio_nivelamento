CREATE DATABASE IF NOT EXISTS ans_operadoras;

-- Usar o banco de dados
USE ans_operadoras;

-- Tabela de Operadoras
CREATE TABLE IF NOT EXISTS operadoras (
    registro_ans VARCHAR(50) PRIMARY KEY,
    cnpj VARCHAR(20),
    razao_social VARCHAR(255),
    nome_fantasia VARCHAR(255),
    modalidade VARCHAR(100),
    logradouro VARCHAR(100),
    numero VARCHAR(20),
    complemento VARCHAR(100),
    bairro VARCHAR(50),
    cidade VARCHAR(50),
    uf VARCHAR(2),
    cep VARCHAR(10),
    ddd VARCHAR(2),
    telefone VARCHAR(20),
    fax VARCHAR(10),
    email VARCHAR(100),
    representante VARCHAR(50),
    cargo_representante VARCHAR(50),
    regiao_comercializacao VARCHAR(2),
    data_registro_ANS DATE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Tabela de Demonstrações Contábeis
CREATE TABLE IF NOT EXISTS demonstracoes_contabeis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data_referencia date,
    registro_ans VARCHAR(50),
    conta_contabil VARCHAR(255),
    descricao VARCHAR(100),
    valor_saldo_inicial DECIMAL(18,2),
    valor_saldo_final DECIMAL(18,2),
    FOREIGN KEY (registro_ans) REFERENCES operadoras(registro_ans)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- ATENCAO: Antes de rodar os comandos, adicionar a opcao 'OPT_LOCAL_INFILE=1' na aba Advanced da conexao para permitir leitura dos arquivos

select * from operadoras;
select * from demonstracoes_contabeis;

-- Comando direto para importar operadoras
-- NOTA: Substitua este caminho pelo caminho real para seu arquivo
LOAD DATA LOCAL INFILE 'C:/Users/Matheus/Downloads/Dados_MySQL/Operadoras/Relatorio_cadop.csv'
INTO TABLE operadoras
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
    (registro_ans, 
    cnpj, 
    razao_social, 
    nome_fantasia, 
    modalidade, 
    logradouro,numero, 
    complemento, 
    bairro,
    cidade,
    uf,
    cep,
    ddd,
    telefone,
    fax,
    email,
    representante,
    cargo_representante,
    regiao_comercializacao,
    data_registro_ANS);

-- Comando direto para importar demonstrações contábeis
-- NOTA: Substitua este caminho pelo caminho real para seu arquivo
LOAD DATA LOCAL INFILE 'C:/Users/Matheus/Downloads/Dados_MySQL/1T2024.csv' INTO TABLE demonstracoes_contabeis FIELDS TERMINATED BY ';' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS
	(data_referencia,
    registro_ans,
    conta_contabil,
    descricao,
    valor_saldo_inicial,
    valor_saldo_final);
    
LOAD DATA LOCAL INFILE 'C:/Users/Matheus/Downloads/Dados_MySQL/2T2024.csv' INTO TABLE demonstracoes_contabeis FIELDS TERMINATED BY ';' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS
	(data_referencia,
    registro_ans,
    conta_contabil,
    descricao,
    valor_saldo_inicial,
    valor_saldo_final);
    
LOAD DATA LOCAL INFILE 'C:/Users/Matheus/Downloads/Dados_MySQL/3T2024.csv' INTO TABLE demonstracoes_contabeis FIELDS TERMINATED BY ';' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS
	(data_referencia,
    registro_ans,
    conta_contabil,
    descricao,
    valor_saldo_inicial,
    valor_saldo_final);
    
LOAD DATA LOCAL INFILE 'C:/Users/Matheus/Downloads/Dados_MySQL/4T2024.csv' INTO TABLE demonstracoes_contabeis FIELDS TERMINATED BY ';' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS
	(data_referencia,
    registro_ans,
    conta_contabil,
    descricao,
    valor_saldo_inicial,
    valor_saldo_final);

LOAD DATA LOCAL INFILE 'C:/Users/Matheus/Downloads/Dados_MySQL/1T2023.csv' INTO TABLE demonstracoes_contabeis FIELDS TERMINATED BY ';' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS
	(data_referencia,
    registro_ans,
    conta_contabil,
    descricao,
    valor_saldo_inicial,
    valor_saldo_final);
    
LOAD DATA LOCAL INFILE 'C:/Users/Matheus/Downloads/Dados_MySQL/2T2023.csv' INTO TABLE demonstracoes_contabeis FIELDS TERMINATED BY ';' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS
	(data_referencia,
    registro_ans,
    conta_contabil,
    descricao,
    valor_saldo_inicial,
    valor_saldo_final);
    
LOAD DATA LOCAL INFILE 'C:/Users/Matheus/Downloads/Dados_MySQL/3T2023.csv' INTO TABLE demonstracoes_contabeis FIELDS TERMINATED BY ';' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS
	(data_referencia,
    registro_ans,
    conta_contabil,
    descricao,
    valor_saldo_inicial,
    valor_saldo_final);
    
LOAD DATA LOCAL INFILE 'C:/Users/Matheus/Downloads/Dados_MySQL/4T2023.csv' INTO TABLE demonstracoes_contabeis FIELDS TERMINATED BY ';' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS
	(data_referencia,
    registro_ans,
    conta_contabil,
    descricao,
    valor_saldo_inicial,
    valor_saldo_final);


-- View para 10 operadoras com maiores despesas no último trimestre
CREATE OR REPLACE VIEW top_10_despesas_trimestre AS
SELECT 
    o.registro_ans,
    o.razao_social,
    o.nome_fantasia,
    o.modalidade,
    ABS(dc.valor_saldo_final) AS despesa_total
FROM 
    demonstracoes_contabeis dc
JOIN 
    operadoras o ON dc.registro_ans = o.registro_ans
WHERE 
    dc.data_referencia = (SELECT MAX(data_referencia) FROM demonstracoes_contabeis) -- Último trimestre disponível
    AND (
        dc.conta_contabil LIKE '411%'
        OR dc.descricao LIKE '%EVENTO%MÉDICO%' 
        OR dc.descricao LIKE '%SINISTR%MÉDICO%'
        OR dc.descricao LIKE '%ASSISTÊNCIA A SAÚDE%'
    )
ORDER BY 
    despesa_total DESC
LIMIT 10;

-- View para 10 operadoras com maiores despesas no último ano
CREATE OR REPLACE VIEW top_10_despesas_ano AS
SELECT 
    o.registro_ans,
    o.razao_social,
    o.nome_fantasia,
    o.modalidade,
    SUM(ABS(dc.valor_saldo_final)) AS despesa_anual
FROM 
    demonstracoes_contabeis dc
JOIN 
    operadoras o ON dc.registro_ans = o.registro_ans
WHERE 
    YEAR(dc.data_referencia) = 2024
    AND (
        dc.conta_contabil LIKE '411%'
        OR dc.descricao LIKE '%EVENTO%MÉDICO%' 
        OR dc.descricao LIKE '%SINISTR%MÉDICO%'
        OR dc.descricao LIKE '%ASSISTÊNCIA A SAÚDE%'
    )
GROUP BY 
    o.registro_ans, o.razao_social, o.nome_fantasia, o.modalidade
ORDER BY 
    despesa_anual DESC
LIMIT 10;

-- Consultar resultados
SELECT * FROM top_10_despesas_trimestre;
SELECT * FROM top_10_despesas_ano;