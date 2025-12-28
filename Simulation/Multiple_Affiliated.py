import numpy as np
import matplotlib.pyplot as plt
from eBay.Multiple_Affiliated_Proxy_Bidding import (ebay_affiliated_bidding_multiple,multiple_affiliated_arrival_order)


def general_parameters(m: int, reserv_base: float, increment_base: float,
                       sigma_reserve=0.05, sigma_increment=0.002):
    """
    Idéntica al caso eBay múltiple. Genera parámetros heterogéneos para m objetos.
    """
    reserve_price = [reserv_base]
    min_increment = [increment_base]

    for j in range(m - 1):
        s_j = reserv_base + np.random.normal(0, sigma_reserve)
        s_j = max(0.0, s_j)
        d_j = increment_base + np.random.normal(0, sigma_increment)
        d_j = max(1e-4, d_j)
        reserve_price.append(s_j)
        min_increment.append(d_j)

    return reserve_price, min_increment


def sim_reserve_multiple(n: int, m: int, reserve_price_list: list,min_increment: float, simulations: int,
                         valuation_method,sigma_reserve: float = 0.05,sigma_increment: float = 0.002):
    """
    Versión afiliada de la función sim_reserve_multiple para eBay múltiple.
    """
    results = []
    bids = []
    for s in reserve_price_list:
        all_prices = []
        all_buyers_counts = []
        for _ in range(simulations):
            # Generar parámetros
            reserve_list, incr_list = general_parameters(m, reserv_base=s, increment_base=min_increment,
                sigma_reserve=sigma_reserve, sigma_increment=sigma_increment)
            # Ejecutar subasta afiliada
            objetos = ebay_affiliated_bidding_multiple(n, m, reserve_list, incr_list,valuation_method=valuation_method)

            # Recoger resultados
            for obj in objetos:
                if obj.highest_bidder is not None:
                    all_prices.append(obj.current_price)
                    all_buyers_counts.append(obj.buyers_count)

        avg_price = np.mean(all_prices) if all_prices else 0.0
        avg_buyers = np.mean(all_buyers_counts) if all_buyers_counts else 0.0

        results.append(avg_price)
        bids.append(avg_buyers)

    return results, bids


def sim_increment_multiple(n: int, m: int, reserve_price: float,min_increment_list: list, simulations: int,
                           valuation_method,sigma_reserve: float = 0.05,sigma_increment: float = 0.002):
    """
    Versión afiliada de la función sim_increment_multiple para eBay múltiple..
    """
    results = []
    bids = []
    for d in min_increment_list:
        all_prices = []
        all_buyers_counts = []

        for _ in range(simulations):
            # Generar parámetros
            reserve_list, incr_list = general_parameters(m, reserv_base=reserve_price, increment_base=d,
                sigma_reserve=sigma_reserve, sigma_increment=sigma_increment)

            # Ejecutar subasta afiliada
            objetos = ebay_affiliated_bidding_multiple(n, m, reserve_list, incr_list,valuation_method=valuation_method)

            # Recoger resultados
            for obj in objetos:
                if obj.highest_bidder is not None:
                    all_prices.append(obj.current_price)
                    all_buyers_counts.append(obj.buyers_count)

        avg_price = np.mean(all_prices) if all_prices else 0.0
        avg_buyers = np.mean(all_buyers_counts) if all_buyers_counts else 0.0

        results.append(avg_price)
        bids.append(avg_buyers)

    return results, bids


def comparacion_simulaciones_multiple(n: int, m: int, max_min_increment: int,
                                      sims: int, valuation_method):
    """
    Versión afiliada de la función comparacion_simulaciones_multiple para eBay múltiple.
    """
    Min_increment = np.linspace(0, max_min_increment, 20)

    results_increment, bids = sim_increment_multiple(n=n, m=m, reserve_price=0,min_increment_list=Min_increment,
        simulations=sims,valuation_method=valuation_method)

    return Min_increment, results_increment, bids


def sim_bids_fixed_d_multiple(n: int, m: int, reserve_price: float,
                              d: float, simulations: int,
                              valuation_method,
                              sigma_reserve=0.05, sigma_increment=0.002):
    """
    Versión afiliada de la función sim_bids_fixed_d_multiple para eBay múltiple.
    """
    all_buyers_counts = []

    for _ in range(simulations):
        # Generar parámetros heterogéneos
        reserve_list, incr_list = general_parameters(m, reserv_base=reserve_price, increment_base=d,
            sigma_reserve=sigma_reserve, sigma_increment=sigma_increment)

        # Ejecutar subasta afiliada
        objetos = ebay_affiliated_bidding_multiple(n, m, reserve_list, incr_list,valuation_method=valuation_method)

        # Recoger número de pujadores por objeto
        for obj in objetos:
            if obj.highest_bidder is not None:
                all_buyers_counts.append(obj.buyers_count)

    return np.mean(all_buyers_counts) if all_buyers_counts else 0.0


def prob_win_order_multiple(n: int, m: int, d_values: list, sims: int,
                            valuation_method):
    """
    Versión afiliada de la función prob_win_order_multiple para eBay múltiple.
    """
    resultados = {d: np.zeros(n) for d in d_values}

    for d in d_values:
        print(f"\nSimulando d = {d}")
        for k in range(n):
            wins = 0
            for sim in range(sims):
                # Generar orden de llegada afiliado
                order = multiple_affiliated_arrival_order(n, m, valuation_method=valuation_method)

                # Generar parámetros
                reserve_prices, min_increments = general_parameters(m, reserv_base=0, increment_base=d,
                    sigma_reserve=0.05, sigma_increment=0.002)

                # Subasta afiliada
                objetos = ebay_affiliated_bidding_multiple(n, m, reserve_prices, min_increments,biders=order,valuation_method=valuation_method)

                # Lista de ganadores
                winners_ids = [obj.highest_bidder.ID for obj in objetos if obj.highest_bidder is not None]

                # Postor en posición k
                postor_k = order[k]

                # ¿Ganó un objeto?
                if postor_k.ID in winners_ids:
                    wins += 1

            resultados[d][k] = wins / sims

    return resultados


def prob_kth_max_val_wins_by_position_multiple(n: int, m: int, d_values: list,sims: int, k: int,valuation_method):
    """
    Versión afiliada de la función prob_kth_max_val_wins_by_position_multiple para eBay múltiple.
    """
    if k < 1 or k > n:
        raise ValueError("k debe estar entre 1 y n")

    # Función auxiliar para obtener índice k-ésimo mayor
    def get_kth_index(vals, k):
        idx_sorted = np.argsort(vals)
        return idx_sorted[-k]

    results = {"first": [], "random": [], "last": []}

    for d in d_values:
        wins = {"first": 0, "random": 0, "last": 0}
        for _ in range(sims):
            # Orden de llegada afiliado
            order = multiple_affiliated_arrival_order(n, m, valuation_method=valuation_method)

            # Obtener valoraciones base
            vals = np.array([buyer.original_valuations.mean()
                             if hasattr(buyer, 'original_valuations')
                             else np.mean([buyer.get_valuation_for_object(i + 1)
                                           for i in range(m)])
                             for buyer in order])

            # Identificar licitador objetivo
            idx_target = get_kth_index(vals, k)
            bidder_target = order[idx_target]

            # Generar parámetros
            reserve_prices, min_increments = general_parameters(m, reserv_base=0, increment_base=d)

            # CASO 1: Llega primero
            order_first = np.array(order, dtype=object)
            order_first[[0, idx_target]] = order_first[[idx_target, 0]]
            for b in order_first:
                b.active_object = None
            objetos = ebay_affiliated_bidding_multiple(n, m, reserve_prices, min_increments,biders=order_first,
                valuation_method=valuation_method)

            winners_ids = [obj.highest_bidder.ID for obj in objetos if obj.highest_bidder is not None]

            if bidder_target.ID in winners_ids:
                wins["first"] += 1

            # CASO 2: Llega aleatorio
            order_random = np.array(order, dtype=object)
            pos_random = np.random.randint(0, n)
            order_random[[pos_random, idx_target]] = order_random[[idx_target, pos_random]]

            for b in order_random:
                b.active_object = None
            objetos = ebay_affiliated_bidding_multiple(n, m, reserve_prices, min_increments,
                biders=order_random,valuation_method=valuation_method)

            winners_ids = [obj.highest_bidder.ID for obj in objetos if obj.highest_bidder is not None]

            if bidder_target.ID in winners_ids:
                wins["random"] += 1

            # CASO 3: Llega último
            order_last = np.array(order, dtype=object)
            order_last[[n - 1, idx_target]] = order_last[[idx_target, n - 1]]
            for b in order_last:
                b.active_object = None

            objetos = ebay_affiliated_bidding_multiple(n, m, reserve_prices, min_increments,
                biders=order_last,valuation_method=valuation_method)

            winners_ids = [obj.highest_bidder.ID for obj in objetos if obj.highest_bidder is not None]

            if bidder_target.ID in winners_ids:
                wins["last"] += 1

        # Guardar probabilidades
        for key in results:
            results[key].append(wins[key] / sims)

    return results


def expected_profit_k_phi_max_valuation_by_position_multiple(n: int, m: int,
                                                             d_values: list,
                                                             sims: int, k: int,
                                                             valuation_method):
    """
    Versión afiliada de la función expected_profit_k_phi_max_valuation_by_position_multiple para eBay múltiple.
    """
    if k < 1 or k > n:
        raise ValueError("k debe estar entre 1 y n")

    def get_kth_index(vals, k):
        idx_sorted = np.argsort(vals)
        return idx_sorted[-k]

    results = {"first": [], "random": [], "last": []}
    for d in d_values:
        profits = {"first": [], "random": [], "last": []}
        for _ in range(sims):
            # Orden de llegada afiliado
            order = multiple_affiliated_arrival_order(n, m, valuation_method=valuation_method)
            # Obtener valoraciones base
            vals = np.array([buyer.original_valuations.mean()
                             if hasattr(buyer, 'original_valuations')
                             else np.mean([buyer.get_valuation_for_object(i + 1)
                                           for i in range(m)])
                             for buyer in order])
            # Identificar licitador objetivo
            idx_target = get_kth_index(vals, k)
            bidder_target = order[idx_target]

            # Generar parámetros
            reserve_prices, min_increments = general_parameters(m, reserv_base=0, increment_base=d)

            # CASO 1: Llega primero
            order_first = np.array(order, dtype=object)
            order_first[[0, idx_target]] = order_first[[idx_target, 0]]
            for b in order_first:
                b.active_object = None
            objetos = ebay_affiliated_bidding_multiple(n, m, reserve_prices, min_increments,
                biders=order_first,valuation_method=valuation_method)

            # Calcular beneficio
            precios_ganados = [obj.current_price for obj in objetos
                               if obj.highest_bidder is not None
                               and obj.highest_bidder.ID == bidder_target.ID]

            beneficio = bidder_target.original_valuations.mean() - sum(precios_ganados) \
                if precios_ganados else 0
            profits["first"].append(beneficio)

            # CASO 2: Llega aleatorio
            order_random = np.array(order, dtype=object)
            pos_random = np.random.randint(0, n)
            order_random[[pos_random, idx_target]] = order_random[[idx_target, pos_random]]
            for b in order_random:
                b.active_object = None
            objetos = ebay_affiliated_bidding_multiple(n, m, reserve_prices, min_increments,
                biders=order_random,valuation_method=valuation_method)

            precios_ganados = [obj.current_price for obj in objetos if obj.highest_bidder is not None
                               and obj.highest_bidder.ID == bidder_target.ID]

            beneficio = bidder_target.original_valuations.mean() - sum(precios_ganados) \
                if precios_ganados else 0
            profits["random"].append(beneficio)

            # CASO 3: Llega último
            order_last = np.array(order, dtype=object)
            order_last[[n - 1, idx_target]] = order_last[[idx_target, n - 1]]
            for b in order_last:
                b.active_object = None
            objetos = ebay_affiliated_bidding_multiple(n, m, reserve_prices, min_increments,
                biders=order_last,valuation_method=valuation_method)

            precios_ganados = [obj.current_price for obj in objetos if obj.highest_bidder is not None
                               and obj.highest_bidder.ID == bidder_target.ID]

            beneficio = bidder_target.original_valuations.mean() - sum(precios_ganados) \
                if precios_ganados else 0
            profits["last"].append(beneficio)

        # Guardar beneficios esperados
        for key in results:
            results[key].append(np.mean(profits[key]))

    return results



def plot_probabilities_multiple(d_values, results, k, m):
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size'] = 14

    fig, ax = plt.subplots(figsize=(10, 6))
    x = d_values

    for key in results:
        ax.plot(x, results[key], marker='o', linewidth=2, label=key)
        ax.text(x[-1], results[key][-1], key, fontsize=14, ha='left', va='bottom')

    ax.set_title(f"Figura 9({'a' if k == 1 else 'c'}) – Probability of winning (k={k}, m={m})",
                 fontsize=18)
    ax.set_xlabel("Minimum bid increment d", fontsize=16)
    ax.set_ylabel("Probability of winning ≥ 1 object", fontsize=16)

    ax.set_ylim(0, 1)
    ax.spines['bottom'].set_position(('data', 0))
    ax.spines['left'].set_position(('data', 0))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend()

    plt.tight_layout()
    plt.show()


def plot_expected_profits_multiple(d_values, results, k, m):
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size'] = 14

    fig, ax = plt.subplots(figsize=(10, 6))
    x = d_values

    for key in results:
        ax.plot(x, results[key], marker='o', linewidth=2, label=key)
        ax.text(x[-1], results[key][-1], key, fontsize=14, ha='left', va='bottom')

    ax.set_title(f"Figura 9({'b' if k == 1 else 'd'}) - Expected profit (k={k}, m={m})",
                 fontsize=18)
    ax.set_xlabel("Minimum bid increment d", fontsize=16)
    ax.set_ylabel("Expected profit (sum of profits over objects)", fontsize=16)

    ax.set_ylim(0, 0.3)
    ax.spines['bottom'].set_position(('data', 0))
    ax.spines['left'].set_position(('data', 0))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend()

    plt.tight_layout()
    plt.show()


# FUNCIÓN DE COMPARACIÓN ENTRE MODELOS

def compare_models(n: int, m: int, max_min_increment: float, sims: int = 100):
    """
    Compara resultados entre modelo IPV y modelos afiliados.

    Returns:
        Diccionario con resultados para cada modelo
    """
    models = {"IPV": "independent","Common Value": "common_value","Correlated Private": "correlated_private"}

    results = {}

    for model_name, valuation_method in models.items():
        print(f"\nSimulando modelo: {model_name}")

        Min_increment, revenues, bids = comparacion_simulaciones_multiple(n=n, m=m, max_min_increment=max_min_increment,
            sims=sims, valuation_method=valuation_method)

        results[model_name] = {"d_values": Min_increment,"revenues": revenues,"bids": bids}

    return results


def plot_model_comparison(results):
    """
    Grafica comparación entre modelos.
    """
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size'] = 14
    fig, ax = plt.subplots(figsize=(10, 6))
    #colors = {'IPV': 'blue', 'Common Value': 'orange', 'Correlated Private': 'green'}
    for model_name, data in results.items():
        ax.plot(data["d_values"], data["revenues"],
                marker='o',
                label=model_name)
    ax.set_title("Model Comparison: Expected Revenue per Object", fontsize=18)
    ax.set_xlabel("Minimum bid increment d", fontsize=16)
    ax.set_ylabel("Expected auction revenue per object", fontsize=16)
    ax.set_ylim(0, 1.0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend()
    plt.tight_layout()
    plt.show()