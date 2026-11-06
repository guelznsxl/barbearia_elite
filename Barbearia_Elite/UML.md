# Diagrama UML — Barbearia Elite

```mermaid
classDiagram
    class Cliente {
        +int id
        +str nome
        +str telefone
        +str email
    }
    class Barbeiro {
        +int id
        +str nome
        +str telefone
        +str especialidade
    }
    class Servico {
        +int id
        +str nome
        +str descricao
        +float preco
        +int duracao
    }
    class Agendamento {
        +int id
        +int cliente_id
        +int barbeiro_id
        +int servico_id
        +str data
        +str horario
        +str status
    }
    Cliente "1" --> "0..*" Agendamento : realiza
    Barbeiro "1" --> "0..*" Agendamento : atende
    Servico "1" --> "0..*" Agendamento : corresponde
```

## Relacionamentos
- Um cliente pode realizar vários agendamentos.
- Um barbeiro pode atender vários agendamentos.
- Um serviço pode aparecer em vários agendamentos.
- Cada agendamento pertence a um cliente, um barbeiro e um serviço.
