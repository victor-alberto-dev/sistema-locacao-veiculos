from utils.oracle_queries import OracleQueries
from utils.mongo_connection import MongoConnection
from model.locacao import Locacao


class LocacaoController:
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
            self.col = self.mongo["locacoes"]

        else:
            raise ValueError("db_type deve ser 'oracle' ou 'mongo'")

    def insert(self, l: Locacao):

        if self.db_type == "oracle":
            sql = """
                INSERT INTO locacoes 
                (veiculo_id, cliente, data_retirada, data_devolucao_prevista, 
                 data_devolucao_real, valor_diario, total, status)
                VALUES (
                    :veiculo_id, :cliente,
                    TO_DATE(:dr,'YYYY-MM-DD'),
                    TO_DATE(:dp,'YYYY-MM-DD'),
                    NULL,
                    :vd, :total, :status
                )
            """

            params = {
                'veiculo_id': l.veiculo_id,
                'cliente': l.cliente,
                'dr': l.data_retirada,
                'dp': l.data_devolucao_prevista,
                'vd': l.valor_diario,
                'total': l.total,
                'status': l.status
            }

            self.db.write(sql, params)

        elif self.db_type == "mongo":
            novo_id = self.col.count_documents({}) + 1
            self.col.insert_one({
                "_id": novo_id,
                "veiculo_id": l.veiculo_id,
                "cliente": l.cliente,
                "data_retirada": l.data_retirada,
                "data_devolucao_prevista": l.data_devolucao_prevista,
                "data_devolucao_real": l.data_devolucao_real,
                "valor_diario": l.valor_diario,
                "total": l.total,
                "status": l.status
            })

    def list_all(self):

        if self.db_type == "oracle":
            query = """
                SELECT id, veiculo_id, cliente,
                       TO_CHAR(data_retirada,'YYYY-MM-DD'),
                       TO_CHAR(data_devolucao_prevista,'YYYY-MM-DD'),
                       TO_CHAR(data_devolucao_real,'YYYY-MM-DD'),
                       valor_diario, total, status
                FROM locacoes
                ORDER BY id
            """
            conn = self.db.connect()
            with conn.cursor() as cur:
                cur.execute(query)
                return cur.fetchall()

        elif self.db_type == "mongo":
            docs = list(self.col.find({}))
            return [
                [
                    d["_id"], d["veiculo_id"], d["cliente"],
                    d.get("data_retirada"), d.get("data_devolucao_prevista"),
                    d.get("data_devolucao_real"), d["valor_diario"],
                    d["total"], d["status"]
                ]
                for d in docs
            ]

    def update(self, id, **kwargs):

        if self.db_type == "oracle":
            date_fields = ['data_retirada','data_devolucao_prevista','data_devolucao_real']
            set_clauses = []
            params = {'id': id}

            for k, v in kwargs.items():
                if k in date_fields and v:
                    set_clauses.append(f"{k} = TO_DATE(:{k}, 'YYYY-MM-DD')")
                    params[k] = v
                else:
                    set_clauses.append(f"{k} = :{k}")
                    params[k] = v

            sql = f"UPDATE locacoes SET {', '.join(set_clauses)} WHERE id = :id"
            self.db.write(sql, params)

        elif self.db_type == "mongo":
            self.col.update_one({"_id": id}, {"$set": kwargs})

    def delete(self, id):

        if self.db_type == "oracle":
            sql = "DELETE FROM locacoes WHERE id=:id"
            self.db.write(sql, {'id': id})

        elif self.db_type == "mongo":
            self.col.delete_one({"_id": id})
