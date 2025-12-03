"""
Proxy Bidding con m < n objetos idénticos en subasta con misma fecha de vencimiento. Definimos 2 clases: Objeto y Postores
"""

class Objeto:
    def __init__(self, ID, reserve_price, min_increment):
        self.ID = ID
        self.reserve_price = reserve_price        # precio de reserva
        self.min_increment = min_increment        # incremento mínimo
        self.current_price = 0.0                  # precio visible actual
        self.highest_bid = 0.0                    # mejor puja declarada
        self.second_highest_bid = 0.0             # segunda mejor puja
        self.highest_bidder = None                # ganador provisional
        self.buyers_count = 0                     # número de pujas observadas

    def enter_price(self):
        # Precio mínimo que un nuevo postor ha de enfrentar de querer ingresar en la subasta
        if self.highest_bidder is None:
            return self.reserve_price
        return self.current_price + self.min_increment

    def __repr__(self):
        return (f"Objeto {self.ID} "
                f"(reserva={self.reserve_price:.2f}, incremento={self.min_increment:.2f}, "
                f"precio={self.current_price:.2f})")



#Consideramos n participantes y m  < n objetos identicos en puja. Cada postor puede estar, a lo sumo, en dos pujas diferentes siempre
#que el la suma de los precios actuales de las pujas no superen a su valoracon y, por tanto, a su pago final
#(no queremos rechazar el articulo por falta de liquidez).


class Postores:
    def __init__(self, ID: int, valoracion):
        self.ID = ID
        self.valoracion = valoracion
        self.pujas = {}  # diccionario. Clave: objetos en puja sobre los que el postor tiene participación. Valor: precio actual del objeto en subasta

    def puede_pujar(self, objeto):
        # Verifica si el postor puede pujar en un objeto dado:
        #Máximo 2 objetos distintos (salvo que ya esté en ese objeto) y la suma de precios visibles + nuevo precio ≤ valoración.
        nuevo_precio = objeto.enter_price()
        total = sum(self.pujas.values())
        return (len(self.pujas) < 2 or objeto in self.pujas) and total + nuevo_precio <= self.valoracion
