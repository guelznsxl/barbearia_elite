from pathlib import Path
import sqlite3

# caminho principal da pasta do projeto
PASTA_PROJETO = Path(__file__).resolve().parent.parent

# pasta e arquivos do banco de dados
PASTA_BANCO = PASTA_PROJETO / "banco"
DATABASE = PASTA_BANCO / "barbearia.db"
ARQUIVO_SQL = PASTA_BANCO / "schema.sql"


def conectar():
    # cria a pasta banco caso ela ainda nao exista
    PASTA_BANCO.mkdir(parents=True, exist_ok=True)

    conexao = sqlite3.connect(str(DATABASE))
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")

    return conexao


def criar_banco():
    # confere se o arquivo de criacao das tabelas existe
    if not ARQUIVO_SQL.exists():
        raise FileNotFoundError(
            f"Arquivo schema.sql nao encontrado em: {ARQUIVO_SQL}"
        )

    conexao = conectar()

    try:
        with open(ARQUIVO_SQL, "r", encoding="utf-8") as arquivo:
            conexao.executescript(arquivo.read())
    finally:
        conexao.close()

