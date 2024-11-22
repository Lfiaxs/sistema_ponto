import sqlite3
from datetime import datetime


def registrar_ponto():
    # Conectar ao banco de dados
    conn = sqlite3.connect("registro_ponto.db")
    cursor = conn.cursor()

    # Solicitar ID do colaborador
    colaborador_id = input("Digite seu ID de colaborador: ")

    # Verificar se o colaborador existe
    cursor.execute("SELECT nome FROM colaboradores WHERE id = ?", (colaborador_id,))
    colaborador = cursor.fetchone()

    if colaborador:
        nome = colaborador[0]
        hora_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Inserir o registro de ponto
        cursor.execute("""
        INSERT INTO registros (colaborador_id, hora_registro)
        VALUES (?, ?)
        """, (colaborador_id, hora_atual))

        conn.commit()
        print(f"Ponto registrado com sucesso! Nome: {nome}, Hora: {hora_atual}")
    else:
        print("Colaborador não encontrado. Verifique o ID.")

    # Fechar conexão
    conn.close()

if __name__ == "__main__":
    registrar_ponto()
