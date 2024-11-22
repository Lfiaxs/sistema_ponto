import sqlite3

conn = sqlite3.connect("db/registro_ponto.db")
cursor = conn.cursor()

# Criando tabela de usuários
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    senha TEXT NOT NULL,
    tipo TEXT NOT NULL CHECK(tipo IN ('admin', 'colaborador'))
)
""")

# Criando tabela de colaboradores
cursor.execute("""
CREATE TABLE IF NOT EXISTS colaboradores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
)
""")

# Criando tabela de registros de ponto
cursor.execute("""
CREATE TABLE IF NOT EXISTS registros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    colaborador_id INTEGER NOT NULL,
    hora_registro TEXT NOT NULL,
    FOREIGN KEY(colaborador_id) REFERENCES colaboradores(id)
)
""")

print("Banco de dados configurado!")
conn.commit()
conn.close()
