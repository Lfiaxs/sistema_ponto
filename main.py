from datetime import datetime
import traceback
from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import subprocess
import os
from app.components.gerador_senha import gerar_senha


app = Flask(__name__)
CORS(app)  # Permite que o React acesse os endpoints

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    nome = data.get("nome")
    senha = data.get("senha")

    try:
        with sqlite3.connect("db/registro_ponto.db") as conn:
            cursor = conn.cursor()

            # Verifica o usuário no banco
            cursor.execute("SELECT id, tipo FROM usuarios WHERE nome = ? AND senha = ?", (nome, senha))
            user = cursor.fetchone()

            if not user:
                return jsonify({"error": "Usuário ou senha incorretos"}), 401

            user_id, tipo = user

            # Se for colaborador, buscar o colaborador_id
            if tipo == "colaborador":
                cursor.execute("SELECT id FROM colaboradores WHERE usuario_id = ?", (user_id,))
                colaborador = cursor.fetchone()

                if colaborador:
                    colaborador_id = colaborador[0]
                else:
                    return jsonify({"error": "Colaborador não encontrado"}), 404
            else:
                colaborador_id = None

            return jsonify({"id": user_id, "tipo": tipo, "colaborador_id": colaborador_id}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/registrar_ponto", methods=["POST"])
def registrar_ponto():
    data = request.json
    colaborador_id = data.get("colaborador_id")

    if not colaborador_id:
        return jsonify({"error": "Colaborador não autenticado"}), 401

    hora_atual = datetime.now().strftime("%H:%M:%S")  # Apenas a hora
    data_atual = datetime.now().strftime("%Y-%m-%d")  # Apenas a data

    try:
        with sqlite3.connect("db/registro_ponto.db") as conn:
            cursor = conn.cursor()

            # Inserir registro de ponto
            cursor.execute(
                """
                INSERT INTO registros (colaborador_id, hora_registro, data_registro) 
                VALUES (?, ?, ?)
                """,
                (colaborador_id, hora_atual, data_atual),
            )
            conn.commit()

        return jsonify({"message": "Ponto registrado com sucesso!"}), 201

    except sqlite3.OperationalError as e:
        return jsonify({"error": f"Erro no banco de dados: {e}"}), 500
    except Exception as e:
        return jsonify({"error": "Ocorreu um erro inesperado."}), 500


# Listar Colaboradores
@app.route("/colaboradores", methods=["GET"])
def listar_colaboradores():
    conn = sqlite3.connect("db/registro_ponto.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT colaboradores.id, colaboradores.nome, usuarios.nome AS nome_usuario
    FROM colaboradores
    JOIN usuarios ON colaboradores.usuario_id = usuarios.id
    """)
    colaboradores = cursor.fetchall()
    conn.close()
    return jsonify([{"id": colab[0], "nome": colab[1], "usuario_nome": colab[2]} for colab in colaboradores])

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
    
    # Gerar senha aleatória para o colaborador
    senha = gerar_senha()
    
    try:
        # Usar 'with' para garantir que a conexão seja fechada corretamente
        # Aumentando o timeout para 30 segundos e incluindo PRAGMA para evitar bloqueios
        with sqlite3.connect("db/registro_ponto.db", timeout=30) as conn:
            cursor = conn.cursor()
            
            # Adicionando PRAGMA para melhorar controle de bloqueio
            cursor.execute("PRAGMA journal_mode=DELETE;")  # Garante que o SQLite não use WAL
            cursor.execute("PRAGMA foreign_keys = ON;")  # Habilita as chaves estrangeiras
            
            # Inserir novo usuário
            cursor.execute("INSERT INTO usuarios (nome, senha, tipo) VALUES (?, ?, ?)", (nome, senha, 'colaborador'))
            usuario_id = cursor.lastrowid

            # Inserir colaborador associado ao usuário
            cursor.execute("INSERT INTO colaboradores (usuario_id, nome) VALUES (?, ?)", (usuario_id, nome))

            conn.commit()  # Comitar a transação
            
        return jsonify({"message": f"Colaborador {nome} adicionado com sucesso! senha gerada: {senha}"}), 201

    except sqlite3.OperationalError as e:
        # Captura o erro de banco de dados bloqueado
        print(f"Erro de operação no banco de dados: {e}")
        return jsonify({"error": "Erro ao acessar o banco de dados. Tente novamente."}), 500
    except Exception as e:
        # Captura outros erros e imprime o traceback para depuração
        print(f"Ocorreu um erro inesperado: {e}")
        print(traceback.format_exc())  # Imprime o traceback completo para depuração
        return jsonify({"error": "Ocorreu um erro inesperado. Verifique os logs para mais detalhes."}), 500


# Remover Colaborador
@app.route("/colaboradores/<int:id_colaborador>", methods=["DELETE"])
def remover_colaborador(id_colaborador):
    conn = sqlite3.connect("db/registro_ponto.db")
    cursor = conn.cursor()
    
    # Buscar colaborador para pegar o usuario_id
    cursor.execute("SELECT usuario_id FROM colaboradores WHERE id = ?", (id_colaborador,))
    colaborador = cursor.fetchone()
    
    if colaborador:
        usuario_id = colaborador[0]
        # Excluir colaborador
        cursor.execute("DELETE FROM colaboradores WHERE id = ?", (id_colaborador,))
        # Excluir usuário relacionado
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
        cursor.execute('DELETE FROM registros WHERE colaborador_id = ?', (id_colaborador,))
        conn.commit()
        conn.close()
        return jsonify({"message": f"Colaborador ID {id_colaborador} e usuário removidos com sucesso!"})
    else:
        conn.close()
        return jsonify({"message": "Colaborador não encontrado!"}), 404

if __name__ == "__main__":
    db_create_path = 'db/create_bd.py'
    db_path = 'db/registro_ponto.db'

    if os.path.exists(db_path):
        print('Banco de dados já criado')
    else:
        result = subprocess.run(['python', db_create_path], capture_output=True, text=True)
        print(result.stdout)
        print(result.stderr)

    app.run(debug=True)
