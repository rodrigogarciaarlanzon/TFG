import numpy as np
import matplotlib.pyplot as plt
from eBay.Multiple_Proxy_Bidding import ebay_proxy_bidding_multiple, multiple_arrival_order

def generar_parametros(m: int,reserv_base: float,increment_base: float,sigma_reserve=0.05,sigma_increment=0.002):
    """
    Genera los parámetros heterogéneos (precio de reserva e incremento mínimo)
    para cada uno de los m objetos en una subasta múltiple eBay Proxy Bidding.

    Para cada objeto j se construyen:
        - reserve_j  = reserv_base   + N(0, sigma_reserve)
        - increment_j = increment_base + N(0, sigma_increment)
    donde el término gaussiano introduce heterogeneidad entre objetos.
    Ambos valores se truncan para garantizar no negatividad:
            * reserve_j   >= 0
            * increment_j >= 1e-4

    El primer objeto utiliza exactamente los valores base proporcionados
    (reserv_base, increment_base), y los restantes incorporan ruido estocástico.

    Args:
        m (int): Número total de objetos.
        reserv_base (float): Precio de reserva base común.
        increment_base (float): Incremento mínimo base común.
        sigma_reserve (float): Desviación típica del ruido en los precios de reserva.
        sigma_increment (float): Desviación típica del ruido en los incrementos mínimos.

    Returns:
        tuple:
            reserv_price (list[float]): Lista de precios de reserva generados.
            min_increment (list[float]): Lista de incrementos mínimos generados.

    """

    reserv_price = [reserv_base]
    min_increment = [increment_base]

    for j in range(m-1):
        s_j = reserv_base + np.random.normal(0, sigma_reserve)
        s_j = max(0.0, s_j)  #no negatividad
        d_j = increment_base + np.random.normal(0, sigma_increment)
        d_j = max(1e-4, d_j)  # no negatividad

        reserv_price.append(s_j)
        min_increment.append(d_j)

    return reserv_price, min_increment

def sim_reserv_multiple(n: int,m: int,reserve_price_list: list,min_increment: float,
    simulations: int,sigma_reserve: float = 0.05,sigma_increment: float = 0.002):
    """
    Simula el precio final medio POR OBJETO en una subasta eBay Proxy Bidding
    con m < n objetos idénticos para distintos precios de reserva.

    Para cada valor en reserve_price_list:
        - Se ejecutan `simulations` subastas independientes.
        - En cada subasta se generan parámetros heterogéneos para los m objetos:
              reserve_j = s + N(0, sigma_reserve)
              increment_j = min_increment + N(0, sigma_increment)
        - Se registran los precios finales de todos los objetos vendidos.
        - Se promedia sobre objetos y simulaciones.

    Args:
        n (int): Número total de postores.
        m (int): Número total de objetos.
        reserv_base (float): Precio de reserva base común.
        increment_base (float): Incremento mínimo base común.
        sigma_reserve (float): Desviación típica del ruido en los precios de reserva.
        sigma_increment (float): Desviación típica del ruido en los incrementos mínimos.

    Returns:
        results (list): precio final medio por objeto para cada s.
        bids    (list): número medio de pujadores por objeto para cada s.

    """

    results = []
    bids = []
    for s in reserve_price_list:
        all_prices = []
        all_buyers_counts = []
        for _ in range(simulations):
            # Generamos parámetros heterogéneos para los m objetos
            reserv_list, incr_list = generar_parametros(m,reserv_base=s,increment_base=min_increment,
                sigma_reserve=sigma_reserve,sigma_increment=sigma_increment)
            # Ejecutamos la subasta múltiple
            objetos = ebay_proxy_bidding_multiple(n, m, reserv_list, incr_list)
            # Recogemos resultados por objeto
            for obj in objetos:
                if obj.highest_bidder is not None:
                    all_prices.append(obj.current_price)
                    all_buyers_counts.append(obj.buyers_count)
        avg_price = np.mean(all_prices) if all_prices else 0.0
        avg_buyers = np.mean(all_buyers_counts) if all_buyers_counts else 0.0
        results.append(avg_price)
        bids.append(avg_buyers)
    return results, bids

def sim_increment_multiple(n: int,m: int,reserve_price: float,min_increment_list: list,
    simulations: int,sigma_reserve: float = 0.05,sigma_increment: float = 0.002):
    """
    Simula el precio final medio POR OBJETO en una subasta eBay Proxy Bidding
    con m < n objetos idénticos para distintos incrementos mínimos de puja.

    Para cada valor de min_increment_list:
        - Se ejecutan simulations subastas independientes.
        - En cada subasta se generan parámetros heterogéneos para los m objetos:
              reserve_j = s + N(0, sigma_reserve)
              increment_j = min_increment + N(0, sigma_increment)
        - Se registran los precios finales de todos los objetos vendidos.
        - Se promedia sobre objetos y simulaciones.

    Args:
        n (int): Número total de postores.
        m (int): Número total de objetos.
        reserv_base (float): Precio de reserva base común.
        increment_base (float): Incremento mínimo base común.
        sigma_reserve (float): Desviación típica del ruido en los precios de reserva.
        sigma_increment (float): Desviación típica del ruido en los incrementos mínimos.

    Returns:
        results (list): precio final medio por objeto para cada s.
        bids    (list): número medio de pujadores por objeto para cada s.
    """

    results = []
    bids = []
    for d in min_increment_list:
        all_prices = []
        all_buyers_counts = []
        for _ in range(simulations):
            # Generamos parámetros heterogéneos para los m objetos
            reserv_list, incr_list = generar_parametros(m,reserv_base=reserve_price,increment_base=d,
                sigma_reserve=sigma_reserve,sigma_increment=sigma_increment)
            # Ejecutamos subasta múltiple
            objetos = ebay_proxy_bidding_multiple(n, m, reserv_list, incr_list)
            # Recogemos resultados por objeto
            for obj in objetos:
                if obj.highest_bidder is not None:
                    all_prices.append(obj.current_price)
                    all_buyers_counts.append(obj.buyers_count)
        avg_price = np.mean(all_prices) if all_prices else 0.0
        avg_buyers = np.mean(all_buyers_counts) if all_buyers_counts else 0.0
        results.append(avg_price)
        bids.append(avg_buyers)
    return results, bids

def comparacion_simulaciones_multiple(n: int, m:int , max_min_increment: int, sims: int):
    """
    Función análoga a comparacion_simulaciones del caso uniobjeto,
    pero para el caso de m objetos en subasta simultánea.

    - s = 0 fijo (igual que en el caso uniobjeto)
    - Se varía d en [0, max_min_increment]
    - Para cada d se ejecutan 'sims' simulaciones multiobjeto
    Returns:
        Min_increment: lista de d
        results_increment: revenue medio POR OBJETO
        bids: número medio de pujadores POR OBJETO

    """

    Min_increment = np.linspace(0, max_min_increment, 20)
    results_increment, bids = sim_increment_multiple(n=n,m=m,reserve_price=0,
        min_increment_list=Min_increment,simulations=sims)
    return Min_increment, results_increment, bids


def sim_bids_fixed_d_multiple(n:int, m: int, reserve_price: float, d:float, simulations,sigma_reserve=0.05, sigma_increment=0.002):
    """
    Estima el número medio de pujadores POR OBJETO en una subasta múltiple
    eBay Proxy Bidding, fijando:
        - n compradores
        - m objetos
        - precio de reserva base = reserve_price
        - incremento mínimo base = d

    Para cada simulación:
        - Se generan parámetros heterogéneos para los m objetos:
              reserve_j = reserve_price + N(0, sigma_reserve)
              increment_j = d + N(0, sigma_increment)
        - Se ejecuta la subasta múltiple
        - Se registran los buyers_count de cada objeto vendido

    Args:
        n (int): Número total de compradores.
        m (int): Número total de objetos en subasta.
        reserve_price (float): Precio de reserva base común.
        d (float): Incremento mínimo base común.
        simulations (int): Número de simulaciones independientes.
        sigma_reserve (float): Desviación típica del ruido en los precios de reserva.
        sigma_increment (float): Desviación típica del ruido en los incrementos mínimos.
    Returns:
        float: número medio de pujadores por objeto.

    """

    all_buyers_counts = []
    for _ in range(simulations):
        # Generar parámetros heterogéneos
        reserv_list, incr_list = generar_parametros(m,reserv_base=reserve_price,increment_base=d,
                                                    sigma_reserve=sigma_reserve,sigma_increment=sigma_increment)
        # Ejecutar subasta múltiple
        objetos = ebay_proxy_bidding_multiple(n, m, reserv_list, incr_list)
        # Recoger número de pujadores por objeto
        for obj in objetos:
            if obj.highest_bidder is not None:  # solo objetos vendidos
                all_buyers_counts.append(obj.buyers_count)
    # Media sobre objetos y simulaciones
    return np.mean(all_buyers_counts) if all_buyers_counts else 0.0

def prob_win_order_multiple(n: int, m: int, d_values: list, sims: int):
    """
    Estima la probabilidad de victoria (ganar >= 1 objeto) según la posición
    de llegada en una subasta eBay Proxy Bidding con m objetos.

    Para cada valor de incremento mínimo `d` en `d_values` y s = 0, la función
    ejecuta múltiples simulaciones independientes. En cada simulación se genera
    un orden aleatorio de llegada, se ejecuta la subasta múltiple y se registra
    si el licitador que ocupa la posición k resulta ganador de al menos un objeto.

    Args:
        n (int): Número total de licitadores potenciales.
        m (int): Número de objetos en subasta.
        d_values (list): Lista de valores del incremento mínimo de puja a evaluar.
        sims (int): Número de simulaciones independientes por cada valor de `d`.

    Returns:
        dict:
            Diccionario donde cada clave es un valor de `d` y cada valor asociado
            es un array de longitud `n` que contiene la probabilidad estimada de
            victoria para cada posición de llegada.

    """

    resultados = {d: np.zeros(n) for d in d_values}
    for d in d_values:
        print(f"\nSimulando d = {d}")
        # Para cada posición k
        for k in range(n):
            wins = 0
            for sim in range(sims):
                order = multiple_arrival_order(n)
                # Generamos parámetrosheterogéneos para los m objetos (s=0)
                reserve_prices, min_increments = generar_parametros(m,reserv_base = 0,increment_base = d,sigma_reserve=0.05,sigma_increment=0.002)
                # Subasta múltiple
                objetos = ebay_proxy_bidding_multiple(n, m, reserve_prices, min_increments)
                # Lista de ganadores (IDs)
                winners_ids = [obj.highest_bidder.ID for obj in objetos
                               if obj.highest_bidder is not None]
                # Postor llegada k-esima
                postor_k = order[k]
                # ¿Ganó al menos un objeto?
                if postor_k.ID in winners_ids:
                    wins += 1
            resultados[d][k] = wins / sims
    return resultados

def prob_kth_max_val_wins_by_position_multiple(n:int, m:int, d_values:list, sims:int, k:int):
    """
    Estima la probabilidad de que el licitador con la k‑ésima mayor valoración
    gane al menos un objeto en una subasta múltiple eBay Proxy Bidding,
    condicionada a su posición de llegada.

    El experimento se repite para cada valor del incremento mínimo de puja `d`
    en `d_values`, y para cada `d` se realizan `sims` simulaciones independientes.

    En cada simulación:
        1. Se genera un orden de llegada aleatorio para los n compradores,
            cada uno con valoración independiente ~ U(0,1).
        2. Se identifica al comprador con la k‑ésima mayor valoración dentro
            de ese orden.
        3. Se evalúa su probabilidad de ganar ≥ 1 objeto bajo tres reglas
            de llegada:
                * first  — el comprador objetivo se coloca en la primera posición.
                * random — el comprador objetivo se coloca en una posición aleatoria.
                * last   — el comprador objetivo se coloca en la última posición.

            Para cada caso:
                - Se reordena la lista de compradores según la regla.
                - Se resetea el estado interno de cada comprador (active_object = None).
                - Se generan parámetros heterogéneos para los m objetos:
                        reserve_j   = 0 + N(0, sigma_reserve)
                        increment_j = d + N(0, sigma_increment)
                - Se ejecuta la subasta múltiple mediante ebay_proxy_bidding_multiple().
                - Se comprueba si el comprador objetivo aparece como ganador en alguno de los objetos.

    Finalmente, para cada valor de `d`, la función devuelve la probabilidad
    estimada de victoria del comprador objetivo en cada uno de los tres
    escenarios de llegada.

    Args:
        n (int): Número total de compradores.
        m (int): Número de objetos en subasta.
        d_values (list[float]): Valores del incremento mínimo de puja a evaluar.
        sims (int): Número de simulaciones por cada valor de d.
        k (int): Orden estadístico de la valoración (1 = mayor valoración).

        Returns:
            dict:
                Diccionario con claves "first", "random" y "last".
                Cada clave contiene una lista con la probabilidad estimada
                de victoria para cada valor de d en d_values.
        """

    if k < 1 or k > n:
        raise ValueError("k debe estar entre 1 y n")

    # Auxiliar: índice del k-ésimo mayor
    def get_kth_index(vals, k):
        idx_sorted = np.argsort(vals)
        return idx_sorted[-k]

    results = {"first": [], "random": [], "last": []}
    for d in d_values:
        wins = {"first": 0, "random": 0, "last": 0}
        for _ in range(sims):
            # Orden de llegada multiobjeto
            order = multiple_arrival_order(n)
            vals = np.array([buyer.valoracion for buyer in order])
            # Identificar al licitador objetivo
            idx_target = get_kth_index(vals, k)
            bidder_target = order[idx_target]

            # CASO 1: Llega primero
            order_first = np.array(order, dtype=object)
            order_first[[0, idx_target]] = order_first[[idx_target, 0]]
            for b in order_first:
                b.active_object = None
            reserve_prices, min_increments = generar_parametros(m, reserv_base = 0,increment_base = d,sigma_reserve=0.05,sigma_increment=0.002)
            objetos = ebay_proxy_bidding_multiple(n, m, reserve_prices, min_increments, biders = order_first)
            winners_ids = [obj.highest_bidder.ID for obj in objetos
                if obj.highest_bidder is not None]
            if bidder_target.ID in winners_ids:
                wins["first"] += 1

            # CASO 2: Llega aleatorio
            order_random = np.array(order, dtype=object)
            pos_random = np.random.randint(0, n)
            order_random[[pos_random, idx_target]] = order_random[[idx_target, pos_random]]
            for b in order_random:
                b.active_object = None
            objetos = ebay_proxy_bidding_multiple(n, m, reserve_prices, min_increments, biders = order_random)
            winners_ids = [obj.highest_bidder.ID for obj in objetos
                if obj.highest_bidder is not None]
            if bidder_target.ID in winners_ids:
                wins["random"] += 1

            # CASO 3: Llega último
            order_last = np.array(order, dtype=object)
            order_last[[n-1, idx_target]] = order_last[[idx_target, n-1]]
            for b in order_last:
                b.active_object = None
            objetos = ebay_proxy_bidding_multiple(n, m, reserve_prices, min_increments, biders = order_last)
            winners_ids = [obj.highest_bidder.ID for obj in objetos
                if obj.highest_bidder is not None]
            if bidder_target.ID in winners_ids:
                wins["last"] += 1
        # Guardamos probabilidades
        for key in results:
            results[key].append(wins[key] / sims)

    return results


def plot_probabilities_multiple(d_values, results, k, m):
    """
    Grafica P(gana >= 1 objeto | llega en posición X)
    para el k-ésimo mayor valorador en una subasta con m objetos.

    """

    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size'] = 14
    fig, ax = plt.subplots(figsize=(10,6))
    x = d_values  # eje X = valores de d
    for key in results:
        ax.plot(x, results[key], marker='o', linewidth=2, label=key)
        ax.text(x[-1],results[key][-1],key,fontsize=14,ha='left',va='bottom')

    # Título adaptado al caso multiobjeto
    ax.set_title(f"Figura 9({ 'a' if k==1 else 'c' }) — Probability of winning 1 object (k={k}, m={m})",
        fontsize=18)

    ax.set_xlabel("Minimum bid increment d", fontsize=16)
    ax.set_ylabel("Probability of winning ≥ 1 object", fontsize=16)

    # Ejes
    ax.set_ylim(0, 1)
    ax.spines['bottom'].set_position(('data', 0))
    ax.spines['left'].set_position(('data', 0))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend()
    plt.tight_layout()
    plt.show()


def expected_profit_k_ght_max_valuation_by_position_multiple(n:int, m:int, d_values:list, sims:int, k:int):
    """
    Estima el beneficio esperado del licitador con la k‑ésima mayor valoración
    condicionado a su posición de llegada en una subasta múltiple eBay Proxy Bidding.

    Para cada valor del incremento mínimo de puja `d` en `d_values`, se realizan
    sims` simulaciones independientes. En cada simulación:

        1. Se genera un orden de llegada aleatorio para los n compradores,
            cada uno con valoración independiente ~ U(0,1).
        2. Se identifica al comprador con la k‑ésima mayor valoración dentro
            de ese orden.
        3. Se evalúa su beneficio en tres escenarios de llegada:
                * first  — el comprador objetivo se coloca en la primera posición.
                * random — se coloca en una posición aleatoria.
                * last   — se coloca en la última posición.

            Para cada escenario:
                - Se reordena la lista de compradores según la regla.
                - Se resetea el estado interno de cada comprador (active_object = None).
                - Se generan parámetros heterogéneos para los m objetos:
                        reserve_j   = 0 + N(0, sigma_reserve)
                        increment_j = d + N(0, sigma_increment)
                - Se ejecuta la subasta múltiple mediante ebay_proxy_bidding_multiple().
                - Se identifican los objetos ganados por el comprador objetivo.
                - El beneficio se calcula como: beneficio = valoración − suma de precios pagados
                  siendo cero si no gana ningún objeto.

    Finalmente, para cada valor de `d`, la función devuelve el beneficio esperado
    del comprador objetivo en cada uno de los tres escenarios de llegada.

    Args:
        n (int): Número total de compradores.
        m (int): Número total de objetos en subasta.
        d_values (list[float]): Valores del incremento mínimo de puja a evaluar.
        sims (int): Número de simulaciones por cada valor de d.
        k (int): Orden estadístico de la valoración (1 = mayor valoración).

        Returns:
            dict:
                Diccionario con claves "first", "random" y "last".
                Cada clave contiene una lista con el beneficio esperado para cada
                valor de d en d_values.
        """

    if k < 1 or k > n:
        raise ValueError("k debe estar entre 1 y n")
    # Auxiliar: índice del k-ésimo mayor
    def get_kth_index(vals, k):
        idx_sorted = np.argsort(vals)
        return idx_sorted[-k]
    results = {"first": [], "random": [], "last": []}
    for d in d_values:
        profits = {"first": [], "random": [], "last": []}
        for _ in range(sims):
            # Orden de llegada multiobjeto
            order = multiple_arrival_order(n)
            vals = np.array([buyer.valoracion for buyer in order])
            # Identificar al licitador objetivo
            idx_target = get_kth_index(vals, k)
            bidder_target = order[idx_target]
            # Parámetros heterogéneos para los m objetos (s = 0)
            reserve_prices, min_increments = generar_parametros(m, reserv_base=0, increment_base=d,
                                                                sigma_reserve=0.05, sigma_increment=0.002)

            # CASO 1: Llega primero
            order_first = np.array(order, dtype=object)
            order_first[[0, idx_target]] = order_first[[idx_target, 0]]
            for b in order_first:
                b.active_object = None
            objetos = ebay_proxy_bidding_multiple(n, m, reserve_prices, min_increments, biders = order_first)

            # Objetos ganados por el target
            precios_ganados = [obj.current_price for obj in objetos
                if obj.highest_bidder is not None and obj.highest_bidder.ID == bidder_target.ID]

            beneficio = bidder_target.valoracion - sum(precios_ganados) if precios_ganados else 0
            profits["first"].append(beneficio)

            # CASO 2: Llega aleatorio
            order_random = np.array(order, dtype=object)
            pos_random = np.random.randint(0, n)
            for b in order_random:
                b.active_object = None
            order_random[[pos_random, idx_target]] = order_random[[idx_target, pos_random]]
            objetos = ebay_proxy_bidding_multiple(n, m, reserve_prices, min_increments, biders = order_random)
            precios_ganados = [obj.current_price for obj in objetos
                if obj.highest_bidder is not None and obj.highest_bidder.ID == bidder_target.ID]

            beneficio = bidder_target.valoracion - sum(precios_ganados) if precios_ganados else 0
            profits["random"].append(beneficio)

            # CASO 3: Llega último
            order_last = np.array(order, dtype=object)
            order_last[[n - 1, idx_target]] = order_last[[idx_target, n - 1]]
            for b in order_last:
                b.active_object = None
            objetos = ebay_proxy_bidding_multiple(n, m, reserve_prices, min_increments, biders = order_last)
            precios_ganados = [obj.current_price for obj in objetos
                if obj.highest_bidder is not None and obj.highest_bidder.ID == bidder_target.ID]
            beneficio = bidder_target.valoracion - sum(precios_ganados) if precios_ganados else 0
            profits["last"].append(beneficio)

        # Guardamos beneficios esperados
        for key in results:
            results[key].append(np.mean(profits[key]))

    return results



def plot_expected_profits_multiple(d_values, results, k, m):
    """
    Grafica los beneficios esperados para cada regla de llegada según
    expected_profit_k_ght_max_valuation_by_position_multiple().

    """

    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size'] = 14
    fig, ax = plt.subplots(figsize=(10, 6))
    x = d_values  # eje X = valores de d
    for key in results:
        ax.plot(x, results[key], marker='o', linewidth=2, label=key)
        ax.text(x[-1],results[key][-1],key,fontsize=14,ha='left',va='bottom')

    # Título adaptado al caso multiobjeto
    ax.set_title(f"Figura 9({'b' if k == 1 else 'd'}) — Expected profit (k={k}, m={m})",
                 fontsize=18)
    ax.set_xlabel("Minimum bid increment d", fontsize=16)
    ax.set_ylabel("Expected profit (sum of profits over objects)", fontsize=16)
    # Ejes
    ax.set_ylim(0, 0.3)
    ax.spines['bottom'].set_position(('data', 0))
    ax.spines['left'].set_position(('data', 0))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend()
    plt.tight_layout()
    plt.show()

    # Título adaptado al caso multiobjeto
    ax.set_title(f"Figura 9({ 'a' if k==1 else 'c' }) — Probability of winning ≥1 object (k={k}, m={m})",
        fontsize=18)

    ax.set_xlabel("Minimum bid increment d", fontsize=16)
    ax.set_ylabel("Probability of winning ≥ 1 object", fontsize=16)

