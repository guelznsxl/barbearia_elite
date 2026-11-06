const mensagem = document.getElementById("mensagem");

async function api(url, metodo = "GET", dados = null) {
    const opcoes = { method: metodo, headers: { "Content-Type": "application/json" } };
    if (dados) opcoes.body = JSON.stringify(dados);

    const resposta = await fetch(url, opcoes);
    const resultado = await resposta.json();

    if (!resposta.ok) throw new Error(resultado.erro || "Ocorreu um erro.");
    return resultado;
}

function avisar(texto, erro = false) {
    mensagem.textContent = texto;
    mensagem.className = erro ? "mensagem erro" : "mensagem";
}

function escapar(texto) {
    return String(texto ?? "").replace(/[&<>"']/g, caractere => ({
        "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;"
    }[caractere]));
}

async function carregarTudo() {
    try {
        await Promise.all([
            carregarClientes(), carregarBarbeiros(), carregarServicos(),
            carregarAgendamentos(), carregarResumo()
        ]);
    } catch (erro) {
        avisar(erro.message, true);
    }
}

async function carregarResumo() {
    const dados = await api("/api/resumo");
    document.getElementById("totalClientes").textContent = dados.clientes;
    document.getElementById("totalBarbeiros").textContent = dados.barbeiros;
    document.getElementById("totalServicos").textContent = dados.servicos;
    document.getElementById("totalAgendamentos").textContent = dados.agendamentos;
}

async function carregarClientes() {
    const dados = await api("/api/clientes");
    document.getElementById("listaClientes").innerHTML = dados.map(item => `
        <tr><td>${escapar(item.nome)}</td><td>${escapar(item.telefone)}</td>
        <td>${escapar(item.email)}</td><td>
        <button class="acao" onclick="editarCliente(${item.id})">Editar</button>
        <button class="acao perigo" onclick="excluirItem('clientes',${item.id})">Excluir</button></td></tr>`).join("");
    document.getElementById("agCliente").innerHTML = '<option value="">Selecione</option>' +
        dados.map(item => `<option value="${item.id}">${escapar(item.nome)}</option>`).join("");
}

async function carregarBarbeiros() {
    const dados = await api("/api/barbeiros");
    document.getElementById("listaBarbeiros").innerHTML = dados.map(item => `
        <tr><td>${escapar(item.nome)}</td><td>${escapar(item.telefone)}</td>
        <td>${escapar(item.especialidade)}</td><td>
        <button class="acao" onclick="editarBarbeiro(${item.id})">Editar</button>
        <button class="acao perigo" onclick="excluirItem('barbeiros',${item.id})">Excluir</button></td></tr>`).join("");
    document.getElementById("agBarbeiro").innerHTML = '<option value="">Selecione</option>' +
        dados.map(item => `<option value="${item.id}">${escapar(item.nome)}</option>`).join("");
}

async function carregarServicos() {
    const dados = await api("/api/servicos");
    document.getElementById("listaServicos").innerHTML = dados.map(item => `
        <tr><td>${escapar(item.nome)}</td><td>${escapar(item.descricao)}</td>
        <td>R$ ${Number(item.preco).toFixed(2)}</td><td>${item.duracao} min</td><td>
        <button class="acao" onclick="editarServico(${item.id})">Editar</button>
        <button class="acao perigo" onclick="excluirItem('servicos',${item.id})">Excluir</button></td></tr>`).join("");
    document.getElementById("agServico").innerHTML = '<option value="">Selecione</option>' +
        dados.map(item => `<option value="${item.id}">${escapar(item.nome)} - R$ ${Number(item.preco).toFixed(2)}</option>`).join("");
}

async function carregarAgendamentos() {
    const dados = await api("/api/agendamentos");
    document.getElementById("listaAgendamentos").innerHTML = dados.map(item => `
        <tr><td>${escapar(item.cliente)}</td><td>${escapar(item.barbeiro)}</td>
        <td>${escapar(item.servico)}</td><td>${escapar(item.data)}</td>
        <td>${escapar(item.horario)}</td><td><span class="status">${escapar(item.status)}</span></td>
        <td><button class="acao" onclick="mudarStatus(${item.id})">Status</button>
        <button class="acao perigo" onclick="excluirItem('agendamentos',${item.id})">Excluir</button></td></tr>`).join("");
}

document.getElementById("formCliente").addEventListener("submit", async evento => {
    evento.preventDefault();
    const dados = {
        nome: document.getElementById("clienteNome").value,
        telefone: document.getElementById("clienteTelefone").value,
        email: document.getElementById("clienteEmail").value
    };
    try {
        await api("/api/clientes", "POST", dados);
        evento.target.reset(); avisar("Cliente cadastrado."); await carregarTudo();
    } catch (erro) { avisar(erro.message, true); }
});

document.getElementById("formBarbeiro").addEventListener("submit", async evento => {
    evento.preventDefault();
    const dados = {
        nome: document.getElementById("barbeiroNome").value,
        telefone: document.getElementById("barbeiroTelefone").value,
        especialidade: document.getElementById("barbeiroEspecialidade").value
    };
    try {
        await api("/api/barbeiros", "POST", dados);
        evento.target.reset(); avisar("Barbeiro cadastrado."); await carregarTudo();
    } catch (erro) { avisar(erro.message, true); }
});

document.getElementById("formServico").addEventListener("submit", async evento => {
    evento.preventDefault();
    const dados = {
        nome: document.getElementById("servicoNome").value,
        preco: document.getElementById("servicoPreco").value,
        duracao: document.getElementById("servicoDuracao").value,
        descricao: document.getElementById("servicoDescricao").value
    };
    try {
        await api("/api/servicos", "POST", dados);
        evento.target.reset(); avisar("Serviço cadastrado."); await carregarTudo();
    } catch (erro) { avisar(erro.message, true); }
});

document.getElementById("formAgendamento").addEventListener("submit", async evento => {
    evento.preventDefault();
    const dados = {
        cliente_id: document.getElementById("agCliente").value,
        barbeiro_id: document.getElementById("agBarbeiro").value,
        servico_id: document.getElementById("agServico").value,
        data: document.getElementById("agData").value,
        horario: document.getElementById("agHorario").value
    };
    try {
        await api("/api/agendamentos", "POST", dados);
        evento.target.reset(); avisar("Agendamento criado."); await carregarTudo();
    } catch (erro) { avisar(erro.message, true); }
});

async function editarCliente(id) {
    const nome = prompt("Novo nome do cliente:");
    if (nome === null) return;
    const telefone = prompt("Novo telefone:");
    if (telefone === null) return;
    const email = prompt("Novo e-mail:") || "";
    try {
        await api(`/api/clientes/${id}`, "PUT", { nome, telefone, email });
        avisar("Cliente atualizado."); await carregarTudo();
    } catch (erro) { avisar(erro.message, true); }
}

async function editarBarbeiro(id) {
    const nome = prompt("Novo nome do barbeiro:");
    if (nome === null) return;
    const telefone = prompt("Novo telefone:") || "";
    const especialidade = prompt("Especialidade:") || "";
    try {
        await api(`/api/barbeiros/${id}`, "PUT", { nome, telefone, especialidade });
        avisar("Barbeiro atualizado."); await carregarTudo();
    } catch (erro) { avisar(erro.message, true); }
}

async function editarServico(id) {
    const nome = prompt("Nome do serviço:");
    if (nome === null) return;
    const preco = prompt("Preço:");
    if (preco === null) return;
    const duracao = prompt("Duração em minutos:");
    if (duracao === null) return;
    const descricao = prompt("Descrição:") || "";
    try {
        await api(`/api/servicos/${id}`, "PUT", { nome, preco, duracao, descricao });
        avisar("Serviço atualizado."); await carregarTudo();
    } catch (erro) { avisar(erro.message, true); }
}

async function mudarStatus(id) {
    const status = prompt("Digite: Pendente, Confirmado, Concluido ou Cancelado");
    if (!status) return;
    try {
        await api(`/api/agendamentos/${id}`, "PATCH", { status });
        avisar("Status atualizado."); await carregarTudo();
    } catch (erro) { avisar(erro.message, true); }
}

async function excluirItem(tipo, id) {
    if (!confirm("Tem certeza que deseja excluir este registro?")) return;
    try {
        await api(`/api/${tipo}/${id}`, "DELETE");
        avisar("Registro excluído."); await carregarTudo();
    } catch (erro) { avisar(erro.message, true); }
}

document.querySelectorAll(".aba").forEach(botao => {
    botao.addEventListener("click", () => {
        document.querySelectorAll(".aba").forEach(item => item.classList.remove("ativa"));
        document.querySelectorAll(".painel").forEach(item => item.classList.add("escondido"));
        botao.classList.add("ativa");
        document.getElementById(`painel-${botao.dataset.alvo}`).classList.remove("escondido");
    });
});

document.getElementById("dataHoje").textContent =
    new Date().toLocaleDateString("pt-BR", { weekday: "long", day: "2-digit", month: "long", year: "numeric" });

carregarTudo();
