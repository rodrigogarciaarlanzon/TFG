import numpy as np
from Class.Class_Proxy_Bidding import Licitadores


def arrival_order(n: int) -> np.ndarray:
    """
    Genera un orden de llegada aleatorio para los licitadores de la subasta.
    Crea `n` instancias de `Licitadores`, las almacena en un array de NumPy y
    devuelve una permutación aleatoria del mismo, representando el orden de
    llegada estocástico tal y como se refleja en el trabajo de
    A. Rogers, E. David, N. R. Jennings, and J. Schiff (2007). “The Effects of Proxy Bidding
    and Minimum Bid Increments within eBay Auctions.”

    Args:
        n (int): Número total de licitadores potenciales.
    Returns:
        np.ndarray: Array unidimensional de objetos `Licitadores` permutado
        aleatoriamente.

    """

    buyers_array = np.empty((0,), dtype=object)
    for i in range(n):
        buyer = Licitadores(ID=f"ID{i+1}")
        buyers_array = np.append(buyers_array, buyer)
    return np.random.permutation(buyers_array)


def ebay_proxy_bidding(n, reserve_price: float, min_increment: float, biders = None):
    """
    Implementa el mecanismo de Proxy Bidding utilizado en subastas tipo eBay.
    El algoritmo simula la dinámica de pujas automáticas: cada licitador entra
    con su máxima valoración privada y el sistema actualiza el precio visible siguiendo
    las reglas de eBay (precio de reserva, incrementos mínimos y puja máxima).
    Si no se proporciona un orden de llegada, se genera uno aleatorio mediante
    arrival_order. Se incluyen comentarios para captar la dinámica y lógica de la subasta a modo
    de trial para una subasta de eBay.


        Args:
            n (int): Número total de licitadores potenciales.
            reserve_price (float): Precio de reserva que debe alcanzarse para que
                la subasta comience.
            min_increment (float): Incremento mínimo requerido para superar la puja
                visible actual.
            biders (np.ndarray | None): Array opcional con objetos `Licitadores`
                que define el orden de llegada. Si es `None`, se genera uno nuevo.

        Returns:
            tuple:
                - highest_bidder (Licitadores | None): Ganador de la subasta o
                  `None` si nadie alcanza el precio de reserva.
                - current_price (float): Precio final visible de la subasta.
                - Buyers (int): Número de licitadores que efectivamente participan
                  (aquellos cuya valoración entra en el algoritmo Proxy Biding).

    """

    if biders is None:
        biders = arrival_order(n)
    current_price = 0
    highest_bid = 0
    second_highest_bid = 0
    highest_bidder = None

    #print("Evolución de la subasta")

    # Contabilizamos el número de pujadores que verdaderamente toman participación (ingresan) en la puja.
    # Es decir, su valoración ingresa en el algoritmo Proxy Bidding.
    Buyers = 0
    for i, buyer in enumerate(biders):
        bid = buyer.valoracion
        #print(f"\nPujador {buyer.ID} ingresa con valoración {bid:.3f}")
        if i == 0:
            # Primer pujador
            if bid >= reserve_price:
                Buyers += 1
                current_price = reserve_price
                highest_bid = bid
                highest_bidder = buyer
                #print(f"La subasta comienza: precio de reserva {reserve_price:.3f}, "
                      #f"precio a batir {highest_bid:.3f}")
            else:
                #print("No alcanza el precio de reserva. Subasta no comienza.")
                return None, reserve_price, 0
        else:
            # Siguientes licitadores
            if bid < reserve_price:
                #print("No alcanza el precio de reserva. Ignorado.")
                continue
            if bid >= current_price + min_increment:
                if bid > highest_bid:
                    Buyers += 1
                    second_highest_bid = highest_bid
                    highest_bid = bid
                    highest_bidder = buyer
                    #print(f"Nuevo líder: {buyer.ID} con valoración {bid:.3f}")
                else:
                    Buyers += 1
                    second_highest_bid = max(second_highest_bid, bid)
                    #print(f"Puja aceptada pero no supera al líder. "
                          #f"Segunda mejor puja: {second_highest_bid:.3f}")
                # Ajuste del precio visible
                current_price = min(highest_bid, second_highest_bid + min_increment)
                #print(f"Precio visible actualizado: {current_price:.3f}")
            else:
                pass
                #print("Puja demasiado baja. Ignorada.")

    #print("Resultado final")
    if highest_bidder:
        pass
        #print(f"Ganador: {highest_bidder.ID} con valoración {highest_bid:.3f}")
        #print(f"Precio final de la subasta: {current_price:.3f}")
        #print((f"Número de pujas observadas: {Buyers:.3f}"))
    else:
        pass
        #print("Subasta inválida: nadie alcanzó el precio de reserva")

    return highest_bidder, current_price, Buyers



