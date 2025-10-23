class Veiculo:
    def __init__(self, id=None, placa='', modelo='', marca='', ano=None, cor='', status='disponivel', kilometragem=0.0, categoria_id=None):
        self.id = id
        self.placa = placa
        self.modelo = modelo
        self.marca = marca
        self.ano = ano
        self.cor = cor
        self.status = status
        self.kilometragem = kilometragem
        self.categoria_id = categoria_id

    def __str__(self):
        return f"Veiculo(id={self.id}, placa={self.placa}, modelo={self.modelo})"
