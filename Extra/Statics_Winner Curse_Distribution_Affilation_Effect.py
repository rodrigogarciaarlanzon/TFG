from Simulation.Multiple_Affiliated import general_parameters,expected_profit_k_phi_max_valuation_by_position_multiple, compare_models, plot_model_comparison
from eBay.Multiple_Affiliated_Proxy_Bidding import ebay_affiliated_bidding_multiple, multiple_affiliated_arrival_order
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# ANÁLISIS DE WINNER'S CURSE.

#!!!!!!!!!!!!!!!!!!!!!!!!CONSIDERAR EL CASO TAMBIÉN PARA AFFILIATED VALUES

def analyze_winners_curse(n, m, sims, alpha=0.05):
    """
    Analiza la maldición del ganador comparando modelos common_value vs independent.

    La maldición del ganador ocurre cuando, en un entorno de valor común, el ganador
    tiende a pagar más que el valor real del objeto porque tiene una señal optimista.

    Args:
        n (int): Número de postores en cada subasta
        m (int): Número de objetos en subasta
        sims (int): Número de simulaciones por valor de d
        alpha (float): Nivel de significancia para tests estadísticos (default: 0.05)

    Returns:
        dict: Diccionario con:
            - d_values: Lista de incrementos mínimos evaluados
            - profits_common: Beneficios promedio para modelo common_value
            - profits_ipv: Beneficios promedio para modelo IPV
            - overpayment: Sobrepago estimado (diferencia de beneficios)
            - t_tests: Resultados de tests t para cada d
            - effect_sizes: Tamaños del efecto (Cohen's d) para cada d


    """

    d_values = [0, 0.05, 0.1, 0.15, 0.2]
    print("=" * 70)
    print("ANÁLISIS ESTADÍSTICO DE WINNER'S CURSE")
    print("=" * 70)
    print(f"Configuración: N={n} postores, M={m} objetos, {sims} simulaciones")
    print(f"Nivel de significancia: α={alpha}")

    # Inicializar estructura de resultados
    analysis_results = {
        'd_values': d_values,
        'profits_common': {'first': [], 'random': [], 'last': []},
        'profits_ipv': {'first': [], 'random': [], 'last': []},
        'overpayment': {},
        't_tests': [],  # Resultados de tests estadísticos
        'effect_sizes': [],  # Tamaños del efecto
        'confidence_intervals': []  # Intervalos de confianza
    }

    print("\nComparando beneficios del mejor postor (k=1) entre modelos...")

    # Para cada valor de d, realizar análisis estadístico
    for i, d in enumerate(d_values):
        print(f"\n{'─' * 40}")
        print(f"ANÁLISIS PARA d = {d:.2f}")
        print(f"{'─' * 40}")

        # Obtener beneficios usando función existente
        profits_common = expected_profit_k_phi_max_valuation_by_position_multiple(
            n, m, [d], sims, k=1, valuation_method="common_value")

        profits_ipv = expected_profit_k_phi_max_valuation_by_position_multiple(
            n, m, [d], sims, k=1, valuation_method="independent")

        # Guardar beneficios promedio (posición 'first' como referencia)
        analysis_results['profits_common']['first'].append(profits_common['first'][0])
        analysis_results['profits_ipv']['first'].append(profits_ipv['first'][0])

        # Calcular sobrepago estimado (Winner's Curse)
        overpayment = profits_ipv['first'][0] - profits_common['first'][0]
        analysis_results['overpayment'][d] = overpayment

        # Obtener datos brutos para análisis estadístico
        print("Recolectando datos brutos para análisis estadístico...")
        profits_common_raw = _get_raw_profits_for_wc_analysis(n, m, d, sims, "common_value", k=1)
        profits_ipv_raw = _get_raw_profits_for_wc_analysis(n, m, d, sims, "independent", k=1)

        # Realizar test t de dos muestras independientes
        # H0: No hay diferencia (μ_common = μ_ipv)
        # H1: Hay Winner's Curse (μ_common < μ_ipv) → one-tailed test
        t_stat, p_value = stats.ttest_ind(profits_ipv_raw,profits_common_raw,
            equal_var=False,  # Welch's t-test (no asume varianzas iguales)
            alternative='greater')  # Test de una cola: ipv > common

        # Calcular tamaño del efecto (Cohen's d)
        n1, n2 = len(profits_ipv_raw), len(profits_common_raw)
        pooled_std = np.sqrt(
            ((n1 - 1) * np.var(profits_ipv_raw) + (n2 - 1) * np.var(profits_common_raw)) / (n1 + n2 - 2))
        cohens_d = (np.mean(profits_ipv_raw) - np.mean(profits_common_raw)) / pooled_std if pooled_std > 0 else 0

        # Calcular intervalo de confianza 95% para la diferencia de medias
        mean_diff = np.mean(profits_ipv_raw) - np.mean(profits_common_raw)
        se_diff = np.sqrt(np.var(profits_ipv_raw) / n1 + np.var(profits_common_raw) / n2)
        ci_lower = mean_diff - 1.96 * se_diff
        ci_upper = mean_diff + 1.96 * se_diff

        # Determinar significancia estadística
        significant = p_value < alpha

        # Guardar resultados del test
        test_result = {
            'd': d,
            't_statistic': t_stat,
            'p_value': p_value,
            'significant': significant,
            'mean_common': np.mean(profits_common_raw),
            'mean_ipv': np.mean(profits_ipv_raw),
            'std_common': np.std(profits_common_raw),
            'std_ipv': np.std(profits_ipv_raw),
            'n_common': n2,
            'n_ipv': n1
        }

        analysis_results['t_tests'].append(test_result)

        # Guardar tamaño del efecto
        effect_size = {
            'd': d,
            'cohens_d': cohens_d,
            'interpretation': _interpret_cohens_d(cohens_d),
            'mean_difference': mean_diff,
            'ci_lower': ci_lower,
            'ci_upper': ci_upper
        }

        analysis_results['effect_sizes'].append(effect_size)
        analysis_results['confidence_intervals'].append((ci_lower, ci_upper))

        # Mostrar resultados
        print(
            f"  Beneficio promedio Common Value: {np.mean(profits_common_raw):.4f} ± {np.std(profits_common_raw):.4f}")
        print(f"  Beneficio promedio IPV: {np.mean(profits_ipv_raw):.4f} ± {np.std(profits_ipv_raw):.4f}")
        print(f"  Diferencia estimada: {mean_diff:.4f} [IC95%: {ci_lower:.4f}, {ci_upper:.4f}]")
        print(f"  Test t de Welch: t({n1 + n2 - 2:.0f}) = {t_stat:.3f}, p = {p_value:.4f}")
        print(f"  Tamaño del efecto (Cohen's d): {cohens_d:.3f} ({effect_size['interpretation']})")
        print(f"  ¿Winner\'s Curse significativo (p < {alpha})?: {'SÍ' if significant else 'NO'}")

        # Advertencia sobre potencia estadística
        if not significant and len(profits_common_raw) < 30:
            print(f" Potencia estadística limitada (n={len(profits_common_raw)})")




    return analysis_results


def _get_raw_profits_for_wc_analysis(n, m, d, sims, valuation_method, k=1):
    """
    Obtiene beneficios brutos para análisis estadístico de Winner's Curse.

    Args:
        n (int): Número de postores
        m (int): Número de objetos
        d (float): Incremento mínimo
        sims (int): Número de simulaciones
        valuation_method (str): Mét0do de valoración
        k (int): k-ésimo mayor valorador (1 = mejor)

    Returns:
        list: Lista de beneficios brutos
    """
    profits = []

    for _ in range(sims):
        # Crear orden de llegada
        order = multiple_affiliated_arrival_order(n, m, valuation_method=valuation_method)

        # Obtener valoraciones para identificar k-ésimo mayor
        vals = np.array([buyer.original_valuations.mean()
                         if hasattr(buyer, 'original_valuations')
                         else np.mean([buyer.get_valuation_for_object(i + 1)
                                       for i in range(m)])
                         for buyer in order])

        # Identificar k-ésimo mayor
        idx_sorted = np.argsort(vals)
        idx_target = idx_sorted[-k]
        bidder_target = order[idx_target]

        # Generar parámetros de subasta
        reserve_prices, min_increments = general_parameters(m, reserv_base=0, increment_base=d)

        # Posición aleatoria (para evitar bias de posición)
        pos_random = np.random.randint(0, n)
        order_modified = np.array(order, dtype=object)
        order_modified[[pos_random, idx_target]] = order_modified[[idx_target, pos_random]]

        # Resetear estado de compradores
        for b in order_modified:
            b.active_object = None

        # Ejecutar subasta
        objetos = ebay_affiliated_bidding_multiple(n, m, reserve_prices, min_increments,
            biders=order_modified,valuation_method=valuation_method)

        # Calcular beneficio del comprador objetivo
        precios_ganados = [obj.current_price for obj in objetos if obj.highest_bidder is not None
                           and obj.highest_bidder.ID == bidder_target.ID]

        beneficio = bidder_target.original_valuations.mean() - sum(precios_ganados) \
            if precios_ganados else 0

        profits.append(beneficio)

    return profits


def _interpret_cohens_d(d):
    """
    Interpreta el tamaño del efecto de Cohen's d según convenciones estándar.

    Args:
        d (float): Valor de Cohen's d

    Returns:
        str: Interpretación cualitativa
    """
    if abs(d) < 0.2:
        return "efecto trivial"
    elif abs(d) < 0.5:
        return "efecto pequeño"
    elif abs(d) < 0.8:
        return "efecto moderado"
    else:
        return "efecto grande"




def ejemplo_1_comparacion_rapida():
    """Comparación rápida con pocas simulaciones."""
    print("Ejemplo 1: Comparación rápida de modelos")
    resultados = compare_models(n=10, m=3, max_min_increment=0.2, sims=50)
    return resultados


def ejemplo_2_winners_curse_basico():
    """Análisis básico de Winner's Curse."""
    print("Ejemplo 2: Winner's Curse básico")
    resultados = analyze_winners_curse(n=15, m=4, sims=100, alpha=0.05)
    return resultados



def ejemplo_4_correr_todo():
    """Ejecuta todos los ejemplos."""
    print("=" * 60)
    print("EJECUTANDO TODOS LOS EJEMPLOS")
    print("=" * 60)

    print("\n1. Comparación rápida...")
    res1 = ejemplo_1_comparacion_rapida()

    print("\n2. Winner's Curse básico...")
    res2 = ejemplo_2_winners_curse_basico()


    print("\n✓ Todos los ejemplos completados")
    return res1, res2


#Ejecutar código:
if __name__ == "__main__":
    ejemplo_4_correr_todo()