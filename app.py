from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Função para criar conexão a cada requisição
def get_db():
    return mysql.connector.connect(
        host="localhost",
        database="petshop",
        user="root",
        password=""
    )

# ---------------- PETS ----------------
@app.route('/')
def home():
    return render_template('home_menu.html')


@app.route('/pets')
def listar_pets():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM pets")
    pets = cur.fetchall()
    cur.close()
    db.close()
    return render_template('listar_pets.html', pets=pets)


@app.route('/novo_pet')
def novo_pet():
    return render_template('cadastrar_pet.html')


@app.route('/salvar_pet', methods=['POST'])
def salvar_pet():
    nome = request.form['nome']
    tipo = request.form.get('tipo')
    idade = request.form.get('idade')
    tutor_nome = request.form['tutor_nome']

    db = get_db()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO pets (nome, tipo, idade, tutor_nome) VALUES (%s, %s, %s, %s)",
        (nome, tipo, idade, tutor_nome)
    )
    db.commit()
    cur.close()
    db.close()
    return redirect(url_for('listar_pets'))


@app.route('/editar_pet/<int:id>')
def editar_pet(id):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM pets WHERE id=%s", (id,))
    pet = cur.fetchone()
    cur.close()
    db.close()
    return render_template('editar_pet.html', pet=pet)


@app.route('/atualizar_pet/<int:id>', methods=['POST'])
def atualizar_pet(id):
    nome = request.form['nome']
    tipo = request.form.get('tipo')
    idade = request.form.get('idade')
    tutor_nome = request.form['tutor_nome']

    db = get_db()
    cur = db.cursor()
    cur.execute(
        "UPDATE pets SET nome=%s, tipo=%s, idade=%s, tutor_nome=%s WHERE id=%s",
        (nome, tipo, idade, tutor_nome, id)
    )
    db.commit()
    cur.close()
    db.close()
    return redirect(url_for('listar_pets'))


@app.route('/deletar_pet/<int:id>', methods=['POST'])
def deletar_pet(id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM pets WHERE id=%s", (id,))
    db.commit()
    cur.close()
    db.close()
    return redirect(url_for('listar_pets'))


# ---------------- CONSULTAS ----------------

@app.route('/consultas')
def listar_consultas():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("""
        SELECT id, pet_nome, vet_nome, data_consulta, horario, observacoes
        FROM consultas
        ORDER BY data_consulta, horario
    """)
    consultas = cur.fetchall()
    cur.close()
    db.close()
    return render_template('listar_consultas.html', consultas=consultas)


@app.route('/nova_consulta')
def nova_consulta():
    return render_template('cadastrar_consulta.html')


@app.route('/salvar_consulta', methods=['POST'])
def salvar_consulta():
    pet_nome = request.form.get('pet_nome', 'Desconhecido')
    vet_nome = request.form.get('vet_nome', 'Veterinário(a)')
    data_consulta = request.form['data_consulta']
    horario = request.form['horario']
    observacoes = request.form.get('observacoes', '')

    db = get_db()
    cur = db.cursor()
    cur.execute("""
        INSERT INTO consultas (pet_nome, vet_nome, data_consulta, horario, observacoes)
        VALUES (%s, %s, %s, %s, %s)
    """, (pet_nome, vet_nome, data_consulta, horario, observacoes))

    db.commit()
    cur.close()
    db.close()
    return redirect(url_for('listar_consultas'))


@app.route('/editar_consulta/<int:id>')
def editar_consulta(id):
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("""
        SELECT id, pet_nome, vet_nome, data_consulta, horario, observacoes
        FROM consultas WHERE id=%s
    """, (id,))
    
    consulta = cur.fetchone()
    cur.close()
    db.close()

    if not consulta:
        return redirect(url_for('listar_consultas'))

    return render_template('editar_consulta.html', consulta=consulta)


@app.route('/atualizar_consulta/<int:id>', methods=['POST'])
def atualizar_consulta(id):
    pet_nome = request.form.get('pet_nome', 'Desconhecido')
    vet_nome = request.form.get('vet_nome', 'Veterinário(a)')
    data_consulta = request.form['data_consulta']
    horario = request.form['horario']
    observacoes = request.form.get('observacoes', '')

    db = get_db()
    cur = db.cursor()
    cur.execute("""
        UPDATE consultas
        SET pet_nome=%s, vet_nome=%s, data_consulta=%s, horario=%s, observacoes=%s
        WHERE id=%s
    """, (pet_nome, vet_nome, data_consulta, horario, observacoes, id))

    db.commit()
    cur.close()
    db.close()
    return redirect(url_for('listar_consultas'))


@app.route('/deletar_consulta/<int:id>', methods=['POST'])
def deletar_consulta(id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM consultas WHERE id=%s", (id,))
    db.commit()
    cur.close()
    db.close()
    return redirect(url_for('listar_consultas'))


if __name__ == '__main__':
    app.run(debug=True)
