from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="petshop"
    )

@app.route('/')
def home():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT pets.id, pets.nome, pets.tipo, pets.idade, tutores.nome
        FROM pets
        LEFT JOIN tutores ON pets.tutor_id = tutores.id
    ''')
    lista_pets = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', pets=lista_pets)

@app.route('/novo_pet')
def novo_pet():
    return render_template('cadastrar_pet.html')

@app.route('/salvar_pet', methods=['POST'])
def salvar_pet():
    nome = request.form['nome']
    tipo = request.form['tipo']
    idade = request.form['idade']
    tutor_nome = request.form['tutor_nome']

    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM tutores WHERE nome = %s', (tutor_nome,))
    tutor = cursor.fetchone()
    if tutor:
        tutor_id = tutor[0]
    else:
        cursor.execute('INSERT INTO tutores (nome) VALUES (%s)', (tutor_nome,))
        conn.commit()
        tutor_id = cursor.lastrowid

    cursor.execute(
        'INSERT INTO pets (nome, tipo, idade, tutor_id) VALUES (%s, %s, %s, %s)',
        (nome, tipo, idade, tutor_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/')

@app.route('/editar/<int:id>')
def editar(id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT pets.id, pets.nome, pets.tipo, pets.idade, tutores.nome
        FROM pets
        LEFT JOIN tutores ON pets.tutor_id = tutores.id
        WHERE pets.id = %s
    ''', (id,))
    pet = cursor.fetchone()
    cursor.close()
    conn.close()
    if pet:
        return render_template('editar_pet.html', pet=pet)
    return redirect('/')

@app.route('/atualizar/<int:id>', methods=['POST'])
def atualizar(id):
    nome = request.form['nome']
    tipo = request.form['tipo']
    idade = request.form['idade']
    tutor_nome = request.form['tutor_nome']

    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM tutores WHERE nome = %s', (tutor_nome,))
    tutor = cursor.fetchone()
    if tutor:
        tutor_id = tutor[0]
    else:
        cursor.execute('INSERT INTO tutores (nome) VALUES (%s)', (tutor_nome,))
        conn.commit()
        tutor_id = cursor.lastrowid

    cursor.execute('''
        UPDATE pets
        SET nome=%s, tipo=%s, idade=%s, tutor_id=%s
        WHERE id=%s
    ''', (nome, tipo, idade, tutor_id, id))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/')

@app.route('/deletar/<int:id>', methods=['POST'])
def deletar(id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM pets WHERE id=%s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
