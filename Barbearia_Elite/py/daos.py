# DAOs: classes responsaveis por conversar com o banco de dados

from database import conectar
from models import Cliente, Barbeiro, Servico, Agendamento


class ClienteDAO:
    def listar(self):
        conexao = conectar()
        dados = conexao.execute("SELECT * FROM clientes ORDER BY nome").fetchall()
        conexao.close()
        return [dict(item) for item in dados]

    def inserir(self, cliente):
        conexao = conectar()
        conexao.execute(
            "INSERT INTO clientes (nome, telefone, email) VALUES (?, ?, ?)",
            (cliente.nome, cliente.telefone, cliente.email)
        )
        conexao.commit()
        conexao.close()

    def atualizar(self, id_cliente, cliente):
        conexao = conectar()
        conexao.execute(
            "UPDATE clientes SET nome=?, telefone=?, email=? WHERE id=?",
            (cliente.nome, cliente.telefone, cliente.email, id_cliente)
        )
        conexao.commit()
        alterou = conexao.total_changes
        conexao.close()
        return alterou > 0

    def excluir(self, id_cliente):
        conexao = conectar()
        conexao.execute("DELETE FROM clientes WHERE id=?", (id_cliente,))
        alterou = conexao.total_changes
        conexao.commit()
        conexao.close()
        return alterou > 0


class BarbeiroDAO:
    def listar(self):
        conexao = conectar()
        dados = conexao.execute("SELECT * FROM barbeiros ORDER BY nome").fetchall()
        conexao.close()
        return [dict(item) for item in dados]

    def inserir(self, barbeiro):
        conexao = conectar()
        conexao.execute(
            "INSERT INTO barbeiros (nome, telefone, especialidade) VALUES (?, ?, ?)",
            (barbeiro.nome, barbeiro.telefone, barbeiro.especialidade)
        )
        conexao.commit()
        conexao.close()

    def atualizar(self, id_barbeiro, barbeiro):
        conexao = conectar()
        conexao.execute(
            "UPDATE barbeiros SET nome=?, telefone=?, especialidade=? WHERE id=?",
            (barbeiro.nome, barbeiro.telefone, barbeiro.especialidade, id_barbeiro)
        )
        alterou = conexao.total_changes
        conexao.commit()
        conexao.close()
        return alterou > 0

    def excluir(self, id_barbeiro):
        conexao = conectar()
        conexao.execute("DELETE FROM barbeiros WHERE id=?", (id_barbeiro,))
        alterou = conexao.total_changes
        conexao.commit()
        conexao.close()
        return alterou > 0


class ServicoDAO:
    def listar(self):
        conexao = conectar()
        dados = conexao.execute("SELECT * FROM servicos ORDER BY nome").fetchall()
        conexao.close()
        return [dict(item) for item in dados]

    def inserir(self, servico):
        conexao = conectar()
        conexao.execute(
            "INSERT INTO servicos (nome, descricao, preco, duracao) VALUES (?, ?, ?, ?)",
            (servico.nome, servico.descricao, servico.preco, servico.duracao)
        )
        conexao.commit()
        conexao.close()

    def atualizar(self, id_servico, servico):
        conexao = conectar()
        conexao.execute(
            "UPDATE servicos SET nome=?, descricao=?, preco=?, duracao=? WHERE id=?",
            (servico.nome, servico.descricao, servico.preco, servico.duracao, id_servico)
        )
        alterou = conexao.total_changes
        conexao.commit()
        conexao.close()
        return alterou > 0

    def excluir(self, id_servico):
        conexao = conectar()
        conexao.execute("DELETE FROM servicos WHERE id=?", (id_servico,))
        alterou = conexao.total_changes
        conexao.commit()
        conexao.close()
        return alterou > 0


class AgendamentoDAO:
    def listar(self):
        conexao = conectar()
        dados = conexao.execute("""
            SELECT a.*, c.nome AS cliente, b.nome AS barbeiro, s.nome AS servico
            FROM agendamentos a
            JOIN clientes c ON a.cliente_id = c.id
            JOIN barbeiros b ON a.barbeiro_id = b.id
            JOIN servicos s ON a.servico_id = s.id
            ORDER BY a.data, a.horario
        """).fetchall()
        conexao.close()
        return [dict(item) for item in dados]

    def horario_ocupado(self, barbeiro_id, data, horario, ignorar_id=None):
        conexao = conectar()
        sql = """
            SELECT id FROM agendamentos
            WHERE barbeiro_id=? AND data=? AND horario=? AND status != 'Cancelado'
        """
        valores = [barbeiro_id, data, horario]
        if ignorar_id is not None:
            sql += " AND id != ?"
            valores.append(ignorar_id)
        resultado = conexao.execute(sql, valores).fetchone()
        conexao.close()
        return resultado is not None

    def inserir(self, agendamento):
        conexao = conectar()
        conexao.execute(
            """INSERT INTO agendamentos
            (cliente_id, barbeiro_id, servico_id, data, horario, status)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (agendamento.cliente_id, agendamento.barbeiro_id,
             agendamento.servico_id, agendamento.data,
             agendamento.horario, agendamento.status)
        )
        conexao.commit()
        conexao.close()

    def atualizar_status(self, id_agendamento, status):
        conexao = conectar()
        conexao.execute(
            "UPDATE agendamentos SET status=? WHERE id=?",
            (status, id_agendamento)
        )
        alterou = conexao.total_changes
        conexao.commit()
        conexao.close()
        return alterou > 0

    def excluir(self, id_agendamento):
        conexao = conectar()
        conexao.execute("DELETE FROM agendamentos WHERE id=?", (id_agendamento,))
        alterou = conexao.total_changes
        conexao.commit()
        conexao.close()
        return alterou > 0
