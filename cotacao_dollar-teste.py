from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import pandas as pd
import psycopg2
import time
from datetime import datetime

try:
#conexao db
    conexao = psycopg2.connect(user="avnadmin", password="AVNS_soL4IKAZqbRQwbx06Jb",
                                host="devops-postgresql-pipeline-banco-postgresql-devops.e.aivencloud.com",
                                port="24043",
                                database="dbcotacao")

    print("Conexão bem-sucedida!")
except psycopg2.Error as e:
    print("Erro ao conectar ao banco de dados:", e)
cursor = conexao.cursor()

# Abrir o navegador Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
time.sleep(4)

driver.get("https://g.co/kgs/UGYy5mT")
time.sleep(2)

dollar_element = driver.find_element(By.XPATH, '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]')
dollar = dollar_element.text
dollar = dollar.replace(',', '.')
dollar = float(dollar)

# Horario atual
data = datetime.now().strftime("%Y-%m-%d")
horario = datetime.now().strftime("%H:%M:%S")

try:
    query = """
    CALL inserir_cotacao_dolar(%s, %s, %s)
    """
    valores = (data, horario, dollar)
    cursor.execute(query, valores)
    conexao.commit()  # Commit the transaction if needed
  
    select_query = f"SELECT * FROM data;"
  
    cursor.execute(select_query)
    registros = cursor.fetchall()
    colunas = [desc[0] for desc in cursor.description]

    tabela = pd.DataFrame(registros, columns=colunas)
    print(tabela)
except Exception as e:
    print(f"Error executing stored procedure: {e}")
    conexao.rollback()  # Rollback in case of error
finally:
    cursor.close()
    conexao.close()
