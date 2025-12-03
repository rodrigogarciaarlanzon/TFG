""""
Creamos una clase llamada Licitadores, cuyos objetos (los licitadores),
únicamente tendrán como atributo un ID identificador y la valoración del objeto subastado. Tal valoración
se distribuirá según una variable aleatoria independiente  Uniforme en el intervalo 0 , 1
"""

import random

class Licitadores:
    def __init__(self, ID : int):
        self.ID = ID
        self.valoracion = random.uniform(0,1)
    def __repr__(self):
        return f"Licitador(ID={self.ID}, valoracion={self.valoracion: .3f})"





