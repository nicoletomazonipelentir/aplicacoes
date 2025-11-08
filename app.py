import os
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

app = Flask(__name__)

# Conexão com o banco MongoDB Atlas
#client = MongoClient("mongodb+srv://aplicacoes_db:CokMfv13XUavZxiA@cluster0.xshcr4u.mongodb.net/?appName=Cluster0")
# db = client["antidoping"]
# atletas = db["atletas"]
# exames = db["exames"]

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
print("String de conexão:", mongo_uri)

db = client["antidoping"]
atletas = db["atletas"]
exames = db["exames"]

@app.route('/')
def index():
    return render_template('index.html')

# ---- ROTAS DE ATLETAS ----
@app.route('/atletas')
def listar_atletas():
    lista = list(atletas.find())
    return render_template('atletas.html', atletas=lista)

@app.route('/novo_atleta', methods=['POST'])
def novo_atleta():
    nome = request.form['nome']
    idade = request.form['idade']
    clube = request.form['clube']
    posicao = request.form['posicao']
    atletas.insert_one({
        'nome': nome,
        'idade': idade,
        'clube': clube,
        'posicao': posicao
    })
    
    return redirect('/atletas')

# ---- ROTAS DE EXAMES ----
@app.route('/exames')
def listar_exames():
    lista = list(exames.find())
    atletas_lista = list(atletas.find())
    return render_template('exames.html', exames=lista, atletas=atletas_lista)

@app.route('/novo_exame', methods=['POST'])
def novo_exame():
    atleta = request.form['atleta']
    data = request.form['data']
    resultado = request.form['resultado']
    obs = request.form['obs']
    exames.insert_one({
        'atleta': atleta,
        'data': data,
        'resultado': resultado,
        'obs': obs
    })
    return redirect('/exames')

if __name__ == '__main__':
    app.run(debug=True)
