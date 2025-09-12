from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Conexão com o banco
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Coloque sua senha do MySQL
        database="petshop"
    )

# --------------------------
# Página inicial - lista pets
# --------------------------
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT pets.id, pets.nome, pets.tipo, pets.idade, tutores.nome
        FROM pets
        LEFT JOIN tutores ON pets.tutor_id = tutores.id
    ''')
    pets = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', pets=pets)

# --------------------------
# Formulário de cadastro
# --------------------------
@app.route('/cadastrar_pet')
def cadastrar_pet():
    return render_template('cadastrar_pet.html')

# --------------------------
# Adicionar pet
# --------------------------
@app.route('/adicionar_pet', methods=['POST'])
def adicionar_pet():
    nome = request.form['nome']
    tipo = request.form['tipo']
    idade = request.form['idade']
    tutor_nome = request.form['tutor_nome']

    conn = get_db_connection()
    cursor = conn.cursor()

    # Verifica se o tutor já existe
    cursor.execute('SELECT id FROM tutores WHERE nome = %s', (tutor_nome,))
    tutor = cursor.fetchone()

    if tutor:
        tutor_id = tutor[0]
    else:
        cursor.execute('INSERT INTO tutores (nome) VALUES (%s)', (tutor_nome,))
        conn.commit()
        tutor_id = cursor.lastrowid

    # Adiciona o pet
    cursor.execute(
        'INSERT INTO pets (nome, tipo, idade, tutor_id) VALUES (%s, %s, %s, %s)',
        (nome, tipo, idade, tutor_id)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/')

# --------------------------
# Tela de edição de pet
# --------------------------
@app.route('/editar_pet/<int:id>', methods=['GET'])
def editar_pet(id):
    conn = get_db_connection()
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

# --------------------------
# Atualizar pet
# --------------------------
@app.route('/atualizar_pet/<int:id>', methods=['POST'])
def atualizar_pet(id):
    nome = request.form['nome']
    tipo = request.form['tipo']
    idade = request.form['idade']
    tutor_nome = request.form['tutor_nome']

    conn = get_db_connection()
    cursor = conn.cursor()

    # Verifica se tutor existe
    cursor.execute('SELECT id FROM tutores WHERE nome = %s', (tutor_nome,))
    tutor = cursor.fetchone()
    if tutor:
        tutor_id = tutor[0]
    else:
        cursor.execute('INSERT INTO tutores (nome) VALUES (%s)', (tutor_nome,))
        conn.commit()
        tutor_id = cursor.lastrowid

    # Atualiza o pet
    cursor.execute('''
        UPDATE pets
        SET nome = %s, tipo = %s, idade = %s, tutor_id = %s
        WHERE id = %s
    ''', (nome, tipo, idade, tutor_id, id))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/')

# --------------------------
# Excluir pet
# --------------------------
@app.route('/excluir_pet/<int:id>', methods=['POST'])
def excluir_pet(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM pets WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/')

# --------------------------
# Rodar o app
# --------------------------
if __name__ == '__main__':
    app.run(debug=True)
