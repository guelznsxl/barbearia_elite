PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT NOT NULL,
    email TEXT
);

CREATE TABLE IF NOT EXISTS barbeiros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT,
    especialidade TEXT
);

CREATE TABLE IF NOT EXISTS servicos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT,
    preco REAL NOT NULL,
    duracao INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS agendamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    barbeiro_id INTEGER NOT NULL,
    servico_id INTEGER NOT NULL,
    data TEXT NOT NULL,
    horario TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Pendente',
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (barbeiro_id) REFERENCES barbeiros(id),
    FOREIGN KEY (servico_id) REFERENCES servicos(id)
);
