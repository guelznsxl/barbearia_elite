
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CAMINHO_BANCO = os.path.join(BASE_DIR, "sql", "barbearia.db")
CAMINHO_SCHEMA = os.path.join(BASE_DIR, "sql", "schema.sql")


def conectar():
    os.makedirs(os.path.dirname(CAMINHO_BANCO), exist_ok=True)
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def criar_banco():
    if not os.path.exists(CAMINHO_SCHEMA):
        raise FileNotFoundError(
            f"Arquivo schema.sql não encontrado em: {CAMINHO_SCHEMA}"
        )

    with open(CAMINHO_SCHEMA, "r", encoding="utf-8") as arquivo:
        sql = arquivo.read()

    conexao = conectar()
    conexao.executescript(sql)
    conexao.close()
