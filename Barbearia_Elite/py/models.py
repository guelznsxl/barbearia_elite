# classes que representam os dados principais do sistema

class Cliente:
    def __init__(self, nome, telefone, email=""):
        self.nome = nome
        self.telefone = telefone
        self.email = email


class Barbeiro:
    def __init__(self, nome, telefone="", especialidade=""):
        self.nome = nome
        self.telefone = telefone
        self.especialidade = especialidade


class Servico:
    def __init__(self, nome, preco, duracao, descricao=""):
        self.nome = nome
        self.preco = preco
        self.duracao = duracao
        self.descricao = descricao


class Agendamento:
    def __init__(self, cliente_id, barbeiro_id, servico_id, data, horario, status="Pendente"):
        self.cliente_id = cliente_id
        self.barbeiro_id = barbeiro_id
        self.servico_id = servico_id
        self.data = data
        self.horario = horario
        self.status = status
