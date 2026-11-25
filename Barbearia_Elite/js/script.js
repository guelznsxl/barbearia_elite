
async function carregarAgendamentos() {
    try {
        const dados = await buscarDados("/api/agendamentos");
        const tabela = document.getElementById("tabelaAgendamentos");

        if (!tabela) return;

        tabela.innerHTML = "";

        dados.forEach(item => {
            tabela.innerHTML += `
                <tr>
                    <td>${protegerTexto(item.cliente_nome || item.cliente_id)}</td>
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
        console.log(erro);
    }
}
