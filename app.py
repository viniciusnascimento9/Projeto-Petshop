from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Função para conectar ao banco MySQL
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",       # coloque aqui o usuário do MySQL
        password="",       # se definiu senha, coloque aqui
        database="petshop"
    )

# Rota inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para exibir o formulário de cadastro
@app.route('/cadastrar_pet')
def cadastrar_pet():
    return render_template('cadastrar_pet.html')

# Rota para adicionar pet no banco
@app.route('/adicionar_pet', methods=['POST'])
def adicionar_pet():
    nome = request.form['nome']
    tipo = request.form['tipo']
    idade = request.form['idade']
    tutor_id = request.form['tutor_id']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        'INSERT INTO pets (nome, tipo, idade, tutor_id) VALUES (%s, %s, %s, %s)',
        (nome, tipo, idade, tutor_id)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)