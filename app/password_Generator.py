import random
import string


def generate_password(tamanho=12):
    """
    Gera uma senha aleatória com o tamanho especificado.
    O padrão é uma senha de 12 caracteres.
    """
    # Caracteres que podem ser usados na senha
    caracteres = string.ascii_letters + string.digits + string.punctuation

    # Gera uma senha aleatória
    senha = ''.join(random.choice(caracteres) for _ in range(tamanho))

    return senha

# Exemplo de uso
if __name__ == "__main__":
    tamanho = int(input("Digite o tamanho da senha que deseja gerar: "))
    senha_gerada = generate_password(tamanho)
    print(f"Sua senha gerada é: {senha_gerada}")