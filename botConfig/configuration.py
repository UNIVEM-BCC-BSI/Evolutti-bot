from flask import Flask, render_template, request
import json
import webbrowser
import os

app = Flask(__name__, template_folder="template_folder", static_url_path='/static')

# Função para carregar as configurações a partir do arquivo JSON
def carregar_config():
    with open('messages.json', 'r') as config_file:
        return json.load(config_file)

# Rota para a página inicial
@app.route('/')
def index():
    config = carregar_config()
    return render_template('index.html', config=config)

# Rota para atualizar as configurações
@app.route('/atualizar', methods=['POST'])
def atualizar():
    # Obter os valores do formulário
    novo_config = {
        "menu_saudacao": request.form.get('menu_saudacao'),
        "opt_1": request.form.get('opt_1'),
        "opt_2": request.form.get('opt_2'),
        "opt_3": request.form.get('opt_3'),
        "opt_4": request.form.get('opt_4'),
        "opt_5": request.form.get('opt_5'),
        "opt_6": request.form.get('opt_6'),
        "retorno": request.form.get('retorno'),
    }

    # Salvar as configurações no arquivo JSON
    with open('messages.json', 'w', encoding='utf-8') as config_file:
        json.dump(novo_config, config_file, indent=4)

    return render_template('update.html')

# Rota para desligar o servidor
@app.route('/desligar', methods=['POST'])
def desligar_servidor():
    os._exit(0)

if __name__ == '__main__':
    # Abre o navegador no momento da inicialização
    webbrowser.open_new('http://localhost:5000')

    app.run(debug=True)
