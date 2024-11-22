from app.sistema_admin import listar_colaboradores, listar_registros, adicionar_colaborador, remover_colaborador

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