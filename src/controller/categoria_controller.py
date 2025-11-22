from utils.oracle_queries import OracleQueries
from utils.mongo_connection import MongoConnection
from model.categoria import Categoria


class CategoriaController:
    def __init__(self, db_type="oracle", can_write=False):
        """
        db_type: "oracle" ou "mongo"
        """
        self.db_type = db_type

        if db_type == "oracle":
            self.db = OracleQueries(can_write=can_write)
            self.mongo = None
            self.col = None

        elif db_type == "mongo":
            self.db = None
            self.mongo = MongoConnection().get_db()
            self.col = self.mongo["categorias"]

        else:
            raise ValueError("db_type deve ser 'oracle' ou 'mongo'")

    def insert(self, categoria: Categoria):
        if self.db_type == "oracle":
            query = """
                INSERT INTO categorias (nome, descricao)
                VALUES (:nome, :descricao)
            """
            self.db.write(query, params={
                "nome": categoria.nome,
                "descricao": categoria.descricao
            })

        elif self.db_type == "mongo":
            novo_id = self.col.count_documents({}) + 1
            self.col.insert_one({
                "_id": novo_id,
                "nome": categoria.nome,
                "descricao": categoria.descricao
            })

    def list_all(self):
        if self.db_type == "oracle":
            query = "SELECT id, nome, descricao FROM categorias ORDER BY id"
            return self.db.sqlToMatrix(query)[0]

        elif self.db_type == "mongo":
            docs = list(self.col.find({}))
            return [[d["_id"], d["nome"], d["descricao"]] for d in docs]

    def update(self, id, nome, descricao):
        if self.db_type == "oracle":
            query = """
                UPDATE categorias 
                SET nome=:nome, descricao=:descricao 
                WHERE id=:id
            """
            self.db.write(query, params={
                "nome": nome,
                "descricao": descricao,
                "id": id
            })

        elif self.db_type == "mongo":
            self.col.update_one(
                {"_id": id},
                {"$set": {"nome": nome, "descricao": descricao}}
            )

    def delete(self, id):
        if self.db_type == "oracle":
            query = "DELETE FROM categorias WHERE id=:id"
            self.db.write(query, params={"id": id})

        elif self.db_type == "mongo":
            self.col.delete_one({"_id": id})
