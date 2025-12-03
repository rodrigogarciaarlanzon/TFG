import numpy as np
from Class.Class_Multiple_Proxy_Bidding import Objeto, Postores

def arrival_order(n):
    """
    Crea n postores con valoraciones ~ U(0,1) y devuelve
    un np.ndarray permutado aleatoriamente.
    """
    buyers_array = np.empty((0,), dtype=object)
    for i in range(n):
        valoracion = np.random.uniform(0, 1)
        buyer = Postores(ID=f"ID{i+1}", valoracion=valoracion)
        buyers_array = np.append(buyers_array, buyer)
    return np.random.permutation(buyers_array)

def ebay_proxy_bidding_multiple(n, m, reserve_prices: list, min_increments: list):
    biders = arrival_order(n)
    objetos = [Objeto(i+1, reserve_prices[i], min_increments[i]) for i in range(m)]

    print("=== Evolución de la subasta múltiple ===")

    for buyer in biders:
        bid = buyer.valoracion

        # Elegir el objeto con menor precio de entrada entre los que puede pujar
        candidatos = [o for o in objetos if buyer.puede_pujar(o)]
        if not candidatos:
            print(f"\nPostor {buyer.ID} con valoración {bid:.3f} no puede pujar en ningún objeto.")
            continue

        objeto = min(candidatos, key=lambda o: o.enter_price())
        enter_price = objeto.enter_price()

        print(f"\nPujador {buyer.ID} llega con valoración {bid:.3f} y evalúa Objeto {objeto.ID} "
              f"(precio de entrada {enter_price:.3f})")

        # Primera puja en el objeto
        if objeto.highest_bidder is None:
            if bid >= objeto.reserve_price:
                objeto.buyers_count += 1
                objeto.current_price = objeto.reserve_price
                objeto.highest_bid = bid
                objeto.highest_bidder = buyer
                buyer.pujas[objeto.ID] = objeto.current_price
                print(f"Objeto {objeto.ID}: subasta comienza (reserva {objeto.reserve_price:.3f}), "
                      f"precio a batir {objeto.highest_bid:.3f}")
            else:
                print(f"Objeto {objeto.ID}: valoración por debajo de la reserva. Ignorado.")
        else:
            # Pujas subsecuentes
            if bid >= objeto.current_price + objeto.min_increment:
                if bid > objeto.highest_bid:
                    objeto.buyers_count += 1
                    objeto.second_highest_bid = objeto.highest_bid
                    objeto.highest_bid = bid
                    objeto.highest_bidder = buyer
                    print(f"Objeto {objeto.ID}: nuevo líder {buyer.ID} con valoración {bid:.3f}")
                else:
                    objeto.buyers_count += 1
                    objeto.second_highest_bid = max(objeto.second_highest_bid, bid)
                    print(f"Objeto {objeto.ID}: puja aceptada sin superar al líder. "
                          f"Segunda mejor {objeto.second_highest_bid:.3f}")

                # Actualizar precio visible (proxy)
                prev_price = objeto.current_price
                objeto.current_price = min(objeto.highest_bid, objeto.second_highest_bid + objeto.min_increment)
                if objeto.current_price > prev_price:
                    buyer.pujas[objeto.ID] = objeto.current_price
                print(f"Objeto {objeto.ID}: precio visible actualizado {objeto.current_price:.3f}")
            else:
                print(f"Objeto {objeto.ID}: puja demasiado baja respecto a incremento mínimo. Ignorada.")

    print("\n=== Resultados finales ===")
    for obj in objetos:
        if obj.highest_bidder:
            print(f"Objeto {obj.ID}: ganador {obj.highest_bidder.ID} con valoración {obj.highest_bid:.3f}, "
                  f"precio final {obj.current_price:.3f}, pujas observadas {obj.buyers_count}")
        else:
            print(f"Objeto {obj.ID}: sin ganador (no alcanzó reserva)")

    return objetos