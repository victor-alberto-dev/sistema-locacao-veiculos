from utils.oracle_queries import OracleQueries
from model.categoria import Categoria

class CategoriaController:
    def __init__(self, can_write=False):
        self.db = OracleQueries(can_write=can_write)

    def insert(self, categoria: Categoria):
        query = 'INSERT INTO categorias (nome, descricao) VALUES (:nome, :descricao)'
        self.db.write(query, params={'nome': categoria.nome, 'descricao': categoria.descricao})

    def list_all(self):
        query = 'SELECT id, nome, descricao FROM categorias ORDER BY id'
        return self.db.sqlToMatrix(query)[0]  # retorna apenas os dados como matriz

    def update(self, id, nome, descricao):
        query = 'UPDATE categorias SET nome=:nome, descricao=:descricao WHERE id=:id'
        self.db.write(query, params={'nome': nome, 'descricao': descricao, 'id': id})

    def delete(self, id):
        query = 'DELETE FROM categorias WHERE id=:id'
        self.db.write(query, params={'id': id})
