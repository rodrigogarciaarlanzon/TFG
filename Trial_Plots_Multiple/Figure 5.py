from Simulation.Multiple_Proxy_Bidding_Simulation import comparacion_simulaciones_multiple
import matplotlib.pyplot as plt

"""
Figura 5 (versión multiobjeto):
Simulation results showing the dependence of the expected auction revenue per object
on the number of bidders N using proxy bidding with m identical objects.

Results shown for N = 10, 20, and 40 bidders with valuations ~ U(0,1).
Reserve price s = 0. Results averaged over many simulations.
"""

# Parámetros
m = 5  # número de objetos en subasta
max_min_increment = 0.2
sims = 100

# Ejecutamos simulaciones para distintos N
x10, y10, z10 = comparacion_simulaciones_multiple(10, m, max_min_increment, sims)
x20, y20, z20 = comparacion_simulaciones_multiple(20, m, max_min_increment, sims)
x40, y40, z40 = comparacion_simulaciones_multiple(40, m, max_min_increment, sims)

# --- Gráfico comparativo ---
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 14

fig, ax = plt.subplots(figsize=(10,6))

ax.plot(x10, y10, marker='o', label='N = 10')
ax.plot(x20, y20, marker='o', label='N = 20')
ax.plot(x40, y40, marker='o', label='N = 40')

# Título y ejes
ax.set_title(f"Auction revenue per object vs number of bidders N (m = {m})", fontsize=18)
ax.set_xlabel("Minimum bid increment d", fontsize=16)
ax.set_ylabel("Expected auction revenue per object", fontsize=16)

# Rango del eje Y (ajústalo según tus resultados)
ax.set_ylim(0, 1.0)


# Ocultar ejes superior y derecho
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Cuadrícula suave
ax.grid(True, linestyle='--', alpha=0.5)

# Etiquetas sobre cada curva
ax.text(x10[-1], y10[-1], "N = 10", fontsize=14, color='black', ha='left', va='bottom')
ax.text(x20[-1], y20[-1], "N = 20", fontsize=14, color='black', ha='left', va='bottom')
ax.text(x40[-1], y40[-1], "N = 40", fontsize=14, color='black', ha='left', va='bottom')

plt.tight_layout()
plt.show()
