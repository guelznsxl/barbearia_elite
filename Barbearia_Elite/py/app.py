
from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, session
from pathlib import Path
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

from database import criar_banco
from daos import ClienteDAO, BarbeiroDAO, ServicoDAO, AgendamentoDAO
from models import Cliente, Barbeiro, Servico, Agendamento


# configuracao do projeto
PASTA_PROJETO = Path(__file__).resolve().parent.parent

app = Flask(
    __name__,
    template_folder=str(PASTA_PROJETO / "html"),
    static_folder=None
)

app.secret_key = os.environ.get("SECRET_KEY", "chave-local-de-desenvolvimento")

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = os.environ.get("RENDER") is not None

# dados do administrador
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
ADMIN_PASSWORD_HASH = os.environ.get("ADMIN_PASSWORD_HASH")

if ADMIN_PASSWORD_HASH:
    SENHA_ADMIN_HASH = ADMIN_PASSWORD_HASH
elif ADMIN_PASSWORD:
    SENHA_ADMIN_HASH = generate_password_hash(ADMIN_PASSWORD)
else:
    SENHA_ADMIN_HASH = None


# conexao com os DAOs
cliente_dao = ClienteDAO()
barbeiro_dao = BarbeiroDAO()
servico_dao = ServicoDAO()
agendamento_dao = AgendamentoDAO()


# arquivos CSS
@app.route("/css/<path:arquivo>")
def arquivos_css(arquivo):
    return send_from_directory(PASTA_PROJETO / "css", arquivo)


# arquivos JavaScript
@app.route("/js/<path:arquivo>")
def arquivos_js(arquivo):
    return send_from_directory(PASTA_PROJETO / "js", arquivo)


# verificacao de acesso
@app.before_request
def proteger_apis():
    if request.endpoint and request.endpoint.startswith("api_"):
        if not session.get("admin_logado"):
            return jsonify({"erro": "Faça login para continuar."}), 401


# pagina de login
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        if session.get("admin_logado"):
            return redirect("/")
        return render_template("login.html")

    dados = request.get_json() or {}

    usuario = dados.get("usuario", "")
    senha = dados.get("senha", "")

    if not SENHA_ADMIN_HASH:
        return jsonify({
            "erro": "Configure a senha do administrador no ambiente do servidor."
        }), 503

    if (
        usuario == ADMIN_USERNAME
        and check_password_hash(SENHA_ADMIN_HASH, senha)
    ):
        session.clear()
        session["admin_logado"] = True
        session["usuario"] = usuario

        return jsonify({
            "mensagem": "Login realizado com sucesso."
        })

    return jsonify({"erro": "Usuário ou senha incorretos."}), 401


# sair da conta
@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"mensagem": "Sessão encerrada."})


# pagina inicial
@app.route("/")
def inicio():
    if not session.get("admin_logado"):
        return redirect("/login")

    return render_template("index.html")


# paginas do sistema
@app.route("/clientes")
def pagina_clientes():
    if not session.get("admin_logado"):
        return redirect("/login")
    return render_template("clientes.html")


@app.route("/barbeiros")
def pagina_barbeiros():
    if not session.get("admin_logado"):
        return redirect("/login")
    return render_template("barbeiros.html")


@app.route("/servicos")
def pagina_servicos():
    if not session.get("admin_logado"):
        return redirect("/login")
    return render_template("servicos.html")


@app.route("/agendamentos")
def pagina_agendamentos():
    if not session.get("admin_logado"):
        return redirect("/login")
    return render_template("agendamentos.html")


@app.route("/admin")
def pagina_admin():
    if not session.get("admin_logado"):
        return redirect("/login")
    return render_template("admin.html")


# mensagens de erro
def erro(mensagem, codigo=400):
    return jsonify({"erro": mensagem}), codigo


# CLIENTES
@app.route("/api/clientes", methods=["GET", "POST"], endpoint="api_clientes")
def clientes():

    if request.method == "GET":
        return jsonify(cliente_dao.listar())

    dados = request.get_json() or {}

    nome = dados.get("nome", "").strip()
    telefone = dados.get("telefone", "").strip()
    email = dados.get("email", "").strip()

    if not nome or not telefone:
        return erro("Informe o nome e o telefone do cliente.")

    cliente_dao.inserir(Cliente(nome, telefone, email))

    return jsonify({"mensagem": "Cliente cadastrado com sucesso."}), 201


@app.route("/api/clientes/<int:id_item>", methods=["PUT", "DELETE"], endpoint="api_cliente_detalhe")
def cliente_detalhe(id_item):

    if request.method == "DELETE":
        try:
            if cliente_dao.excluir(id_item):
                return jsonify({"mensagem": "Cliente excluido."})

            return erro("Cliente nao encontrado.", 404)

        except sqlite3.IntegrityError:
            return erro("Esse cliente possui agendamentos.")

    dados = request.get_json() or {}

    nome = dados.get("nome", "").strip()
    telefone = dados.get("telefone", "").strip()
    email = dados.get("email", "").strip()

    if not nome or not telefone:
        return erro("Informe o nome e o telefone.")

    if cliente_dao.atualizar(id_item, Cliente(nome, telefone, email)):
        return jsonify({"mensagem": "Cliente atualizado."})

    return erro("Cliente nao encontrado.", 404)


# BARBEIROS
@app.route("/api/barbeiros", methods=["GET", "POST"], endpoint="api_barbeiros")
def barbeiros():

    if request.method == "GET":
        return jsonify(barbeiro_dao.listar())

    dados = request.get_json() or {}

    nome = dados.get("nome", "").strip()

    if not nome:
        return erro("Informe o nome do barbeiro.")

    barbeiro_dao.inserir(
        Barbeiro(
            nome,
            dados.get("telefone", ""),
            dados.get("especialidade", "")
        )
    )

    return jsonify({"mensagem": "Barbeiro cadastrado."}), 201


@app.route("/api/barbeiros/<int:id_item>", methods=["PUT", "DELETE"], endpoint="api_barbeiro_detalhe")
def barbeiro_detalhe(id_item):

    if request.method == "DELETE":
        try:
            if barbeiro_dao.excluir(id_item):
                return jsonify({"mensagem": "Barbeiro excluido."})

            return erro("Barbeiro nao encontrado.", 404)

        except sqlite3.IntegrityError:
            return erro("Este barbeiro possui agendamentos cadastrados.")

    dados = request.get_json() or {}

    nome = dados.get("nome", "").strip()

    if not nome:
        return erro("Informe o nome do barbeiro.")

    barbeiro = Barbeiro(
        nome,
        dados.get("telefone", ""),
        dados.get("especialidade", "")
    )

    if barbeiro_dao.atualizar(id_item, barbeiro):
        return jsonify({"mensagem": "Barbeiro atualizado."})

    return erro("Barbeiro nao encontrado.", 404)


# SERVICOS
@app.route("/api/servicos", methods=["GET", "POST"], endpoint="api_servicos")
def servicos():

    if request.method == "GET":
        return jsonify(servico_dao.listar())

    dados = request.get_json() or {}

    nome = dados.get("nome", "").strip()

    try:
        preco = float(dados.get("preco", 0))
        duracao = int(dados.get("duracao", 0))
    except (ValueError, TypeError):
        return erro("Preco e duracao precisam ser numeros.")

    if not nome or preco < 0 or duracao <= 0:
        return erro("Informe nome, preco valido e duracao maior que zero.")

    servico_dao.inserir(
        Servico(
            nome,
            preco,
            duracao,
            dados.get("descricao", "")
        )
    )

    return jsonify({"mensagem": "Servico cadastrado."}), 201


@app.route("/api/servicos/<int:id_item>", methods=["PUT", "DELETE"], endpoint="api_servico_detalhe")
def servico_detalhe(id_item):

    if request.method == "DELETE":
        try:
            if servico_dao.excluir(id_item):
                return jsonify({"mensagem": "Servico excluido."})

            return erro("Servico nao encontrado.", 404)

        except sqlite3.IntegrityError:
            return erro("Este servico esta ligado a agendamentos.")

    dados = request.get_json() or {}

    try:
        preco = float(dados.get("preco", 0))
        duracao = int(dados.get("duracao", 0))
    except (ValueError, TypeError):
        return erro("Preco e duracao precisam ser numeros.")

    nome = dados.get("nome", "").strip()

    if not nome or preco < 0 or duracao <= 0:
        return erro("Preencha os dados do servico corretamente.")

    servico = Servico(
        nome,
        preco,
        duracao,
        dados.get("descricao", "")
    )

    if servico_dao.atualizar(id_item, servico):
        return jsonify({"mensagem": "Servico atualizado."})

    return erro("Servico nao encontrado.", 404)


# AGENDAMENTOS
@app.route("/api/agendamentos", methods=["GET", "POST"], endpoint="api_agendamentos")
def agendamentos():

    if request.method == "GET":
        return jsonify(agendamento_dao.listar())

    dados = request.get_json() or {}

    try:
        cliente_id = int(dados.get("cliente_id"))
        barbeiro_id = int(dados.get("barbeiro_id"))
        servico_id = int(dados.get("servico_id"))
    except (ValueError, TypeError):
        return erro("Selecione cliente, barbeiro e servico.")

    data = dados.get("data", "")
    horario = dados.get("horario", "")

    if not data or not horario:
        return erro("Informe a data e o horario.")

    if agendamento_dao.horario_ocupado(barbeiro_id, data, horario):
        return erro("Esse barbeiro ja possui agendamento nesse horario.")

    agendamento = Agendamento(
        cliente_id,
        barbeiro_id,
        servico_id,
        data,
        horario
    )

    try:
        agendamento_dao.inserir(agendamento)
    except sqlite3.IntegrityError:
        return erro("Confira se o cliente, barbeiro e servico existem.")

    return jsonify({"mensagem": "Agendamento criado com sucesso."}), 201


@app.route("/api/agendamentos/<int:id_item>", methods=["PATCH", "DELETE"], endpoint="api_agendamento_detalhe")
def agendamento_detalhe(id_item):

    if request.method == "DELETE":
        if agendamento_dao.excluir(id_item):
            return jsonify({"mensagem": "Agendamento excluido."})

        return erro("Agendamento nao encontrado.", 404)

    dados = request.get_json() or {}

    status = dados.get("status", "")

    if status not in ["Pendente", "Confirmado", "Concluido", "Cancelado"]:
        return erro("Status invalido.")

    if agendamento_dao.atualizar_status(id_item, status):
        return jsonify({"mensagem": "Status atualizado."})

    return erro("Agendamento nao encontrado.", 404)


# RESUMO DO SISTEMA
@app.route("/api/resumo", endpoint="api_resumo")
def resumo():

    return jsonify({
        "clientes": len(cliente_dao.listar()),
        "barbeiros": len(barbeiro_dao.listar()),
        "servicos": len(servico_dao.listar()),
        "agendamentos": len(agendamento_dao.listar())
    })


# cria o banco de dados
criar_banco()


if __name__ == "__main__":
    app.run(debug=True)
