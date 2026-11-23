
// elementos gerais
const menuToggle = document.getElementById("menuToggle");
const sidebar = document.getElementById("sidebar");
const btnSair = document.getElementById("btnSair");
const btnSairAdmin = document.getElementById("btnSairAdmin");

// abrir e fechar menu no celular
if (menuToggle && sidebar) {
    menuToggle.addEventListener("click", () => {
        sidebar.classList.toggle("open");
    });
}

// sair da conta
async function sair() {
    await fetch("/logout", {
        method: "POST"
    });

    window.location.href = "/login";
}

if (btnSair) {
    btnSair.addEventListener("click", sair);
}

if (btnSairAdmin) {
    btnSairAdmin.addEventListener("click", sair);
}

// funcao para buscar dados da API
async function buscarDados(url) {
    const resposta = await fetch(url);

    if (!resposta.ok) {
        throw new Error("Erro ao buscar informações");
    }

    return await resposta.json();
}

// funcao para enviar dados
async function enviarDados(url, metodo, dados) {
    const resposta = await fetch(url, {
        method: metodo,
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(dados)
    });

    const resultado = await resposta.json();

    if (!resposta.ok) {
        throw new Error(resultado.erro || resultado.mensagem || "Erro na operação");
    }

    return resultado;
}

// evitar que dados sejam interpretados como HTML
function protegerTexto(valor) {
    return String(valor ?? "").replace(/[&<>"']/g, caractere => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;"
    })[caractere]);
}

// LOGIN
const formLogin = document.getElementById("formLogin");

if (formLogin) {
    formLogin.addEventListener("submit", async (evento) => {
        evento.preventDefault();

        const usuario = document.getElementById("usuario").value;
        const senha = document.getElementById("senha").value;
        const mensagem = document.getElementById("loginMensagem");

        try {
            const resultado = await enviarDados("/login", "POST", {
                usuario: usuario,
                senha: senha
            });

            mensagem.textContent = resultado.mensagem || "Login realizado!";
            window.location.href = "/";
        } catch (erro) {
            mensagem.textContent = erro.message;
        }
    });
}

// DASHBOARD
async function carregarResumo() {
    try {
        const dados = await buscarDados("/api/resumo");

        const clientes = document.getElementById("totalClientes");
        const barbeiros = document.getElementById("totalBarbeiros");
        const servicos = document.getElementById("totalServicos");
        const agendamentos = document.getElementById("totalAgendamentos");

        if (clientes) clientes.textContent = dados.clientes ?? 0;
        if (barbeiros) barbeiros.textContent = dados.barbeiros ?? 0;
        if (servicos) servicos.textContent = dados.servicos ?? 0;
        if (agendamentos) agendamentos.textContent = dados.agendamentos ?? 0;

        const adminClientes = document.getElementById("adminTotalClientes");
        const adminBarbeiros = document.getElementById("adminTotalBarbeiros");
        const adminServicos = document.getElementById("adminTotalServicos");
        const adminAgendamentos = document.getElementById("adminTotalAgendamentos");

        if (adminClientes) adminClientes.textContent = dados.clientes ?? 0;
        if (adminBarbeiros) adminBarbeiros.textContent = dados.barbeiros ?? 0;
        if (adminServicos) adminServicos.textContent = dados.servicos ?? 0;
        if (adminAgendamentos) adminAgendamentos.textContent = dados.agendamentos ?? 0;

    } catch (erro) {
        console.log("Não foi possível carregar o resumo:", erro);
    }
}

carregarResumo();

// CLIENTES
const formCliente = document.getElementById("formCliente");

async function carregarClientes() {
    try {
        const dados = await buscarDados("/api/clientes");
        const tabela = document.getElementById("tabelaClientes");

        if (!tabela) return;

        tabela.innerHTML = "";

        dados.forEach(cliente => {
            tabela.innerHTML += `
                <tr>
                    <td>${protegerTexto(cliente.nome)}</td>
                    <td>${protegerTexto(cliente.telefone)}</td>
                    <td>${protegerTexto(cliente.email)}</td>
                    <td>
                        <button onclick="editarCliente(${cliente.id})">Editar</button>
                        <button onclick="excluirCliente(${cliente.id})">Excluir</button>
                    </td>
                </tr>
            `;
        });

    } catch (erro) {
        console.log(erro);
    }
}

if (formCliente) {
    formCliente.addEventListener("submit", async evento => {
        evento.preventDefault();

        const id = document.getElementById("clienteId").value;

        const dados = {
            nome: document.getElementById("clienteNome").value,
            telefone: document.getElementById("clienteTelefone").value,
            email: document.getElementById("clienteEmail").value
        };

        try {
            await enviarDados(
                id ? `/api/clientes/${id}` : "/api/clientes",
                id ? "PUT" : "POST",
                dados
            );

            document.getElementById("mensagemCliente").textContent = "Cliente salvo com sucesso!";
            formCliente.reset();
            document.getElementById("clienteId").value = "";

            carregarClientes();
            carregarResumo();

        } catch (erro) {
            document.getElementById("mensagemCliente").textContent = erro.message;
        }
    });
}

async function editarCliente(id) {
    const dados = await buscarDados("/api/clientes");
    const cliente = dados.find(item => item.id === id);

    if (!cliente) return;

    document.getElementById("clienteId").value = cliente.id;
    document.getElementById("clienteNome").value = cliente.nome;
    document.getElementById("clienteTelefone").value = cliente.telefone;
    document.getElementById("clienteEmail").value = cliente.email;
}

async function excluirCliente(id) {
    if (!confirm("Deseja excluir este cliente?")) return;

    try {
        await enviarDados(`/api/clientes/${id}`, "DELETE");
        carregarClientes();
        carregarResumo();
    } catch (erro) {
        alert(erro.message);
    }
}

const btnAtualizarClientes = document.getElementById("btnAtualizarClientes");

if (btnAtualizarClientes) {
    btnAtualizarClientes.addEventListener("click", carregarClientes);
}

if (document.getElementById("tabelaClientes")) {
    carregarClientes();
}

// BARBEIROS
const formBarbeiro = document.getElementById("formBarbeiro");

async function carregarBarbeiros() {
    try {
        const dados = await buscarDados("/api/barbeiros");
        const tabela = document.getElementById("tabelaBarbeiros");

        if (!tabela) return;

        tabela.innerHTML = "";

        dados.forEach(barbeiro => {
            tabela.innerHTML += `
                <tr>
                    <td>${protegerTexto(barbeiro.nome)}</td>
                    <td>${protegerTexto(barbeiro.telefone)}</td>
                    <td>${protegerTexto(barbeiro.especialidade)}</td>
                    <td>
                        <button onclick="editarBarbeiro(${barbeiro.id})">Editar</button>
                        <button onclick="excluirBarbeiro(${barbeiro.id})">Excluir</button>
                    </td>
                </tr>
            `;
        });

    } catch (erro) {
        console.log(erro);
    }
}

if (formBarbeiro) {
    formBarbeiro.addEventListener("submit", async evento => {
        evento.preventDefault();

        const id = document.getElementById("barbeiroId").value;

        const dados = {
            nome: document.getElementById("barbeiroNome").value,
            telefone: document.getElementById("barbeiroTelefone").value,
            especialidade: document.getElementById("barbeiroEspecialidade").value
        };

        try {
            await enviarDados(
                id ? `/api/barbeiros/${id}` : "/api/barbeiros",
                id ? "PUT" : "POST",
                dados
            );

            document.getElementById("mensagemBarbeiro").textContent = "Barbeiro salvo com sucesso!";
            formBarbeiro.reset();
            document.getElementById("barbeiroId").value = "";

            carregarBarbeiros();
            carregarResumo();

        } catch (erro) {
            document.getElementById("mensagemBarbeiro").textContent = erro.message;
        }
    });
}

async function editarBarbeiro(id) {
    const dados = await buscarDados("/api/barbeiros");
    const barbeiro = dados.find(item => item.id === id);

    if (!barbeiro) return;

    document.getElementById("barbeiroId").value = barbeiro.id;
    document.getElementById("barbeiroNome").value = barbeiro.nome;
    document.getElementById("barbeiroTelefone").value = barbeiro.telefone;
    document.getElementById("barbeiroEspecialidade").value = barbeiro.especialidade;
}

async function excluirBarbeiro(id) {
    if (!confirm("Deseja excluir este barbeiro?")) return;

    try {
        await enviarDados(`/api/barbeiros/${id}`, "DELETE");
        carregarBarbeiros();
        carregarResumo();
    } catch (erro) {
        alert(erro.message);
    }
}

const btnAtualizarBarbeiros = document.getElementById("btnAtualizarBarbeiros");

if (btnAtualizarBarbeiros) {
    btnAtualizarBarbeiros.addEventListener("click", carregarBarbeiros);
}

if (document.getElementById("tabelaBarbeiros")) {
    carregarBarbeiros();
}

// SERVICOS
const formServico = document.getElementById("formServico");

async function carregarServicos() {
    try {
        const dados = await buscarDados("/api/servicos");
        const tabela = document.getElementById("tabelaServicos");

        if (!tabela) return;

        tabela.innerHTML = "";

        dados.forEach(servico => {
            tabela.innerHTML += `
                <tr>
                    <td>${protegerTexto(servico.nome)}</td>
                    <td>${protegerTexto(servico.descricao)}</td>
                    <td>R$ ${Number(servico.preco).toFixed(2)}</td>
                    <td>${protegerTexto(servico.duracao)} min</td>
                    <td>
                        <button onclick="editarServico(${servico.id})">Editar</button>
                        <button onclick="excluirServico(${servico.id})">Excluir</button>
                    </td>
                </tr>
            `;
        });

    } catch (erro) {
        console.log(erro);
    }
}

if (formServico) {
    formServico.addEventListener("submit", async evento => {
        evento.preventDefault();

        const id = document.getElementById("servicoId").value;

        const dados = {
            nome: document.getElementById("servicoNome").value,
            descricao: document.getElementById("servicoDescricao").value,
            preco: Number(document.getElementById("servicoPreco").value),
            duracao: Number(document.getElementById("servicoDuracao").value)
        };

        try {
            await enviarDados(
                id ? `/api/servicos/${id}` : "/api/servicos",
                id ? "PUT" : "POST",
                dados
            );

            document.getElementById("mensagemServico").textContent = "Serviço salvo com sucesso!";
            formServico.reset();
            document.getElementById("servicoId").value = "";

            carregarServicos();
            carregarResumo();

        } catch (erro) {
            document.getElementById("mensagemServico").textContent = erro.message;
        }
    });
}

async function editarServico(id) {
    const dados = await buscarDados("/api/servicos");
    const servico = dados.find(item => item.id === id);

    if (!servico) return;

    document.getElementById("servicoId").value = servico.id;
    document.getElementById("servicoNome").value = servico.nome;
    document.getElementById("servicoDescricao").value = servico.descricao;
    document.getElementById("servicoPreco").value = servico.preco;
    document.getElementById("servicoDuracao").value = servico.duracao;
}

async function excluirServico(id) {
    if (!confirm("Deseja excluir este serviço?")) return;

    try {
        await enviarDados(`/api/servicos/${id}`, "DELETE");
        carregarServicos();
        carregarResumo();
    } catch (erro) {
        alert(erro.message);
    }
}

const btnAtualizarServicos = document.getElementById("btnAtualizarServicos");

if (btnAtualizarServicos) {
    btnAtualizarServicos.addEventListener("click", carregarServicos);
}

if (document.getElementById("tabelaServicos")) {
    carregarServicos();
}

// AGENDAMENTOS
const formAgendamento = document.getElementById("formAgendamento");

async function carregarOpcoesAgendamento() {
    try {
        const clientes = await buscarDados("/api/clientes");
        const barbeiros = await buscarDados("/api/barbeiros");
        const servicos = await buscarDados("/api/servicos");

        const campoCliente = document.getElementById("agendamentoCliente");
        const campoBarbeiro = document.getElementById("agendamentoBarbeiro");
        const campoServico = document.getElementById("agendamentoServico");

        if (campoCliente) {
            campoCliente.innerHTML = '<option value="">Selecione um cliente</option>';
            clientes.forEach(item => {
                campoCliente.innerHTML += `<option value="${item.id}">${protegerTexto(item.nome)}</option>`;
            });
        }

        if (campoBarbeiro) {
            campoBarbeiro.innerHTML = '<option value="">Selecione um barbeiro</option>';
            barbeiros.forEach(item => {
                campoBarbeiro.innerHTML += `<option value="${item.id}">${protegerTexto(item.nome)}</option>`;
            });
        }

        if (campoServico) {
            campoServico.innerHTML = '<option value="">Selecione um serviço</option>';
            servicos.forEach(item => {
                campoServico.innerHTML += `<option value="${item.id}">${protegerTexto(item.nome)}</option>`;
            });
        }

    } catch (erro) {
        console.log(erro);
    }
}

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

if (formAgendamento) {
    carregarOpcoesAgendamento();

    formAgendamento.addEventListener("submit", async evento => {
        evento.preventDefault();

        const id = document.getElementById("agendamentoId").value;

        const dados = {
            cliente_id: Number(document.getElementById("agendamentoCliente").value),
            barbeiro_id: Number(document.getElementById("agendamentoBarbeiro").value),
            servico_id: Number(document.getElementById("agendamentoServico").value),
            data: document.getElementById("agendamentoData").value,
            horario: document.getElementById("agendamentoHorario").value,
            status: document.getElementById("agendamentoStatus").value
        };

        try {
            await enviarDados(
                id ? `/api/agendamentos/${id}` : "/api/agendamentos",
                id ? "PATCH" : "POST",
                dados
            );

            document.getElementById("mensagemAgendamento").textContent = "Agendamento salvo com sucesso!";
            formAgendamento.reset();
            document.getElementById("agendamentoId").value = "";

            carregarAgendamentos();
            carregarResumo();

        } catch (erro) {
            document.getElementById("mensagemAgendamento").textContent = erro.message;
        }
    });
}

async function excluirAgendamento(id) {
    if (!confirm("Deseja excluir este agendamento?")) return;

    try {
        await enviarDados(`/api/agendamentos/${id}`, "DELETE");
        carregarAgendamentos();
        carregarResumo();
    } catch (erro) {
        alert(erro.message);
    }
}

const btnAtualizarAgendamentos = document.getElementById("btnAtualizarAgendamentos");

if (btnAtualizarAgendamentos) {
    btnAtualizarAgendamentos.addEventListener("click", carregarAgendamentos);
}

if (document.getElementById("tabelaAgendamentos")) {
    carregarAgendamentos();
}

// data atual no dashboard
const dataHoje = document.getElementById("dataHoje");

if (dataHoje) {
    dataHoje.textContent = new Date().toLocaleDateString("pt-BR");
}
