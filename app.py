from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)

DB_PATH = "backend/db/registro_ponto.db"

# Função para conexão com o banco
def conectar_banco():
    conn = sqlite3.connect(DB_PATH)
    return conn, conn.cursor()

# Rota de login
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    nome = data.get("nome")
    senha = data.get("senha")

    conn, cursor = conectar_banco()
    cursor.execute("SELECT id, tipo FROM usuarios WHERE nome = ? AND senha = ?", (nome, senha))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"id": user[0], "tipo": user[1]}), 200
    return jsonify({"error": "Credenciais inválidas"}), 401

# Rota para registrar ponto
@app.route("/registrar_ponto", methods=["POST"])
def registrar_ponto():
    data = request.json
    colaborador_id = data.get("colaborador_id")
    hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn, cursor = conectar_banco()
    cursor.execute("INSERT INTO registros (colaborador_id, hora_registro) VALUES (?, ?)", (colaborador_id, hora))
    conn.commit()
    conn.close()

    return jsonify({"message": "Ponto registrado com sucesso!", "hora": hora}), 201

# Rota para listar colaboradores
@app.route("/colaboradores", methods=["GET"])
def listar_colaboradores():
    conn, cursor = conectar_banco()
    cursor.execute("SELECT * FROM colaboradores")
    colaboradores = cursor.fetchall()
    conn.close()

    return jsonify([{"id": colab[0], "nome": colab[1]} for colab in colaboradores])

# Rota para adicionar colaborador
@app.route("/colaboradores", methods=["POST"])
def adicionar_colaborador():
    data = request.json
    nome = data.get("nome")

    conn, cursor = conectar_banco()
    cursor.execute("INSERT INTO colaboradores (nome) VALUES (?)", (nome,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Colaborador adicionado com sucesso!"}), 201

# Rota para remover colaborador
@app.route("/colaboradores/<int:id>", methods=["DELETE"])
def remover_colaborador(id):
    conn, cursor = conectar_banco()
    cursor.execute("DELETE FROM colaboradores WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Colaborador removido com sucesso!"}), 200

# Rota para editar colaborador
@app.route("/colaboradores/<int:id>", methods=["PUT"])
def editar_colaborador(id):
    data = request.json
    nome = data.get("nome")

    conn, cursor = conectar_banco()
    cursor.execute("UPDATE colaboradores SET nome = ? WHERE id = ?", (nome, id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Colaborador atualizado com sucesso!"}), 200

if __name__ == "__main__":
    app.run(debug=True)
