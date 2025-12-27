import numpy as np

class Licitadores:
    """
    Clase cuyos objetos únicamente tendrán como atributo un ID identificador y la valoración del objeto subastado.
    Tal valoración será una variable aleatoria independiente distribuida según una Uniforme (0 , 1).
    """

    def __init__(self, ID : int):
        self.ID = ID
        self.valoracion = np.random.uniform(0,1)
    def __repr__(self):
        return f"Licitador(ID={self.ID}, valoracion={self.valoracion: .3f})"





