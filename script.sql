CREATE TABLE cotacao_dolar (
    id SERIAL PRIMARY KEY,
    data DATE,
    hora TIME,
    cotacao DECIMAL(10, 2)
);

CREATE OR REPLACE PROCEDURE inserir_cotacao_dolar(
    data_param DATE,
    hora_param TIME,
    cotacao_param DECIMAL
) AS
$$
BEGIN
    INSERT INTO cotacao_dolar (data, hora, cotacao)
    VALUES (data_param, hora_param, cotacao_param);
    
    RAISE NOTICE 'Dados inseridos com sucesso: Data=%, Hora=%, Cotação=%', data_param, hora_param, cotacao_param;
END;
$$ LANGUAGE plpgsql;

--call inserir_cotacao_dolar('2024-06-22', '07:18:01', 5.44)