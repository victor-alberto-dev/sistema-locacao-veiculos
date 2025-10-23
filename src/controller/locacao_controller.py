from utils.oracle_queries import OracleQueries
from model.locacao import Locacao

class LocacaoController:
    def __init__(self, can_write=False):
        self.db = OracleQueries(can_write=can_write)

    def insert(self, l: Locacao):
        sql = """
        INSERT INTO locacoes 
        (veiculo_id, cliente, data_retirada, data_devolucao_prevista, data_devolucao_real, valor_diario, total, status) 
        VALUES (
            :veiculo_id,
            :cliente,
            TO_DATE(:dr,'YYYY-MM-DD'),
            TO_DATE(:dp,'YYYY-MM-DD'),
            NULL,
            :vd,
            :total,
            :status
        )
        """
        params = {
            'veiculo_id': l.veiculo_id,
            'cliente': l.cliente,
            'dr': l.data_retirada if l.data_retirada else None,
            'dp': l.data_devolucao_prevista if l.data_devolucao_prevista else None,
            'vd': l.valor_diario,
            'total': l.total,
            'status': l.status
        }
        self.db.write(sql, params)

    def list_all(self):
        conn = self.db.connect()
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, veiculo_id, cliente, 
                       TO_CHAR(data_retirada,'YYYY-MM-DD') as data_retirada,
                       TO_CHAR(data_devolucao_prevista,'YYYY-MM-DD') as data_devolucao_prevista,
                       TO_CHAR(data_devolucao_real,'YYYY-MM-DD') as data_devolucao_real,
                       valor_diario, total, status
                FROM locacoes
                ORDER BY id
            """)
            rows = cur.fetchall()
        return rows

    def update(self, id, **kwargs):
        # Converte campos de data para TO_DATE se necessário
        date_fields = ['data_retirada','data_devolucao_prevista','data_devolucao_real']
        set_clauses = []
        params = {'id': id}
        for k,v in kwargs.items():
            if k in date_fields and v:
                set_clauses.append(f"{k} = TO_DATE(:{k}, 'YYYY-MM-DD')")
                params[k] = v
            else:
                set_clauses.append(f"{k} = :{k}")
                params[k] = v
        sql = f"UPDATE locacoes SET {', '.join(set_clauses)} WHERE id = :id"
        self.db.write(sql, params)

    def delete(self, id):
        sql = "DELETE FROM locacoes WHERE id=:id"
        self.db.write(sql, {'id': id})
