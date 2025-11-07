from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
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
    cur = db.cursor()
    cur.execute("SELECT * FROM pets")
    pets = cur.fetchall()
    cur.close()
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
    cur = db.cursor()
    cur.execute(
        "INSERT INTO pets (nome, tipo, idade, tutor_nome) VALUES (%s,%s,%s,%s)",
        (nome, tipo, idade, tutor_nome)
    )
    db.commit()
    cur.close()
    return redirect(url_for('listar_pets'))

@app.route('/editar_pet/<int:id>')
def editar_pet(id):
    cur = db.cursor()
    cur.execute("SELECT * FROM pets WHERE id=%s", (id,))
    pet = cur.fetchone()
    cur.close()
    return render_template('editar_pet.html', pet=pet)

@app.route('/atualizar_pet/<int:id>', methods=['POST'])
def atualizar_pet(id):
    nome = request.form['nome']
    tipo = request.form.get('tipo')
    idade = request.form.get('idade')
    tutor_nome = request.form['tutor_nome']
    cur = db.cursor()
    cur.execute(
        "UPDATE pets SET nome=%s, tipo=%s, idade=%s, tutor_nome=%s WHERE id=%s",
        (nome, tipo, idade, tutor_nome, id)
    )
    db.commit()
    cur.close()
    return redirect(url_for('listar_pets'))

@app.route('/deletar_pet/<int:id>', methods=['POST'])
def deletar_pet(id):
    cur = db.cursor()
    cur.execute("DELETE FROM pets WHERE id=%s", (id,))
    db.commit()
    cur.close()
    return redirect(url_for('listar_pets'))

# ---------------- CONSULTAS ----------------
@app.route('/consultas')
def listar_consultas():
    cur = db.cursor(dictionary=True)
    cur.execute(
        "SELECT id, pet_nome, vet_nome, data_consulta, horario, observacoes FROM consultas ORDER BY data_consulta, horario"
    )
    consultas = cur.fetchall()
    cur.close()
    return render_template('listar_consultas.html', consultas=consultas)

@app.route('/nova_consulta')
def nova_consulta():
    return render_template('cadastrar_consulta.html')


@app.route('/salvar_consulta', methods=['POST'])
def salvar_consulta():
    pet_nome = request.form.get('pet_nome', 'Desconhecido')
    data_consulta = request.form['data_consulta']
    horario = request.form['horario']
    observacoes = request.form.get('observacoes', '')
    vet_nome = request.form.get('vet_nome', 'Veterinário(a)')

    cur = db.cursor()
    cur.execute(
        "INSERT INTO consultas (pet_nome, vet_nome, data_consulta, horario, observacoes) VALUES (%s,%s,%s,%s,%s)",
        (pet_nome, vet_nome, data_consulta, horario, observacoes)
    )
    db.commit()
    cur.close()
    return redirect(url_for('listar_consultas'))

@app.route('/editar_consulta/<int:id>')
def editar_consulta(id):
    cur = db.cursor(dictionary=True)
    cur.execute(
        "SELECT id, pet_nome, vet_nome, data_consulta, horario, observacoes FROM consultas WHERE id=%s",
        (id,)
    )
    consulta = cur.fetchone()
    cur.close()
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

    cur = db.cursor()
    cur.execute(
        "UPDATE consultas SET pet_nome=%s, vet_nome=%s, data_consulta=%s, horario=%s, observacoes=%s WHERE id=%s",
        (pet_nome, vet_nome, data_consulta, horario, observacoes, id)
    )
    db.commit()
    cur.close()
    return redirect(url_for('listar_consultas'))


@app.route('/deletar_consulta/<int:id>', methods=['POST'])
def deletar_consulta(id):
    cur = db.cursor()
    cur.execute("DELETE FROM consultas WHERE id=%s", (id,))
    db.commit()
    cur.close()
    return redirect(url_for('listar_consultas'))



# ---------------- VETERINÁRIOS ----------------
@app.route('/veterinarios')
def listar_veterinarios():
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT id, nome, crmv, especialidade, telefone, email FROM vets")
    veterinarios = cur.fetchall()
    cur.close()
    return render_template('listar_veterinarios.html', veterinarios=veterinarios)


@app.route('/novo_veterinario')
def novo_veterinario():
    return render_template('cadastrar_veterinario.html')


@app.route('/salvar_veterinario', methods=['POST'])
def salvar_veterinario():
    nome = request.form['nome']
    crmv = request.form['crmv']
    especialidade = request.form['especialidade']
    telefone = request.form['telefone']
    email = request.form['email']

    cur = db.cursor()
    cur.execute(
        "INSERT INTO vets (nome, crmv, especialidade, telefone, email) VALUES (%s, %s, %s, %s, %s)",
        (nome, crmv, especialidade, telefone, email)
    )
    db.commit()
    cur.close()
    return redirect(url_for('listar_veterinarios'))


@app.route('/editar_veterinario/<int:id>')
def editar_veterinario(id):
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM vets WHERE id=%s", (id,))
    veterinario = cur.fetchone()
    cur.close()
    return render_template('editar_veterinario.html', veterinario=veterinario)


@app.route('/atualizar_veterinario/<int:id>', methods=['POST'])
def atualizar_veterinario(id):
    nome = request.form['nome']
    crmv = request.form['crmv']
    especialidade = request.form['especialidade']
    telefone = request.form['telefone']
    email = request.form['email']

    cur = db.cursor()
    cur.execute(
        "UPDATE vets SET nome=%s, crmv=%s, especialidade=%s, telefone=%s, email=%s WHERE id=%s",
        (nome, crmv, especialidade, telefone, email, id)
    )
    db.commit()
    cur.close()
    return redirect(url_for('listar_veterinarios'))


@app.route('/deletar_veterinario/<int:id>', methods=['POST'])
def deletar_veterinario(id):
    cur = db.cursor()
    cur.execute("DELETE FROM vets WHERE id=%s", (id,))
    db.commit()
    cur.close()
    return redirect(url_for('listar_veterinarios'))


if __name__ == '__main__':
    app.run(debug=True, port=5001)