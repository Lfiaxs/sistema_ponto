import sqlite3

def listar_colaboradores():
    conn = sqlite3.connect("registro_ponto.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM colaboradores")
    colaboradores = cursor.fetchall()

    print("\n=== Lista de Colaboradores ===")
    for colab in colaboradores:
        print(f"ID: {colab[0]}, Nome: {colab[1]}")
    
    conn.close()

def listar_registros():
    conn = sqlite3.connect("registro_ponto.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT registros.id, colaboradores.nome, registros.hora_registro
    FROM registros
    INNER JOIN colaboradores ON registros.colaborador_id = colaboradores.id
    """)
    registros = cursor.fetchall()

    print("\n=== Registros de Ponto ===")
    for reg in registros:
        print(f"ID Registro: {reg[0]}, Nome: {reg[1]}, Hora: {reg[2]}")
    
    conn.close()

def adicionar_colaborador():
    conn = sqlite3.connect("registro_ponto.db")
    cursor = conn.cursor()

    nome = input("Digite o nome do novo colaborador: ")

    cursor.execute("INSERT INTO colaboradores (nome) VALUES (?)", (nome,))
    conn.commit()
    print(f"Colaborador {nome} adicionado com sucesso!")

    conn.close()

def remover_colaborador():
    conn = sqlite3.connect("registro_ponto.db")
    cursor = conn.cursor()

    id_colaborador = input("Digite o ID do colaborador a ser removido: ")

    cursor.execute("DELETE FROM colaboradores WHERE id = ?", (id_colaborador,))
    conn.commit()
    print(f"Colaborador ID {id_colaborador} removido com sucesso!")

    conn.close()

def sistema_admin():
    while True:
        print("\n=== Sistema do Administrador ===")
        print("1. Listar Colaboradores")
        print("2. Listar Registros de Ponto")
        print("3. Adicionar Colaborador")
        print("4. Remover Colaborador")
        print("5. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            listar_colaboradores()
        elif opcao == "2":
            listar_registros()
        elif opcao == "3":
            adicionar_colaborador()
        elif opcao == "4":
            remover_colaborador()
        elif opcao == "5":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    sistema_admin()
