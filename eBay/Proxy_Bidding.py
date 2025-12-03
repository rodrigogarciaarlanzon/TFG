"""
Primera aproximación mecanismo Proxy Bidding

"""

import numpy as np
from Class.Class_Proxy_Bidding import Licitadores

#Función con parámetro de entrada n, número de licitadores en la subasta. Retorna un array de numpy tras realizar
#una permutación aleatoria de las valoraciones de los pujadores para capturar el carácter aleaatorio de ingreso en la subasta
#tal y como se refleja en el trabajo de A. Rogers, E. David, N. R. Jennings, and J. Schiff (2007). “The Effects of Proxy Bidding
# and Minimum Bid Increments within eBay Auctions.”

def arrival_order(n) -> np.ndarray:

    buyers_array = np.empty((0,), dtype=object)
    for i in range(n):
        buyer = Licitadores(ID=f"ID{i+1}")
        buyers_array = np.append(buyers_array, buyer)
    return np.random.permutation(buyers_array)


#Mecanismo subasta Proxy Bidding. Dependinete del número de licitadors, precio de reserva e incremento mínimo de puja

def ebay_proxy_bidding(n, reserve_price, min_increment):
    biders = arrival_order(n)
    current_price = 0
    highest_bid = 0
    second_highest_bid = 0
    highest_bidder = None

    print("=== Evolución de la subasta ===")

    for i, buyer in enumerate(biders):
        bid = buyer.valoracion
        print(f"\nPujador {buyer.ID} ingresa con valoración {bid:.3f}")

        if i == 0:
            # Primer pujador
            Buyers = 0 #Contabilizamos el número de pujadores que verdaderamente toman participación (ingresan) en la puja. Es decir, su valoración ingresa en el algoritmo Proxy Bidding
            if bid >= reserve_price:
                Buyers += 1
                current_price = reserve_price
                highest_bid = bid
                highest_bidder = buyer
                print(f"La subasta comienza: precio de reserva {reserve_price:.3f}, "
                      f"precio a batir {highest_bid:.3f}")
            else:
                print("No alcanza el precio de reserva. Subasta no comienza.")
                return None, reserve_price
        else:
            # Siguientes licitadores
            if bid < reserve_price:
                print("No alcanza el precio de reserva. Ignorado.")
                continue

            if bid >= current_price + min_increment:
                if bid > highest_bid:
                    Buyers += 1
                    second_highest_bid = highest_bid
                    highest_bid = bid
                    highest_bidder = buyer
                    print(f"Nuevo líder: {buyer.ID} con valoración {bid:.3f}")
                else:
                    Buyers += 1
                    second_highest_bid = max(second_highest_bid, bid)
                    print(f"Puja aceptada pero no supera al líder. "
                          f"Segunda mejor puja: {second_highest_bid:.3f}")

                # Ajuste del precio visible
                current_price = min(highest_bid, second_highest_bid + min_increment)
                print(f"Precio visible actualizado: {current_price:.3f}")
            else:
                print("Puja demasiado baja. Ignorada.")

    print("\n=== Resultado final ===")
    if highest_bidder:
        print(f"Ganador: {highest_bidder.ID} con valoración {highest_bid:.3f}")
        print(f"Precio final de la subasta: {current_price:.3f}")
        print((f"Número de pujas observadas: {Buyers:.3f}"))
    else:
        print("Subasta inválida: nadie alcanzó el precio de reserva")

    return highest_bidder, current_price



