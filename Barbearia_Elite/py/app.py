from flask import Flask, render_template, request, jsonify, send_from_directory
from pathlib import Path
import sqlite3

from database import criar_banco
from daos import ClienteDAO, BarbeiroDAO, ServicoDAO, AgendamentoDAO
from models import Cliente, Barbeiro, Servico, Agendamento

PASTA_PROJETO = Path(__file__).resolve().parent.parent
app = Flask(__name__, template_folder=str(PASTA_PROJETO / "html"), static_folder=None)

@app.route("/css/<path:arquivo>")
def arquivos_css(arquivo):
    return send_from_directory(PASTA_PROJETO / "css", arquivo)

@app.route("/js/<path:arquivo>")
def arquivos_js(arquivo):
    return send_from_directory(PASTA_PROJETO / "js", arquivo)

cliente_dao = ClienteDAO()
barbeiro_dao = BarbeiroDAO()
servico_dao = ServicoDAO()
agendamento_dao = AgendamentoDAO()

@app.route("/")
def inicio():
    return render_template("index.html")


def erro(mensagem, codigo=400):
    return jsonify({"erro": mensagem}), codigo


@app.route("/api/clientes", methods=["GET", "POST"])
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


@app.route("/api/clientes/<int:id_item>", methods=["PUT", "DELETE"])
def cliente_detalhe(id_item):
    if request.method == "DELETE":
        try:
            if cliente_dao.excluir(id_item):
                return jsonify({"mensagem": "Cliente excluido."})
            return erro("Cliente nao encontrado.", 404)
        except sqlite3.IntegrityError:
            return erro("Esse cliente possui agendamentos. Cancele ou remova os agendamentos antes.")

    dados = request.get_json() or {}
    nome = dados.get("nome", "").strip()
    telefone = dados.get("telefone", "").strip()
    email = dados.get("email", "").strip()
    if not nome or not telefone:
        return erro("Informe o nome e o telefone.")
    if cliente_dao.atualizar(id_item, Cliente(nome, telefone, email)):
        return jsonify({"mensagem": "Cliente atualizado."})
    return erro("Cliente nao encontrado.", 404)


@app.route("/api/barbeiros", methods=["GET", "POST"])
def barbeiros():
    if request.method == "GET":
        return jsonify(barbeiro_dao.listar())
    dados = request.get_json() or {}
    nome = dados.get("nome", "").strip()
    if not nome:
        return erro("Informe o nome do barbeiro.")
    barbeiro_dao.inserir(Barbeiro(nome, dados.get("telefone", ""), dados.get("especialidade", "")))
    return jsonify({"mensagem": "Barbeiro cadastrado."}), 201


@app.route("/api/barbeiros/<int:id_item>", methods=["PUT", "DELETE"])
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
    barbeiro = Barbeiro(nome, dados.get("telefone", ""), dados.get("especialidade", ""))
    if barbeiro_dao.atualizar(id_item, barbeiro):
        return jsonify({"mensagem": "Barbeiro atualizado."})
    return erro("Barbeiro nao encontrado.", 404)


@app.route("/api/servicos", methods=["GET", "POST"])
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
    servico_dao.inserir(Servico(nome, preco, duracao, dados.get("descricao", "")))
    return jsonify({"mensagem": "Servico cadastrado."}), 201


@app.route("/api/servicos/<int:id_item>", methods=["PUT", "DELETE"])
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
    servico = Servico(nome, preco, duracao, dados.get("descricao", ""))
    if servico_dao.atualizar(id_item, servico):
        return jsonify({"mensagem": "Servico atualizado."})
    return erro("Servico nao encontrado.", 404)


@app.route("/api/agendamentos", methods=["GET", "POST"])
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

    agendamento = Agendamento(cliente_id, barbeiro_id, servico_id, data, horario)
    try:
        agendamento_dao.inserir(agendamento)
    except sqlite3.IntegrityError:
        return erro("Confira se o cliente, barbeiro e servico existem.")
    return jsonify({"mensagem": "Agendamento criado com sucesso."}), 201


@app.route("/api/agendamentos/<int:id_item>", methods=["PATCH", "DELETE"])
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


@app.route("/api/resumo")
def resumo():
    return jsonify({
        "clientes": len(cliente_dao.listar()),
        "barbeiros": len(barbeiro_dao.listar()),
        "servicos": len(servico_dao.listar()),
        "agendamentos": len(agendamento_dao.listar())
    })


if __name__ == "__main__":
    criar_banco()
    app.run(debug=True)
