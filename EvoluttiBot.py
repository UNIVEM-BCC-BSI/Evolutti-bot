from playwright.sync_api import sync_playwright
import time
from datetime import date, datetime
import re
import sqlite3
import json 
# -----------------------------------------------------

# Carrega o arquivo JSON de mensagens em um dicionário
with open('botConfig/messages.json', 'r') as arquivo:
    mensagens = json.load(arquivo)


with sync_playwright() as p:

    # abre o navegador chormium
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # Vai para a pagina do whatsapp web
    page.goto("https://web.whatsapp.com/")

    # No whatsapp:
    page.locator('//*[@id="side"]/div[1]/div/button/div/span').click()

    while page:
        time.sleep(5)
        current_date = date.today()

        try:
            page.wait_for_selector('._2H6nH').click()

            nome_real = "~"

            # pega o telefone
            array_phone = page.locator(
                '//*[@id="main"]/header/div[2]/div/div/div/span').all_text_contents()
            phone_no_spaces = array_phone[0].replace(
                " ", "")  # Removendo os espaços em branco
            p = phone_no_spaces.replace("-", "")  # Removendo "-"       
            phone = p.replace("+", "")  # Removendo "+"

            # captando as ultimas mensagens do chat
            for i in range(1):
                elements = page.query_selector_all(
                    '.CzM4m')  # Array com as ultimas mensagens

            text = elements[-1].text_content()  # pega a ultima mensagem
            print(text)
            lastMessage = text[:-10]
            print(lastMessage)
            # -----------------------------------------------------------------------------------------------------------------
            # Conecta ao banco de dados
            
            try:
                connect = sqlite3.connect("database.db")
                cursor = connect.cursor()
                cursor.execute(
                    '''CREATE TABLE IF NOT EXISTS atendimento (id INTEGER PRIMARY KEY, apoio TEXT, telefone TEXT, mensagem TEXT)''')
                cursor.execute(
                    "INSERT INTO atendimento (apoio, telefone, mensagem) VALUES (?, ?, ?)", (nome_real, phone, lastMessage))

                cursor.execute(
                    '''CREATE TABLE IF NOT EXISTS processo_atendimento (id INTEGER PRIMARY KEY, apoio TEXT, telefone TEXT, IDD TEXT, status TEXT)''')
                
                cursor.execute("SELECT * FROM processo_atendimento WHERE IDD = ?", (str(current_date)+str(phone),))
                if len(cursor.fetchall()) == 0:
                    cursor.execute(
                    "INSERT INTO processo_atendimento (apoio, telefone, IDD, status) VALUES (?, ?, ?, ?)", (nome_real, phone, str(current_date)+str(phone), 'Aguardando'))

                connect.commit()
            # -----------------------------------------------------------------------------------------------------------------
                select = cursor.execute("SELECT apoio, telefone, IDD, status FROM processo_atendimento WHERE IDD = ?", (str(current_date)+str(phone),))
                results = cursor.fetchall()

            except Exception as e:
                print("Ocorreu um erro")
                break
            finally:
                cursor.close()
                connect.close()

            for result in results:
                print(result)
                result[0] # Nome
                result[1] # Telefone
                result[2] # IDD
                result[3] # Status
            
            if str(result[3]) == 'Aguardando': # Intro
                message = mensagens["menu_saudacao"]
                atualizar1 = 'Esperando Opcao'
                atualizar2 = lastMessage
                atualizar3 = lastMessage

                campo1 = 'status'
                campo2 = 'apoio'
                campo3 = 'apoio2'
            
            elif str(result[3]) == 'Esperando Opcao' and str(lastMessage) == "1": # Opt 1
                message = mensagens["opt_1"]

            elif str(result[3]) == 'Esperando Opcao' and str(lastMessage) == "2": # Opt 2
                message = mensagens["opt_2"]

            elif str(result[3]) == 'Esperando Opcao' and str(lastMessage) == "3": # Opt 3
                message = mensagens["opt_3"]

            elif str(result[3]) == 'Esperando Opcao' and str(lastMessage) == "4": # Opt 4
                message = mensagens["opt_4"]

            elif str(result[3]) == 'Esperando Opcao' and str(lastMessage) == "5": # Opt 5
                message = mensagens["opt_5"]

            elif str(result[3]) == 'Esperando Opcao' and str(lastMessage) == "6": # Opt 6
                message = mensagens["opt_6"]

            else:
                message = mensagens["retorno"]

            page.locator(
                '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div/p').fill(str(message))

            page.keyboard.press('Enter')

            page.locator(
                '//*[@id="main"]/header/div[3]/div/div[3]/div/div/span').click()
            page.locator(
                '//*[@id="app"]/div/span[4]/div/ul/div/div/li[3]/div').click()
            
            if lastMessage != str('1'):
                try:
                    connect = sqlite3.connect("database.db")
                    cursor = connect.cursor()

                    cursor.execute("UPDATE processo_atendimento SET status = ?, apoio = ? WHERE IDD LIKE ?", (atualizar1, lastMessage, '%' + str(result[2]) + '%'))
                    connect.commit()
                    connect.close()
                    cursor.close()
                except:
                    connect.close()
                    cursor.close()
                continue

        except:
            time.sleep(1)
            continue