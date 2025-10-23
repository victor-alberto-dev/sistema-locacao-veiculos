from utils.oracle_queries import OracleQueries
from model.veiculo import Veiculo

class VeiculoController:
    def __init__(self, can_write=False):
        self.db = OracleQueries(can_write=can_write)

    def insert(self, v: Veiculo):
        query = ("INSERT INTO veiculos (placa, modelo, marca, ano, cor, status, kilometragem, categoria_id) "
                 "VALUES (:placa, :modelo, :marca, :ano, :cor, :status, :kilometragem, :categoria_id)")
        self.db.write(query, params={
            'placa': v.placa, 'modelo': v.modelo, 'marca': v.marca, 'ano': v.ano,
            'cor': v.cor, 'status': v.status, 'kilometragem': v.kilometragem,
            'categoria_id': v.categoria_id
        })

    def list_all(self):
        query = 'SELECT id, placa, modelo, marca, ano, cor, status, kilometragem, categoria_id FROM veiculos ORDER BY id'
        return self.db.sqlToMatrix(query)[0]

    def update(self, id, **kwargs):
        fields = ', '.join([f"{k}=:{k}" for k in kwargs.keys()])
        params = kwargs.copy()
        params['id'] = id
        query = f'UPDATE veiculos SET {fields} WHERE id=:id'
        self.db.write(query, params=params)

    def delete(self, id):
        query = 'DELETE FROM veiculos WHERE id=:id'
        self.db.write(query, params={'id': id})
