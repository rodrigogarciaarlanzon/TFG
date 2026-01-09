from Simulation.Proxy_Bidding_Simulation import comparacion_simulaciones
import matplotlib.pyplot as plt
"""
Fig. 5. Simulation results showing the dependence of the expected auction revenue on the number
of bidders using proxy bidding. Results are shown for 10, 20, and 40 bidders with valuations drawn
from auniformdistribution on [0,1]. The starting price s = 0 and results are averaged over 500,000
auctions.
"""
# Ejecutamos las simulaciones para distintos n
x10, y10, z10 = comparacion_simulaciones(10, 0.2, 5000)
x20, y20, z20 = comparacion_simulaciones(20, 0.2, 5000)
x40, y40, z40 = comparacion_simulaciones(40, 0.2,  5000)

# Gráfico comparativo
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 14
fig, ax = plt.subplots(figsize=(10,6))
ax.plot(x10, y10, marker='o', label='n = 10')
ax.plot(x20, y20, marker='o', label='n = 20')
ax.plot(x40, y40, marker='o', label='n = 40')
# Título y ejes
#ax.set_title("Ingreso Esperado frente a d. n = 10, 20, 40 ", fontsize=18)
ax.set_xlabel("Incremento Mínimo de Puja d", fontsize=16)
ax.set_ylabel("Ingreso Esperado de la Subasta", fontsize=16)
# Rango del eje Y
ax.set_ylim(0.8, 1)
# Intersección en (0, 0.8)
ax.spines['bottom'].set_position(('data', 0.8))
ax.spines['left'].set_position(('data', 0))
# Ocultar ejes superior y derecho
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
# Cuadrícula suave
ax.grid(True, linestyle='--', alpha=0.5)
# Etiquetas sobre cada curva
ax.text(x10[-1], y10[-1], "n = 10", fontsize=14, color='black', ha='left', va='bottom')
ax.text(x20[-1], y20[-1], "n = 20", fontsize=14, color='black', ha='left', va='bottom')
ax.text(x40[-1], y40[-1], "n = 40", fontsize=14, color='black', ha='left', va='bottom')
plt.tight_layout()
plt.show()


