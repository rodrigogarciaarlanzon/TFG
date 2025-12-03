import numpy as np
import matplotlib.pyplot as plt
from eBay.Multiple_Proxy_Bidding import ebay_proxy_bidding_multiple


# Generador de parámetros. Dado un precio de reserva y un incremento mínimo de puja, en el resto de pujas vendrán determinados por un incremento delta
def generar_parametros(m, reserve_base, increment_base, delta_reserve=0.01, delta_increment=0.005):
    reserve_prices = [reserve_base + j * delta_reserve for j in range(m)]
    min_increments = [increment_base + j * delta_increment for j in range(m)]
    return reserve_prices, min_increments

# Simulación variando el precio de reserva "base"
def sim_reserv_multi(n, m, reserve_bases, increment_base, delta_reserve, delta_increment, simulations=1000):
    results = []
    for r in reserve_bases:
        prices = []
        for _ in range(simulations):
            reserve_prices, min_increments = generar_parametros(m, r, increment_base, delta_reserve, delta_increment)
            objetos = ebay_proxy_bidding_multiple(n, m, reserve_prices, min_increments)
            precios_finales = [obj.current_price for obj in objetos if obj.highest_bidder is not None]
            if precios_finales:
                prices.append(np.mean(precios_finales))
        results.append(np.mean(prices) if prices else 0)
    return results

# Simulación variando el incremento mínimo "base"
def sim_increment_multi(n, m, reserve_base, increment_bases, delta_reserve, delta_increment, simulations=1000):
    results = []
    for inc in increment_bases:
        prices = []
        for _ in range(simulations):
            reserve_prices, min_increments = generar_parametros(m, reserve_base, inc, delta_reserve, delta_increment)
            objetos = ebay_proxy_bidding_multiple(n, m, reserve_prices, min_increments)
            precios_finales = [obj.current_price for obj in objetos if obj.highest_bidder is not None]
            if precios_finales:
                prices.append(np.mean(precios_finales))
        results.append(np.mean(prices) if prices else 0)
    return results

# Ejecutar simulaciones y graficos. Se obtiene en eje vertical un precio medio de venta de todos los objetos en puja (haciendo asimismo la media entre todas las simulaciones).
def ejecutar_simulaciones_multi(n, m):
    Reserv_base = np.linspace(0, 0.5, 20)       # rango de bases de reserva
    Increment_base = np.linspace(0, 0.2, 20)    # rango de bases de incremento mínimo

    results_reserv = sim_reserv_multi(n, m, Reserv_base, increment_base=0.05,
                                      delta_reserve=0.01, delta_increment=0.005)
    results_increment = sim_increment_multi(n, m, reserve_base=0.2, increment_bases=Increment_base,
                                            delta_reserve=0.01, delta_increment=0.005)

    # Gráficos
    plt.figure(figsize=(12,5))

    plt.subplot(1,2,1)
    plt.plot(Reserv_base, results_reserv, marker='o')
    plt.title(f"Precio medio de venta vs Precio reserva (m={m})")
    plt.xlabel("Precio reserva")
    plt.ylabel("Precio medio venta")

    plt.subplot(1,2,2)
    plt.plot(Increment_base, results_increment, marker='o', color='orange')
    plt.title(f"Precio medio de venta vs Incremento mínimo (m={m})")
    plt.xlabel("Incremento mínimo")
    plt.ylabel("Precio medio de venta")

    plt.tight_layout()
    plt.show()

