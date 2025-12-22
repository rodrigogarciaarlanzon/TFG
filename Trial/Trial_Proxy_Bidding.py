import matplotlib.pyplot as plt
from Simulation.Proxy_Bidding_Simulation import comparacion_simulaciones
from  Simulation.Proxy_Bidding_Simulation import ejecutar_simulaciones

"""
Primer caso en el estudio de Rogers. N = 2 postores. 500.000 simulaciones. Precio de reserva = 0. Rango incremento mínimo de puja np.linspace(0, 0.5, 20)  
ejecutar_simulaciones(2, 0.5)
"""

"""
Segundo caso en el estudio de Rogers. N = 20 postores. 500.000 simulaciones. Precio de reserva = 0. Rango incremento mínimo de puja np.linspace(0, 0.5, 20)  
ejecutar_simulaciones(20, 0.2)
"""

"""
Tercer caso, comparación resultados para N = 10, N = 20, N = 40


# Ejecutamos las simulaciones para distintos n
x10, y10 = comparacion_simulaciones(10, 0.2)
x20, y20 = comparacion_simulaciones(20, 0.2)
x40, y40 = comparacion_simulaciones(40, 0.2)

# Gráfico comparativo
plt.figure(figsize=(10,6))

plt.plot(x10, y10, marker='o', label='n = 10')
plt.plot(x20, y20, marker='o', label='n = 20')
plt.plot(x40, y40, marker='o', label='n = 40')

plt.title("Comparación del precio medio de venta según n")
plt.xlabel("Incremento mínimo")
plt.ylabel("Precio medio de venta")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
"""


"Cuarto caso. Aproximación logarítmica del número de pujas registradas"


# Parámetros
N_values = list(range(1, 41))  # De 0 a 40
d_values = [0.01, 0.025, 0.05, 0.075, 0.1]  # Incrementos mínimos. Figura 7 ensayo referencia

# Diccionario para almacenar resultados
pujas_d_values = {d: [] for d in d_values}

# Simulaciones
for d in d_values:
    print(f"Simulando para d = {d}")
    for n in N_values:
        _, _, bids = comparacion_simulaciones(n, d)
        pujas_media = sum(bids) / len(bids)
        pujas_d_values[d].append(pujas_media)

# Gráfico
plt.figure(figsize=(10,6))

for d in d_values:
    plt.plot([0] + N_values, [0] + pujas_d_values[d], label=f"d = {d}", marker='o') #Añado que pase por el origen pues en t0do el proyecto he considerado que hay más de un pujador y sino tengo que cambiar varias cosas. Así mejor

plt.title("Número esperado de pujas efectivas vs Número de postores")
plt.xlabel("Número de postores (N)")
plt.ylabel("Pujas efectivas promedio")
plt.xlim(0, 40)
plt.ylim(0, 8)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
