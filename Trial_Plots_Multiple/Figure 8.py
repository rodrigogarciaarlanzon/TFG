from Simulation.Multiple_Proxy_Bidding_Simulation import prob_win_order_multiple
import matplotlib.pyplot as plt
import numpy as np

"""
Fig. 8. Simulation results showing the probability of each bidder winning the auction depending
on the order in which they bid. There are 20 bidders with valuations drawn uniformly on [0,1] and
s =0. Results are averaged over 10^7 auctions
"""
m = 5
res = prob_win_order_multiple(n=20, m = m, d_values=[0,0.025,0.05,0.075,0.1], sims=1000)
# Gráfico comparativo
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 14
fig, ax = plt.subplots(figsize=(10,6))
pos = np.arange(1, 21)
# Curvas para cada d
for d in res:
    ax.plot(pos,res[d],marker='o',linewidth=2,label=f"d = {d}")
    # Etiqueta identificativa al final de cada curva
    ax.text(pos[-1],res[d][-1],f"d = {d}",fontsize=14,ha='left',va='bottom')
# Títulos y etiquetas
ax.set_title(f"m ={m} ", fontsize=18)
ax.set_xlabel("Orden de Llegada", fontsize=16)
ax.set_ylabel("Probabilidad de Ganar un Objeto", fontsize=16)
# Límites de los ejes
ax.set_xlim(1, 20)
ax.set_ylim(0, 0.8)
# Intersección en (0, 0)
ax.spines['bottom'].set_position(('data', 0))
ax.spines['left'].set_position(('data', 0))
# Ocultar ejes superior y derecho
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
# Cuadrícula suave
ax.grid(True, linestyle='--', alpha=0.5)
# Leyenda
ax.legend()
plt.tight_layout()
plt.show()
