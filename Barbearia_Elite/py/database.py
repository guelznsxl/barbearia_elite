from pathlib import Path
import sqlite3

# caminho principal da pasta do projeto
PASTA_PROJETO = Path(__file__).resolve().parent.parent
DATABASE = PASTA_PROJETO / "banco" / "barbearia.db"
ARQUIVO_SQL = PASTA_PROJETO / "banco" / "schema.sql"

def conectar():
    conexao = sqlite3.connect(DATABASE)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao

def criar_banco():
    conexao = conectar()
    with open(ARQUIVO_SQL, "r", encoding="utf-8") as arquivo:
        conexao.executescript(arquivo.read())
    conexao.close()

    
