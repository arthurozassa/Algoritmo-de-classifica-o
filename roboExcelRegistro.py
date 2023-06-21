# Algoritmo de classificação 
# Através de registros do Excel, a aplicação entra no registro.br, insere a informação 
# e se o domínio estiver disponível, grava no TXT.
# By Arthur Ozassa
# 10/06/2023
# Banco origem Excel: dominios.xlsx
# Destino TXT: resultado.txt

import pandas as pd


from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
import time
import xlrd
from webdriver_manager.chrome import ChromeDriverManager

print("Iniciando nosso robô...\n")
arq = open("resultado.txt", "w", encoding="utf-8")

dominios = []

# Abre e lê o Excel
# workbook = xlrd.open_workbook('./dominios.xlsx')
workbook = pd.read_excel('./dominios.xlsx', header=None)

dominios = workbook[0].values.tolist()


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

driver.get("https://registro.br/")

# dominios = ["uol.com.br", "wesleyteste.com.br", "globo.com.br"]
for dominio in dominios:
    pesquisa = driver.find_element(By.ID, 'is-avail-field')
    pesquisa.clear() #Limpando a barra de pesquisa
    pesquisa.send_keys(dominio)
    pesquisa.send_keys(Keys.RETURN)
    time.sleep(2)
    resultados = driver.find_elements(By.XPATH, '//*[@id="app"]/div/main/div/section/div[2]/div/p')
    print("Dominio %s %s" % (dominio, resultados[0].text))
    
    # Regra para gravar no TXT somente os domínios disponíveis para registro
    # if resultados[0].text == "Domínio disponível não para registro.":
    if resultados[0].text == "Domínio disponível para registro.":
        texto = "Dominio %s %s %s\n" % (dominio, "-" ,resultados[0].text)
        arq.write(texto)  

time.sleep(5)
arq.close()
driver.close()