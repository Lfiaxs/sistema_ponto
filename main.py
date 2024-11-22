from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # Permite que o React acesse os endpoints

# Listar Colaboradores
@app.route("/colaboradores", methods=["GET"])
def listar_colaboradores():
    conn = sqlite3.connect("db/registro_ponto.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM colaboradores")
    colaboradores = cursor.fetchall()
    conn.close()
    return jsonify([{"id": colab[0], "nome": colab[1]} for colab in colaboradores])

# Listar Registros de Ponto
@app.route("/registros", methods=["GET"])
def listar_registros():
    conn = sqlite3.connect("db/registro_ponto.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT registros.id, colaboradores.nome, registros.hora_registro
    FROM registros
    INNER JOIN colaboradores ON registros.colaborador_id = colaboradores.id
    """)
    registros = cursor.fetchall()
    conn.close()
    return jsonify([{"id_registro": reg[0], "nome": reg[1], "hora": reg[2]} for reg in registros])

# Adicionar Colaborador
@app.route("/colaboradores", methods=["POST"])
def adicionar_colaborador():
    data = request.json
    nome = data.get("nome")
    conn = sqlite3.connect("db/registro_ponto.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO colaboradores (nome) VALUES (?)", (nome,))
    conn.commit()
    conn.close()
    return jsonify({"message": f"Colaborador {nome} adicionado com sucesso!"}), 201

# Remover Colaborador
@app.route("/colaboradores/<int:id_colaborador>", methods=["DELETE"])
def remover_colaborador(id_colaborador):
    conn = sqlite3.connect("db/registro_ponto.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM colaboradores WHERE id = ?", (id_colaborador,))
    conn.commit()
    conn.close()
    return jsonify({"message": f"Colaborador ID {id_colaborador} removido com sucesso!"})

if __name__ == "__main__":
    app.run(debug=True)