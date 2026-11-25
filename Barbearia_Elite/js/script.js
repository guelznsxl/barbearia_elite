
async function carregarAgendamentos() {
    try {
        const dados = await buscarDados("/api/agendamentos");
        const clientes = await buscarDados("/api/clientes");
        const tabela = document.getElementById("tabelaAgendamentos");

        if (!tabela) return;

        tabela.innerHTML = "";

        if (dados.length === 0) {
            tabela.innerHTML = `
                <tr>
                    <td colspan="9" class="empty-cell">
                        Nenhum agendamento cadastrado.
                    </td>
                </tr>
            `;
            return;
        }

        dados.forEach(item => {
            const cliente = clientes.find(
                pessoa => Number(pessoa.id) === Number(item.cliente_id)
            );

            tabela.innerHTML += `
                <tr>
                    <td>${protegerTexto(item.cliente_nome || item.cliente_id)}</td>
                    <td>${protegerTexto(cliente?.telefone || "Não informado")}</td>
                    <td>${protegerTexto(cliente?.email || "Não informado")}</td>
                    <td>${protegerTexto(item.barbeiro_nome || item.barbeiro_id)}</td>
                    <td>${protegerTexto(item.servico_nome || item.servico_id)}</td>
                    <td>${protegerTexto(item.data)}</td>
                    <td>${protegerTexto(item.horario)}</td>
                    <td>${protegerTexto(item.status)}</td>
                    <td>
                        <button onclick="excluirAgendamento(${item.id})">Excluir</button>
                    </td>
                </tr>
            `;
        });

    } catch (erro) {
        console.log("Erro ao carregar agendamentos:", erro);
    }
}
