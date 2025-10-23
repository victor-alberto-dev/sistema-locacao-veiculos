# Locadora de Veículos 
**Disciplina:** Banco de Dados  


## Integrantes
- Anderson Moreira
- Gustavo Covre
- Lucas Léllis
- Mayara Hafez
- Victor Alberto

## O que nosso programa faz
- CRUD completo para `categorias`, `veiculos` e `locacoes` (inserir, listar, atualizar, excluir)
- Menu interativo em console para todas as operações
- Relatórios implementados:
  - Total faturado por categoria (GROUP BY)
  - Locações com dados do veículo (JOIN)
- Script SQL completo para criação das tabelas, sequences e triggers
- Diagrama relacional 

## Como usar 
1. Extraia o ZIP e abra o terminal na pasta do projeto.
2. Configure Oracle / DBeaver e rode `src/sql/create_tables.sql` como usuário `labdatabase`.
3. Abra o terminal, crie e ative o ambiente virtual(venv), instale as dependências(arquivo requirements.txt):
   ```bash
   python3 -m venv venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
4. Rode a aplicação:
   ```bash
   python3 src/main.py
   ```
5. No menu principal você terá acesso a CRUDs e relatórios.


