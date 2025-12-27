import numpy as np
from Class.Class_Multiple_Proxy_Bidding import Objeto, Buyer

def multiple_arrival_order(n: int):
    """
    Genera un conjunto de n compradores independientes con valoraciones
    distribuidas uniformemente en el intervalo [0, 1], y devuelve un
    orden de llegada aleatorio para ser utilizado en una subasta.

    Para cada comprador i:
        - Se asigna un identificador único "ID{i}".
        - Se genera una valoración privada v_i ~ U(0,1).
        - Se crea una instancia de Buyer con dicha valoración.

    Los compradores se almacenan en un array de objetos y posteriormente
    se devuelve una permutación aleatoria del mismo, que representa el
    orden de llegada efectivo en la subasta (mecanismo secuencial).

    Args:
        n (int): Número total de compradores a generar.

    Returns:
        np.ndarray: Array de objetos Buyer permutado aleatoriamente,
                        representando el orden de llegada.
    """
    buyers_array = np.empty((0,), dtype=object)
    for i in range(n):
        valoracion = np.random.uniform(0, 1)
        buyer = Buyer(ID=f"ID{i+1}", valoracion=valoracion)
        buyers_array = np.append(buyers_array, buyer)
    return np.random.permutation(buyers_array)

def ebay_proxy_bidding_multiple(n: int, m: int, reserve_prices: list, min_increments: list,
                               biders = None, max_iter: int = 10000):
    """
    Implementa un mecanismo de Proxy Bidding para m objetos simultáneos,
    replicando exactamente la lógica del proxy bidding individual en cada objeto.

    Dinámica del mecanismo:

    - Cada objeto j funciona como una subasta eBay independiente:
        * highest_bid_j: puja máxima declarada (privada)
        * second_highest_bid_j: segunda mayor puja
        * current_price_j = min(highest_bid_j, second_highest_bid_j + d_j)

    - Cada buyer i tiene una valoración v_i y solo puede competir en un objeto
      a la vez (bienes sustitutivos perfectos).

    - Si el current_price del objeto donde está compitiendo supera su valoración,
      el buyer abandona automáticamente esa subasta.

    - Si no está en ningún objeto, el buyer entra en el objeto viable cuyo
      enter_price sea menor (regla greedy):
            enter_price = reserva si no ha empezado, current_price + d si ya ha empezado.

    - El proceso continúa iterativamente hasta alcanzar un punto fijo
      (ningún buyer cambia de objeto) o hasta max_iter iteraciones.

    Args:

        n (int): Número total de postores.
        m (int): Número total de objetos en subasta.
        reserve_prices (list): Lista con los valoraciones del objeto.
        min_increments (list): Lista de incrementos mínimos de puja para cada objeto.
        max_iter (int): Máximo número de iteraciones para evitar bucles infinitos.

    Returns:

    objetos : list[Objeto]
        Lista de objetos con su estado final (ganador, current_price, etc.).
    """

    # Generamos orden de llegada y objetos
    if biders is None:
        biders = multiple_arrival_order(n)
    objetos = [Objeto(i+1, reserve_prices[i], min_increments[i]) for i in range(m)]
    objetos_by_id = {obj.ID: obj for obj in objetos}

    #print(INICIO DE LA SUBASTA MÚLTIPLE)
    #print(f"Total buyers: {n}, Total objetos: {m}\n")

    changed = True
    it = 0
    while changed and it < max_iter:
        changed = False
        it += 1
        #print(f"\n--- Iteración {it} ---")
        for buyer in biders:
            # 1) Si está en un objeto, comprobar si sigue siendo viable
            if buyer.active_object is not None:
                obj = objetos_by_id[buyer.active_object]
                if obj.current_price > buyer.valoracion:
                    #print(f"Buyer {buyer.ID} abandona Objeto {obj.ID} "
                          #f"(current_price {obj.current_price:.3f} > valoración {buyer.valoracion:.3f})")

                    buyer.active_object = None
                    changed = True
            # 2) Si no está en ningún objeto, intentar entrar en uno nuevo
            if buyer.active_object is None:
                candidatos = [o for o in objetos if buyer.puede_pujar(o)]
                if not candidatos:
                    #print(f"Buyer {buyer.ID} (v={buyer.valoracion:.3f}) no puede pujar en ningún objeto.")
                    continue
                # Regla de entrada a nueva puja: objeto con menor enter_price
                objeto = min(candidatos, key=lambda o: o.enter_price())
                ep = objeto.enter_price()
                #print(f"Buyer {buyer.ID} (v={buyer.valoracion:.3f}) evalúa Objeto {objeto.ID} "
                      #f"(enter_price={ep:.3f}, current_price={objeto.current_price:.3f})")

                exito = objeto.registrar_puja(buyer, buyer.valoracion)

                if exito:
                    buyer.active_object = objeto.ID
                    #print(f"Buyer {buyer.ID} entra en Objeto {objeto.ID}, highest_bid={objeto.highest_bid:.3f}, current_price={objeto.current_price:.3f}")
                    changed = True
                else:
                    pass
                    #print(f"Buyer {buyer.ID} no puede entrar en Objeto {objeto.ID}, puja insuficiente.")

    #print(RESULTADOS FINALES)
    #for obj in objetos:
    #    if obj.highest_bidder:
    #       print(f"Objeto {obj.ID}: ganador {obj.highest_bidder.ID}, highest_bid={obj.highest_bid:.3f}, precio_final={obj.current_price:.3f}, bids_aceptadas={obj.buyers_count}")
    #    else:
    #       print(f"Objeto {obj.ID}: sin ganador (no alcanzó reserva {obj.reserve_price:.3f})")

    return objetos
