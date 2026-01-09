from Simulation.Multiple_Affiliated import (comparacion_simulaciones_multiple,plot_model_comparison,
                                            compare_models)
import matplotlib.pyplot as plt
# Parámetros
m = 5
max_min_increment = 0.2
sims = 100
Valuation_method = ["common_value", "correlated_private", "independent"]

# Gráfico para Common Value (Figura 5)
x10, y10, z10 = comparacion_simulaciones_multiple(10, m, max_min_increment, sims, valuation_method="common_value")
x20, y20, z20 = comparacion_simulaciones_multiple(20, m, max_min_increment, sims, valuation_method="common_value")
x40, y40, z40 = comparacion_simulaciones_multiple(40, m, max_min_increment, sims, valuation_method="common_value")

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 14
fig, ax = plt.subplots(figsize=(10,6))
ax.plot(x10, y10, marker='o', label='n = 10')
ax.plot(x20, y20, marker='o', label='n = 20')
ax.plot(x40, y40, marker='o', label='n = 40')
ax.set_title(f"Valor Común. m = {m}", fontsize=18)
ax.set_xlabel("Incremento Mínimo de Puja d", fontsize=16)
ax.set_ylabel("Ingreso Esperado de la Subasta", fontsize=16)
ax.set_ylim(0, 1.0)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(True, linestyle='--', alpha=0.5)
ax.text(x10[-1], y10[-1], "n = 10", fontsize=14, color='black', ha='left', va='bottom')
ax.text(x20[-1], y20[-1], "n = 20", fontsize=14, color='black', ha='left', va='bottom')
ax.text(x40[-1], y40[-1], "n = 40", fontsize=14, color='black', ha='left', va='bottom')
plt.tight_layout()
plt.show()

# Gráfico para Correlated Private (Figura 5)
x10, y10, z10 = comparacion_simulaciones_multiple(10, m, max_min_increment, sims, valuation_method="correlated_private")
x20, y20, z20 = comparacion_simulaciones_multiple(20, m, max_min_increment, sims, valuation_method="correlated_private")
x40, y40, z40 = comparacion_simulaciones_multiple(40, m, max_min_increment, sims, valuation_method="correlated_private")

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 14
fig, ax = plt.subplots(figsize=(10,6))
ax.plot(x10, y10, marker='o', label='n = 10')
ax.plot(x20, y20, marker='o', label='n = 20')
ax.plot(x40, y40, marker='o', label='n = 40')
ax.set_title(f"Valoraciones Privadas Correlacionadas  m = {m}", fontsize=18)
ax.set_xlabel("Incremento Mínimo de Puja d", fontsize=16)
ax.set_ylabel("Ingreso Esperado de la Subasta", fontsize=16)
ax.set_ylim(0, 1.0)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(True, linestyle='--', alpha=0.5)
ax.text(x10[-1], y10[-1], "n = 10", fontsize=14, color='black', ha='left', va='bottom')
ax.text(x20[-1], y20[-1], "n = 20", fontsize=14, color='black', ha='left', va='bottom')
ax.text(x40[-1], y40[-1], "n = 40", fontsize=14, color='black', ha='left', va='bottom')
plt.tight_layout()
plt.show()

# Gráfico para Independent (Figura 5)
x10, y10, z10 = comparacion_simulaciones_multiple(10, m, max_min_increment, sims, valuation_method="independent")
x20, y20, z20 = comparacion_simulaciones_multiple(20, m, max_min_increment, sims, valuation_method="independent")
x40, y40, z40 = comparacion_simulaciones_multiple(40, m, max_min_increment, sims, valuation_method="independent")

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 14
fig, ax = plt.subplots(figsize=(10,6))
ax.plot(x10, y10, marker='o', label='n = 10')
ax.plot(x20, y20, marker='o', label='n = 20')
ax.plot(x40, y40, marker='o', label='n = 40')
ax.set_title(f"Valoraciones Privadas Independientes. m = {m}", fontsize=18)
ax.set_xlabel("Incremento Mínimo de Puja d", fontsize=16)
ax.set_ylabel("Ingreso Esperado de la Subasta", fontsize=16)
ax.set_ylim(0, 1.0)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(True, linestyle='--', alpha=0.5)
ax.text(x10[-1], y10[-1], "n = 10", fontsize=14, color='black', ha='left', va='bottom')
ax.text(x20[-1], y20[-1], "n = 20", fontsize=14, color='black', ha='left', va='bottom')
ax.text(x40[-1], y40[-1], "n = 40", fontsize=14, color='black', ha='left', va='bottom')
plt.tight_layout()
plt.show()