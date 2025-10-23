class Categoria:
    def __init__(self, id=None, nome='', descricao=''):
        self.id = id
        self.nome = nome
        self.descricao = descricao

    def __str__(self):
        return f"Categoria(id={self.id}, nome={self.nome})"
