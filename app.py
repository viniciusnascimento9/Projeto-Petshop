from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Conexão com MySQL — ajuste host/database/usuário/senha se necessário
db = mysql.connector.connect(
    host="localhost",
    database="petshop"
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

# ---- mostrar formulário de nova consulta (GET) ----
@app.route('/nova_consulta')
def nova_consulta():
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT id, nome FROM pets")
    pets = cur.fetchall()   # lista de dicts: [{'id': ..., 'nome': ...}, ...]
    cur.close()
    return render_template('cadastrar_consulta.html', pets=pets)

# ---- salvar consulta (POST) ----
@app.route('/salvar_consulta', methods=['POST'])
def salvar_consulta():
    pet_id = request.form.get('pet_id')
    data_consulta = request.form['data_consulta']
    horario = request.form['horario']
    observacoes = request.form.get('observacoes', '')
    vet_nome = request.form.get('vet_nome', 'Vetrinário(a)')

    cur = db.cursor()
    pet_nome = "Desconhecido"
    if pet_id:
        cur.execute("SELECT nome FROM pets WHERE id=%s", (pet_id,))
        r = cur.fetchone()
        pet_nome = r[0] if r else "Desconhecido"

    cur.execute(
        "INSERT INTO consultas (pet_nome, vet_nome, data_consulta, horario, observacoes) VALUES (%s,%s,%s,%s,%s)",
        (pet_nome, vet_nome, data_consulta, horario, observacoes)
    )
    db.commit()
    cur.close()
    return redirect(url_for('listar_consultas'))

# ---- editar consulta (GET) ----
@app.route('/editar_consulta/<int:id>')
def editar_consulta(id):
    cur = db.cursor(dictionary=True)
    cur.execute(
        "SELECT id, pet_nome, vet_nome, data_consulta, horario, observacoes FROM consultas WHERE id=%s",
        (id,)
    )
    consulta = cur.fetchone()
    if not consulta:
        cur.close()
        return redirect(url_for('listar_consultas'))

    cur2 = db.cursor()
    cur2.execute("SELECT id, nome FROM pets")
    pets = cur2.fetchall()
    cur.close()
    cur2.close()

    # encontrar pet_id baseado no pet_nome atual
    pet_id_selecionado = None
    for p in pets:
        if p[1] == consulta['pet_nome']:
            pet_id_selecionado = p[0]
            break

    return render_template('editar_consulta.html', consulta=consulta, pets=pets, pet_id_selecionado=pet_id_selecionado)

# ---- atualizar consulta (POST) ----
@app.route('/atualizar_consulta/<int:id>', methods=['POST'])
def atualizar_consulta(id):
    pet_id = request.form.get('pet_id')
    vet_nome = request.form.get('vet_nome', 'Veterinário(a)')
    data_consulta = request.form['data_consulta']
    horario = request.form['horario']
    observacoes = request.form.get('observacoes', '')

    cur = db.cursor()
    pet_nome = None
    if pet_id:
        cur.execute("SELECT nome FROM pets WHERE id=%s", (pet_id,))
        r = cur.fetchone()
        pet_nome = r[0] if r else None

    if not pet_nome:
        cur.execute("SELECT pet_nome FROM consultas WHERE id=%s", (id,))
        r = cur.fetchone()
        pet_nome = r[0] if r else "Desconhecido"

    cur.execute(
        "UPDATE consultas SET pet_nome=%s, vet_nome=%s, data_consulta=%s, horario=%s, observacoes=%s WHERE id=%s",
        (pet_nome, vet_nome, data_consulta, horario, observacoes, id)
    )
    db.commit()
    cur.close()
    return redirect(url_for('listar_consultas'))

# ---- deletar consulta (POST) ----
@app.route('/deletar_consulta/<int:id>', methods=['POST'])
def deletar_consulta(id):
    cur = db.cursor()
    cur.execute("DELETE FROM consultas WHERE id=%s", (id,))
    db.commit()
    cur.close()
    return redirect(url_for('listar_consultas'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
