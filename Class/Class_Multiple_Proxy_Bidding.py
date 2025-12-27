

import numpy as np

class Objeto:
    """
    Representa un objeto subastado en un mecanismo eBay Proxy Bidding.

    Cada objeto mantiene su propio estado interno:
            - reserve_price: precio de reserva.
            - min_increment: incremento mínimo de puja.
            - highest_bid: puja máxima declarada hasta el momento.
            - second_highest_bid: segunda mayor puja declarada.
            - current_price: precio actual visible para los compradores.
            - highest_bidder: comprador que lidera la subasta del objeto.
            - buyers_count: número total de pujas aceptadas.

    El objeto implementa la misma lógica que una subasta eBay individual:
        * Si no hay pujas, el precio de entrada es la reserva.
        * Si ya hay pujas, el precio de entrada es current_price + min_increment.
        * Cuando un comprador registra una puja:
                - Si su valoración no alcanza el precio de entrada, la puja se ignora.
                - Si supera el precio de entrada:
                    · Se actualizan highest_bid y second_highest_bid.
                    · Se actualiza el current_price según la regla: current_price = min(highest_bid,second_highest_bid + min_increment)

    Esta clase se utiliza como componente básico dentro del mecanismo
    multiobjeto, donde cada objeto funciona como una subasta independiente.

    """
    def __init__(self, ID, reserve_price, min_increment):
        self.ID = ID
        self.reserve_price = reserve_price
        self.min_increment = min_increment

        self.current_price = 0.0
        self.highest_bid = 0.0
        self.second_highest_bid = 0.0

        self.highest_bidder = None
        self.buyers_count = 0

    def enter_price(self):
        """
        Devuelve el precio de entrada requerido para pujar en este objeto.

            - Si no hay pujas previas, el precio de entrada es el precio de reserva.
            - Si ya existe un highest_bidder, el precio de entrada es:
                        current_price + min_increment

        Returns:
                 float: precio mínimo necesario para que una puja sea aceptada.

        """
        if self.highest_bidder is None:
            return self.reserve_price
        else:
            return self.current_price + self.min_increment

    def registrar_puja(self, buyer, bid_max):
        """
        Intenta registrar una puja proxy para este objeto.

        La puja se interpreta como la valoración máxima del postor (bid_max),
        siguiendo la lógica del mecanismo eBay Proxy Bidding:

            - Si bid_max < enter_price, la puja se ignora.
            - Si es válida:
                * Se incrementa buyers_count.
                * Si no había pujas previas:
                        highest_bid = bid_max
                        highest_bidder = buyer
                        current_price = reserve_price
                * Si ya había pujas:
                    · Si bid_max supera highest_bid:
                            second_highest_bid = highest_bid
                            highest_bid = bid_max
                            highest_bidder = buyer
                    · En caso contrario:
                            second_highest_bid = max(second_highest_bid, bid_max)

                * El precio actual se actualiza como:
                    current_price = min(highest_bid,second_highest_bid + min_increment)

        Args:
            buyer (Buyer): comprador que realiza la puja.
            bid_max (float): valoración máxima declarada por el comprador.

        Returns:
            bool: True si la puja fue aceptada, False si fue ignorada.

        """

        enter_price = self.enter_price()
        if bid_max < enter_price:
            # Puja demasiado baja: ignorada
            return False
        self.buyers_count += 1
        if self.highest_bidder is None:
            # Primera puja que alcanza la reserva
            self.highest_bid = bid_max
            self.highest_bidder = buyer
            self.current_price = self.reserve_price
        else:
            if bid_max > self.highest_bid:
                self.second_highest_bid = self.highest_bid
                self.highest_bid = bid_max
                self.highest_bidder = buyer
            else:
                self.second_highest_bid = max(self.second_highest_bid, bid_max)
            self.current_price = min(self.highest_bid,self.second_highest_bid + self.min_increment)
        return True


class Buyer:
    def __init__(self, ID, valoracion):
        """
        Representa un comprador en el mecanismo de subasta.

        Cada comprador tiene:
            - ID: identificador único.
            - valoracion: su valoración privada del objeto.
            - active_object: identificador del objeto en el que está compitiendo
                                 actualmente (None si no participa en ninguno).

        El comprador solo puede competir en un objeto a la vez, lo que refleja
        bienes perfectamente sustitutivos en el caso multiobjeto.

        """

        self.ID = ID
        self.valoracion = valoracion
        # El buyer solo puede estar compitiendo activamente en un objeto
        self.active_object = None

    def puede_pujar(self, objeto: Objeto) -> bool:
        """
        Determina si el comprador puede pujar en un objeto dado.

        Reglas:
            - Si el objeto no tiene pujas previas: el comprador debe tener valoración >= precio de reserva.
            - Si ya hay pujas: debe tener valoración >= current_price + min_increment.

        Args:
            objeto (Objeto): objeto en el que se evalúa la posibilidad de pujar.

        Returns:
            bool: True si puede pujar, False en caso contrario.

        """
        # Si no hay pujas, debe superar la reserva
        if objeto.highest_bidder is None:
            return self.valoracion >= objeto.reserve_price

        # Si ya hay pujas, debe superar current_price + incremento
        return self.valoracion >= objeto.current_price + objeto.min_increment


