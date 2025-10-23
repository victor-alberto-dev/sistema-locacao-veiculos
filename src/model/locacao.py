class Locacao:
    def __init__(self, id=None, veiculo_id=None, cliente='', data_retirada=None, data_devolucao_prevista=None, data_devolucao_real=None, valor_diario=0.0, total=0.0, status='ativa'):
        self.id = id
        self.veiculo_id = veiculo_id
        self.cliente = cliente
        self.data_retirada = data_retirada
        self.data_devolucao_prevista = data_devolucao_prevista
        self.data_devolucao_real = data_devolucao_real
        self.valor_diario = valor_diario
        self.total = total
        self.status = status

    def __str__(self):
        return f"Locacao(id={self.id}, veiculo_id={self.veiculo_id}, cliente={self.cliente})"
