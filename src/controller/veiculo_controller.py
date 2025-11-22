from utils.oracle_queries import OracleQueries
from utils.mongo_connection import MongoConnection
from model.veiculo import Veiculo


class VeiculoController:
    def __init__(self, can_write=False, dbtype="oracle"):
        """
        dbtype:
            - "oracle": usa somente Oracle
            - "mongo": usa somente MongoDB
        """

        self.dbtype = dbtype

        if dbtype == "oracle":
            self.db = OracleQueries(can_write=can_write)

        elif dbtype == "mongo":
            self.mongo = MongoConnection().get_db()
            self.col = self.mongo["veiculos"]

    def insert(self, v: Veiculo):

        if self.dbtype == "oracle":
            sql = """
                INSERT INTO veiculos 
                (placa, modelo, marca, ano, cor, status, kilometragem, categoria_id)
                VALUES (:placa, :modelo, :marca, :ano, :cor, :status, :kilometragem, :categoria_id)
            """

            params = {
                'placa': v.placa, 'modelo': v.modelo, 'marca': v.marca,
                'ano': v.ano, 'cor': v.cor, 'status': v.status,
                'kilometragem': v.kilometragem, 'categoria_id': v.categoria_id
            }

            self.db.write(sql, params=params)

        elif self.dbtype == "mongo":
            self.col.insert_one({
                "placa": v.placa,
                "modelo": v.modelo,
                "marca": v.marca,
                "ano": v.ano,
                "cor": v.cor,
                "status": v.status,
                "kilometragem": v.kilometragem,
                "categoria_id": v.categoria_id
            })

    def list_all(self):
        if self.dbtype != "oracle":
            return []  # sem Oracle

        sql = """
            SELECT id, placa, modelo, marca, ano, cor, status, kilometragem, categoria_id
            FROM veiculos ORDER BY id
        """
        return self.db.sqlToMatrix(sql)

    def list_all_mongo(self):
        if self.dbtype != "mongo":
            return []  # sem Mongo

        docs = list(self.col.find({}))
        lista = []
        for d in docs:
            lista.append([
                d.get("_id"), d["placa"], d["modelo"], d["marca"], d["ano"],
                d["cor"], d["status"], d["kilometragem"], d["categoria_id"]
            ])
        return lista

    def update(self, id, **kwargs):

        if self.dbtype == "oracle":
            fields = ', '.join([f"{k}=:{k}" for k in kwargs.keys()])
            params = kwargs.copy()
            params['id'] = id

            sql = f"UPDATE veiculos SET {fields} WHERE id=:id"
            self.db.write(sql, params=params)

        elif self.dbtype == "mongo":
            self.col.update_one({"_id": id}, {"$set": kwargs})

    def delete(self, id):

        if self.dbtype == "oracle":
            sql = "DELETE FROM veiculos WHERE id=:id"
            self.db.write(sql, {'id': id})

        elif self.dbtype == "mongo":
            self.col.delete_one({"_id": id})
