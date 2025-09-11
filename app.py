from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Formulário de cadastro de pet
@app.route('/cadastrar_pet')
def cadastrar_pet():
    return render_template('cadastrar_pet.html')

# Rota que recebe os dados do formulário e salva no banco
@app.route('/adicionar_pet', methods=['POST'])
def adicionar_pet():
    nome = request.form['nome']
    tipo = request.form['tipo']
    idade = request.form['idade']
    tutor_id = request.form['tutor_id']

    conn = sqlite3.connect('petshop.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO pets (nome, tipo, idade, tutor_id) VALUES (?, ?, ?, ?)',
                   (nome, tipo, idade, tutor_id))
    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
