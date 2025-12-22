import numpy as np
import matplotlib.pyplot as plt
from eBay.Proxy_Bidding import ebay_proxy_bidding

# Simulación. Array con la evolución de la media de precios de venta del objeto subastado dependeinte del precio de reserva
def sim_reserv(n, reserve_price: list, min_increment, simulations=500000):
    results = []
    for r in reserve_price:
        prices = []
        for sim in range(simulations):
            winner, price = ebay_proxy_bidding(n, r, min_increment)
            if price is not None:
                prices.append(price)
        results.append(np.mean(prices) if prices else 0)
    return results

# Simulación. Array con la evolución de la media de precios de venta del objeto subastado dependeinte del incremento mínimo de puja
def sim_increment(n, reserve_price, min_increment: list, simulations=1000):
    results = []
    for inc in min_increment:
        prices = []
        for sim in range(simulations):
            winner, price = ebay_proxy_bidding(n, reserve_price, inc)
            if price is not None:
                prices.append(price)
        results.append(np.mean(prices) if prices else 0)
    return results

#Establecemos de forma determinista el dominio del precio de reserva y el incremneto mínimo de puja bajo la condición asumida por los autores s + 2d < V
def ejecutar_simulaciones(n, max_min_increment):
    #Reserv_price = np.linspace(0, 1, 20)          rango de precios de reserva
    Reserv_price = 0 #En el trabajo de Rogers, toman s = 0
    Min_increment = np.linspace(0, max_min_increment, 20)     # rango de incrementos mínimos

    # results_reserv = sim_reserv(n, Reserv_price, min_increment=0.05) #determinamos el incremento mínimo de puja
    results_increment = sim_increment(n, min_increment=Min_increment, reserve_price= 0)

    # Gráficos. Obtendremos dos gráficos que mostrarán la evolución del precio medio de venta según los valores de la variable enfrentada en estudio
    plt.figure(figsize=(12,5))

    #plt.subplot(1,2,1)
    #plt.plot(Reserv_price, results_reserv, marker='o')
    #plt.title("Precio medio venta vs Precio de reserva")
    #plt.xlabel("Precio de reserva")
    #plt.ylabel("Precio medio venta")

    plt.subplot(1,2,2)
    plt.plot(Min_increment, results_increment, marker='o', color='orange')
    plt.title("Precio medio venta vs Incremento mínimo")
    plt.xlabel("Incremento mínimo")
    plt.ylabel("Precio medio venta")

    plt.tight_layout()
    plt.show()

