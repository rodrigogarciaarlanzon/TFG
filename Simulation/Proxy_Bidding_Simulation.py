import numpy as np
import matplotlib.pyplot as plt
from eBay.Proxy_Bidding import ebay_proxy_bidding, arrival_order



def sim_reserv(n: int, reserve_price: list, min_increment: float, simulations: int):
    """
    Simula el precio final esperado en una subasta eBay Proxy Bidding para distintos precios de reserva.
    Para cada valor en reserve_price, ejecuta múltiples simulaciones independientes del mecanismo
    ebay_proxy_bidding y calcula el precio final promedio observado (solo se consideran las subastas
    que llegan a iniciarse, es decir, aquellas cuyo precio final no es None). Posible implementación en otro trabajos para el caso en que  d = 0 y variabilidad
    en precio de reserva (no lo analizamos, en eBay es obligatorio d > 0).

    Args:
        n (int): Número total de licitadores potenciales.
        reserve_price (list): Lista de precios de reserva a evaluar.
        min_increment (float): Incremento mínimo de puja exigido por el mecanismo.
        simulations (int): Número de simulaciones independientes por cada precio de reserva.Calibrar según potencia del terminal.

    Returns:
        tuple:
            - results (list): Precio final promedio de la subasta para cada
              incremento mínimo.
            - bids (list): Número medio de licitadores que participan efectivamente en la puja para
              cada incremento mínimo.
    """
    results = []
    bids = []
    for r in reserve_price:
        prices = []
        bids_placed = []
        for sim in range(simulations):
            winner, price, buyers_count = ebay_proxy_bidding(n, r, min_increment)
            if price is not None:
                prices.append(price)
                bids_placed.append(buyers_count)
        results.append(np.mean(prices) if prices else 0)
        bids.append(np.mean(bids_placed) if bids_placed else 0)
    return results, bids


def sim_increment(n: int, reserve_price: float, min_increment: list, simulations: int):
    """
    Evalúa cómo varía el precio final y el número de pujas observadas en una subasta eBay Proxy Bidding
    al modificar el incremento mínimo de puja. Manteniendo fijo el precio de reserva y el orden
    de llegada de los licitadores, la función ejecuta múltiples simulaciones para cada valor de
    min_increment, calculando el precio final promedio y el número medio de licitadores que
    efectivamente participan en la puja.

    Args:
        n (int): Número total de licitadores potenciales.
        reserve_price (float): Precio de reserva de la subasta.
        min_increment (list): Lista de incrementos mínimos de puja a evaluar.
        simulations (int): Número de simulaciones independientes por cada incremento mínimo.Calibrar según potencia del terminal.
        Returns:
            tuple:
                - results (list): Precio final promedio de la subasta para cada
                  incremento mínimo.
                - bids (list): Número medio de licitadores que participan
                  efectivamente en la puja para cada incremento mínimo.

    """
    results = []
    bids = []
    for inc in min_increment:
        prices = []
        bids_placed = []
        for sim in range(simulations):
            winner, price, buyers_count = ebay_proxy_bidding(n, reserve_price, inc)
            if price is not None:
                prices.append(price)
                bids_placed.append(buyers_count)
        results.append(np.mean(prices) if prices else 0)
        bids.append(np.mean(bids_placed) if bids_placed else 0)
    return results, bids


def ejecutar_simulaciones_d(n: int, max_min_increment: float):
    """
    Ejecuta simulaciones del mecanismo eBay Proxy Bidding y genera gráficos
    que muestran cómo varía el precio medio de venta según el incremento
    mínimo de puja. La función fija el precio de reserva en 0 (el ingreso esperado se maximiza en s = 0, d = 1/4
    para dos pujadores según la obra de Rogers et al.) y evalúa una serie de incrementos mínimos
    equiespaciados entre 0 y max_min_increment. Para cada valor, se
    calcula el precio medio final mediante sim_increment, y se representa
    gráficamente su evolución.

    Args:
        n (int): Número total de licitadores potenciales.
        max_min_increment (float): Valor máximo del rango de incrementos
            mínimos de puja a simular.

    Returns:
        None: La función no retorna valores; muestra en pantalla un gráfico
            con la evolución del precio medio de venta en función del incremento
            mínimo.
    """
    # Rango equiespaciado de incrementos mínimos. num = 20 según las figuras del trabajo de Roges et al.
    Min_increment = np.linspace(0, max_min_increment, 20)
    # Los autores consideran la condición s +2d < 1. Para s = 0:
    if np.any(Min_increment > 0.5):
        print("Violación de la condición s + 2d < 1")
    if n == 2:
        results_increment = sim_increment(n, min_increment = Min_increment, reserve_price= 0, simulations = 10000)
        # Gráficos. Evolución del precio medio de venta dependiente del incremento mínimo de puja.
        plt.rcParams['font.family'] = 'Times New Roman'
        plt.rcParams['font.size'] = 14
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot( Min_increment,results_increment[0],marker='o',color='darkorange',linewidth=2,markersize=6)
        # Título y ejes
        #ax.set_title("Ingreso Esperado de la Subasta vs Incremento Mínimo", fontsize=18)
        ax.set_xlabel("Incremento Mínimo de Puja d", fontsize=16)
        ax.set_ylabel("Ingreso Esperado de la Subasta", fontsize=16)
        # Eje Y desde 0.2 hasta 0.5
        ax.set_ylim(0.2, 0.5)
        # El eje X se coloca en y = 0.2
        ax.spines['bottom'].set_position(('data', 0.2))
        # El eje Y se coloca en x = 0
        ax.spines['left'].set_position(('data', 0))
        # Ocultar ejes superior y derecho
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        # Cuadrícula suave
        ax.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()
    else:
        results_increment = sim_increment(n, min_increment=Min_increment, reserve_price=0, simulations = 1000)
        # Gráficos. Evolución del precio medio de venta dependiente del incremento mínimo de puja.
        plt.rcParams['font.family'] = 'Times New Roman'
        plt.rcParams['font.size'] = 14
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(Min_increment,results_increment[0],marker='o',color='darkorange',linewidth=2,markersize=6)
        # Títulos y ejes
        #ax.set_title("Ingreso Esperado de la Subasta vs Incremento Mínimo", fontsize=18)
        ax.set_xlabel("Incremento Mínimo de Puja d", fontsize=16)
        ax.set_ylabel("Ingreso Esperado de la Subasta", fontsize=16)
        # Eje Y desde 0.8 hasta 0.95
        ax.set_ylim(0.8, 0.95)
        # El eje X se coloca en y = 0.8
        ax.spines['bottom'].set_position(('data', 0.8))
        # El eje Y se coloca en x = 0
        ax.spines['left'].set_position(('data', 0))
        # Ocultar ejes superior y derecho
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        # Cuadrícula suave
        ax.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()


def ejecutar_simulaciones_s(n: int, max_reserv_price: float):
    """
    Ejecuta simulaciones del mecanismo eBay Proxy Bidding y genera gráficos
    que muestran cómo varía el precio medio de venta según el precio de reserva. La función fija el incremento mínimo de puja en
    1/4 (el ingreso esperado se maximiza en s = 0, d = 1/4 para dos pujadores según la obra de Rogers et al.) y evalúa una serie
    de precios de reserva equiespaciados entre 0 y max_reserv_price. Para cada valor, se
    calcula el precio medio final mediante sim_reserv y se representa gráficamente su evolución.
    Los autores no consideran el estudio de este caso para N = 2. Posible implementación posterior por nuestra cuenta.

    Args:
        n (int): Número total de licitadores potenciales.
        max_reserv_price (float): Valor máximo del rango de incrementos
            mínimos de puja a simular.

    Returns:
        None: La función no retorna valores; muestra en pantalla un gráfico
            con la evolución del precio medio de venta en función del incremento
            mínimo.
    """

    # Rango equiespaciado del precio de reserva. num = 20 según las figuras del trabajo de Roges et al.
    Reserv_price = np.linspace(0, max_reserv_price, 20)
    # Los autores consideran la condición s +2d < 1. Para s = 0:
    if np.any(Reserv_price > 0.5):
        print("Violación de la condición s + 2d < 1")
    if n == 2:
        results_reserv = sim_reserv(n, Reserv_price, min_increment=0.25, simulations = 10000)
        # Gráficos. Evolución del precio medio de venta dependiente del incremento mínimo de puja.
        plt.rcParams['font.family'] = 'Times New Roman'
        plt.rcParams['font.size'] = 14
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot( Reserv_price,results_reserv[0],marker='o',color='darkorange',linewidth=2,markersize=6)
        # Título y ejes
        ax.set_title("Auction Revenue vs Reserv Price", fontsize=18)
        ax.set_xlabel("Reserv Price", fontsize=16)
        ax.set_ylabel("Expected auction revenue", fontsize=16)
        # Eje Y desde 0.2 hasta 0.5
        ax.set_ylim(0.2, 0.5)
        # El eje X se coloca en y = 0.2
        ax.spines['bottom'].set_position(('data', 0.2))
        # El eje Y se coloca en x = 0
        ax.spines['left'].set_position(('data', 0))
        # Ocultar ejes superior y derecho
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        # Cuadrícula suave
        ax.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()
    else:
        results_reserv = sim_reserv(n, Reserv_price, min_increment=0.25, simulations=1000)
        # Gráficos. Evolución del precio medio de venta dependiente del incremento mínimo de puja.
        plt.rcParams['font.family'] = 'Times New Roman'
        plt.rcParams['font.size'] = 14
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(Reserv_price, results_reserv[0], marker='o', color='darkorange', linewidth=2, markersize=6)
        # Título y ejes
        ax.set_title("Auction Revenue vs Reserv Price", fontsize=18)
        ax.set_xlabel("Reserv Price", fontsize=16)
        ax.set_ylabel("Expected auction revenue", fontsize=16)
        # Eje Y desde 0.2 hasta 0.5
        ax.set_ylim(0.8, 0.95)
        # El eje X se coloca en y = 0.8
        ax.spines['bottom'].set_position(('data', 0.8))
        # El eje Y se coloca en x = 0
        ax.spines['left'].set_position(('data', 0))
        # Ocultar ejes superior y derecho
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        # Cuadrícula suave
        ax.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()

def comparacion_simulaciones(n, max_min_increment, sims):
    """
    Función idéntica a ejecutar simulaciones_d pero sin plotear los gráficos directamente.
    Lo usaremos para el caso N > 2.

    """
    Min_increment = np.linspace(0, max_min_increment, 20)
    results_increment, bids = sim_increment(n, min_increment=Min_increment, reserve_price=0, simulations  = sims)
    return Min_increment, results_increment, bids


def sim_bids_fixed_d(n, reserve_price, d, simulations):
    """
    Estima el número medio de pujadores efectivos en una subasta eBay Proxy Bidding
    con un único objeto, manteniendo fijo el incremento mínimo de puja `d`.

    Para cada simulación:
     - Se genera un orden de llegada explícito mediante arrival_order(n).
     - Se ejecuta la subasta proxy con:
                  * precio de reserva = reserve_price
                  * incremento mínimo = d
                  * orden de llegada = biders
     - Se registra el número total de compradores que han realizado al menos
              una puja aceptada (buyers_count).

    Tras repetir este proceso `simulations` veces, la función devuelve la media
    del número de pujadores observados. Esto permite analizar cómo el incremento
    mínimo afecta a la intensidad competitiva de la subasta.

    Args:
        n (int): Número total de compradores potenciales.
        reserve_price (float): Precio de reserva del objeto.
        d (float): Incremento mínimo de puja.
        simulations (int): Número de simulaciones independientes.

    Returns:
        float: Número medio de pujadores efectivos.
    """

    buyers_counts = []
    for _ in range(simulations):
        biders = arrival_order(n)  # orden de llegada explícito
        winner, price, buyers_count = ebay_proxy_bidding(n=n, reserve_price=reserve_price,min_increment=d,biders=biders)
        buyers_counts.append(buyers_count)
    return np.mean(buyers_counts)


def prob_win_order(n: int, d_values: list, sims: int):
    """
    Estima la probabilidad de victoria de un licitador según su posición de llegada
    en el orden aleatorio de la subasta eBay Proxy Bidding.

    Para cada valor de incremento mínimo `d` en `d_values y s = 0, la función ejecuta
    múltiples simulaciones independientes. En cada simulación se genera un orden
    aleatorio de llegada, se ejecuta la subasta y se registra si el licitador que
    ocupa la posición k en dicho orden resulta ganador. El resultado final es un
    diccionario que asigna a cada `d` un vector de probabilidades de victoria por
    posición de llegada.

    Args:
        n (int): Número total de licitadores potenciales.
        d_values (list): Lista de valores del incremento mínimo de puja a evaluar.
        sims (int): Número de simulaciones independientes por cada valor de `d`.

    Returns:
        dict:
            Diccionario donde cada clave es un valor de `d` y cada valor asociado
            es un array de longitud `n` que contiene la probabilidad estimada de
            victoria para cada posición de llegada (0 = primer licitador en llegar).
    """

    resultados = {d: np.zeros(n) for d in d_values}

    for d in d_values:
        #print(f"\nSimulando d = {d}")
        for k in range(n):
            wins = 0
            for sim in range(sims):
                #  Orden de llegada
                order = arrival_order(n)
                # Ejecutamos la subasta
                winner, price, buyers_count = ebay_proxy_bidding(n, 0, d, biders=order)
                # Postor que llegó en posición k
                postor_k = order[k]
                # ¿Ganó?
                if winner is not None and winner.ID == postor_k.ID:
                    wins += 1
            resultados[d][k] = wins / sims
    return resultados



def prob_kth_max_val_wins_by_position(n, d_values, sims, k):
    """
    Estima la probabilidad de victoria del licitador con la k-ésima mayor valoración
    condicionada a su posición de llegada en la subasta. Para cada valor de incremento mínimo `d` en `d_values`, la función ejecuta
    múltiples simulaciones del mecanismo eBay Proxy Bidding. En cada simulación:

        - Se genera un orden aleatorio de llegada.
        - Se identifica al licitador con la k-ésima mayor valoración.
        - Se evalúa su probabilidad de ganar en tres escenarios:
            * first: llega en primera posición.
            * random: llega en una posición aleatoria.
            * last: llega en última posición.

    Args:
        n (int): Número total de licitadores potenciales.
        d_values (list): Lista de valores del incremento mínimo de puja a evaluar.
        sims (int): Número de simulaciones independientes por cada valor de `d`.
        k (int): Índice de la valoración objetivo (1 = mayor valoración, 2 = segunda mayor, etc.).

    Returns:
        dict:
            Diccionario con tres claves: "first", "random" y "last". Cada clave
            contiene una lista donde el i-ésimo elemento es la probabilidad
            estimada de victoria del licitador k-ésimo más valorado para el
            valor d_values[i].

    """

    if k < 1 or k > n:
        raise ValueError("k debe estar entre 1 y n")

    #Función auxiliar para obtener el índice k-esimo mayor
    def get_kth_index(vals, k):
        idx_sorted = np.argsort(vals)
        return idx_sorted[-k]   # k-ésimo mayor

    results = { "first": [], "random": [], "last": [] }

    for d in d_values:
        #print(f"\nSimulando d = {d}")
        wins = { "first": 0, "random": 0, "last": 0 }
        for _ in range(sims):
            # Generamos orden de llegada
            order = arrival_order(n)
            vals = np.array([buyer.valoracion for buyer in order])
            # Identificamos al licitador objetivo
            idx_target = get_kth_index(vals, k)
            bidder_target = order[idx_target]

            # CASO 1: Llega primero
            order_first = np.array(order, dtype=object)
            order_first[[0, idx_target]] = order_first[[idx_target, 0]]
            winner, price, _ = ebay_proxy_bidding(n, 0, d, biders=order_first)
            if winner and winner.ID == bidder_target.ID:
                wins["first"] += 1

            # CASO 2: Llega aleatorio
            order_random = np.array(order, dtype=object)
            pos_random = np.random.randint(0, n)
            order_random[[pos_random, idx_target]] = order_random[[idx_target, pos_random]]
            winner, price, _ = ebay_proxy_bidding(n, 0, d, biders=order_random)
            if winner and winner.ID == bidder_target.ID:
                wins["random"] += 1

            # CASO 3: Llega último
            order_last = np.array(order, dtype=object)
            order_last[[n-1, idx_target]] = order_last[[idx_target, n-1]]
            winner, price, _ = ebay_proxy_bidding(n, 0, d, biders=order_last)
            if winner and winner.ID == bidder_target.ID:
                wins["last"] += 1

        # Guardamos probabilities
        for key in results:
            results[key].append(wins[key] / sims)

    return results



def plot_probabilities(d_values, results, k):
    """
    Grafica P(gana | llega en posición X) para el k-ésimo mayor valorador.
    results proviene de prob_kth_max_val_wins_by_position()
    """
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size'] = 14
    fig, ax = plt.subplots(figsize=(10,6))
    # Eje X = valores reales de d
    x = d_values
    for key in results:
        ax.plot(x, results[key], marker='o', linewidth=2, label=key)
        # Etiqueta al final de cada curva
        ax.text(x[-1],results[key][-1],key,fontsize=14,ha='left',va='bottom')
    #ax.set_title(f"Figura 6({ 'a' if k==1 else 'c' }) — Probability winning k={k}", fontsize=18)
    ax.set_xlabel("Incremento Mínimo de Puja d", fontsize=16)
    ax.set_ylabel("Probabilidad de Ganar la Subasta", fontsize=16)
    # Ejes
    ax.set_ylim(bottom=0)
    ax.spines['bottom'].set_position(('data', 0))
    ax.spines['left'].set_position(('data', 0))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend()
    plt.tight_layout()
    plt.show()



def expected_profit_k_ght_max_valuation_by_position(n, d_values, sims, k):
    """
    Estima el beneficio esperado del licitador con la k-ésima mayor valoración
    condicionado a su posición de llegada en la subasta.

    Para cada valor del incremento mínimo `d` en `d_values`, la función ejecuta
    múltiples simulaciones del mecanismo eBay Proxy Bidding. En cada simulación:

    - Se genera un orden aleatorio de llegada.
    - Se identifica al licitador con la k-ésima mayor valoración.
    - Se calcula su beneficio (valoración − precio pagado) en tres escenarios:
        * first: llega en primera posición.
        * random: llega en una posición aleatoria.
        * last: llega en última posición.

     El beneficio es cero cuando el licitador no gana la subasta.

    Args:
        n (int): Número total de licitadores potenciales.
        d_values (list): Lista de valores del incremento mínimo de puja a evaluar.
        sims (int): Número de simulaciones independientes por cada valor de `d`.
        k (int): Índice de la valoración objetivo (1 = mayor valoración, 2 = segunda mayor, etc.).

    Returns:
        dict:
            Diccionario con tres claves: "first", "random" y "last". Cada clave
            contiene una lista donde el i-ésimo elemento es el beneficio esperado
            del licitador k-ésimo más valorado para el valor d_values[i].
    """

    if k < 1 or k > n:
        raise ValueError("k debe estar entre 1 y n")

    # Función auxiliar para obtener el índice k-esimo mayor
    def get_kth_index(vals, k):
        idx_sorted = np.argsort(vals)
        return idx_sorted[-k]  # k-ésimo mayor

    results = {"first": [], "random": [], "last": []}

    for d in d_values:
        #print(f"\nSimulando beneficios para d = {d}")
        profits = {"first": [], "random": [], "last": []}
        for _ in range(sims):
            # Generamos orden de llegada
            order = arrival_order(n)
            vals = np.array([buyer.valoracion for buyer in order])
            # Identificamos al licitador objetivo (k-ésimo mayor)
            idx_target = get_kth_index(vals, k)
            bidder_target = order[idx_target]

            # CASO 1: Llega primero
            order_first = np.array(order, dtype=object)
            order_first[[0, idx_target]] = order_first[[idx_target, 0]]
            winner, price, _ = ebay_proxy_bidding(n, 0, d, biders=order_first)
            profits["first"].append(bidder_target.valoracion - price if winner and winner.ID == bidder_target.ID else 0)

            # CASO 2: Llega aleatorio
            order_random = np.array(order, dtype=object)
            pos_random = np.random.randint(0, n)
            order_random[[pos_random, idx_target]] = order_random[[idx_target, pos_random]]
            winner, price, _ = ebay_proxy_bidding(n, 0, d, biders=order_random)
            profits["random"].append(bidder_target.valoracion - price if winner and winner.ID == bidder_target.ID else 0)

            #CASO 3: Llega último
            order_last = np.array(order, dtype=object)
            order_last[[n - 1, idx_target]] = order_last[[idx_target, n - 1]]
            winner, price, _ = ebay_proxy_bidding(n, 0, d, biders=order_last)
            profits["last"].append(bidder_target.valoracion - price if winner and winner.ID == bidder_target.ID else 0)

        # Guardamos probabilities
        for key in results:
            results[key].append(np.mean(profits[key]))

    return results


def plot_expected_profits(d_values, results, k):
    """
    Grafica los beneficios esperados para cada regla de llegada según expected_profit_k_ght_max_valuation_by_position().
    """
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size'] = 14
    fig, ax = plt.subplots(figsize=(10, 6))
    # Eje X = valores reales de d
    x = d_values
    for key in results:
        ax.plot(x, results[key], marker='o', linewidth=2, label=key)
        # Etiqueta al final de cada curva
        ax.text(x[-1],results[key][-1],key,fontsize=14,ha='left',va='bottom')

    #ax.set_title(f"Figura 6({'b' if k == 1 else 'd'}) — Expected profit for k={k}", fontsize=18)
    ax.set_xlabel("Incremento Mínimo de Puja d", fontsize=16)
    ax.set_ylabel("Beneficio Esperado", fontsize=16)
    # Ejes
    ax.set_ylim(bottom=0)
    ax.spines['bottom'].set_position(('data', 0))
    ax.spines['left'].set_position(('data', 0))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend()
    plt.tight_layout()
    plt.show()
