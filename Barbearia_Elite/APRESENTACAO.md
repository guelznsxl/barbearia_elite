# Guia de apresentação — Barbearia Elite

## 1. Apresentação da ideia
"Meu projeto é o Barbearia Elite, um sistema web para organizar clientes, barbeiros, serviços e agendamentos. A ideia é diminuir a desorganização dos horários e centralizar os cadastros."

## 2. Explicar as tecnologias
- HTML estrutura a página.
- CSS define cores, espaçamentos e responsividade.
- JavaScript controla os formulários e atualiza a tela.
- Fetch envia requisições do navegador para o Flask.
- Flask recebe as requisições e disponibiliza as rotas da API.
- Python e POO organizam as classes e regras.
- Os DAOs fazem as operações no SQLite.
- SQLite armazena os dados.

## 3. Explicar POO
"As classes Cliente, Barbeiro, Servico e Agendamento representam os elementos do sistema. Cada objeto guarda os dados de um registro. Os DAOs separam as operações do banco da parte das rotas."

## 4. Explicar o banco
- clientes: dados dos clientes.
- barbeiros: dados dos profissionais.
- servicos: nome, preço e duração.
- agendamentos: liga cliente, barbeiro e serviço, além de data, horário e status.

## 5. Demonstração sugerida
1. Cadastrar um cliente.
2. Cadastrar um barbeiro.
3. Cadastrar um serviço.
4. Criar um agendamento.
5. Tentar criar outro agendamento para o mesmo barbeiro, data e horário e mostrar a validação.
6. Alterar o status para Confirmado.
7. Mostrar os dados atualizados na tela e no banco.

## 6. Perguntas que podem aparecer
**O que é Flask?**  
É um framework Python usado para criar aplicações web e rotas.

**O que é DAO?**  
É um padrão que separa o acesso ao banco de dados do restante do programa.

**O que é Fetch?**  
É um recurso JavaScript que faz requisições HTTP sem precisar recarregar a página inteira.

**Por que usar SQLite?**  
Porque é simples de configurar e suficiente para a demonstração acadêmica.

**O que é chave estrangeira?**  
É um campo que relaciona uma tabela a outra, como `cliente_id` em agendamentos.

**Como funciona o relacionamento?**  
Um cliente pode ter vários agendamentos, mas cada agendamento está ligado a um cliente específico.

## 7. Limitações conhecidas
O sistema é demonstrativo: não tem autenticação de usuários, pagamentos, notificações, nem bloqueio de horários por duração sobreposta. A validação atual impede dois agendamentos no mesmo horário exato para o mesmo barbeiro.
