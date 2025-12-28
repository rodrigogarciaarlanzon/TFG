from Simulation.Multiple_Affiliated import sim_bids_fixed_d_multiple
import matplotlib.pyplot as plt
import numpy as np
"""
Fig. 7. Comparison of simulation (solid lines) and calculated (circles) results showing the number
of bids observed (n) compared to the number of bidders who attempted to place a bid (N). The
starting price s = 0 and for results where d > 0, bidders’ valuations are drawn uniformly on [0,1].
Results are averaged over 500,000 auctions.
"""

# Parámetros
N_values = list(range(1, 41))  # De 0 a 40
d_values = [0.01, 0.025, 0.05, 0.075, 0.1]
m = 5
reserve_price = 0
sims = 1000
Valuation_method = ["common_value", "correlated_private", "independent"]

# Gráfico para Common Value (Figura 7)
pujas_d_values = {d: [] for d in d_values}
for d in d_values:
    print(f"Simulando para d = {d}")
    for n in N_values:
        pujas_mean = sim_bids_fixed_d_multiple(n,m, reserve_price, d, sims, valuation_method="common_value", sigma_reserve=0.05, sigma_increment=0.002)
        pujas_d_values[d].append(pujas_mean)

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 14
fig, ax = plt.subplots(figsize=(10,6))

for d in d_values:
    ax.plot([0] + N_values,[0] + pujas_d_values[d],marker='o',label=f"d = {d}")
    ax.text(N_values[-1],pujas_d_values[d][-1],f"d = {d}",fontsize=14,ha='left',va='bottom')
N_continuo = np.linspace(1, 40, 400)
f_teorica = 2 * np.log(N_continuo)
ax.plot(N_continuo, f_teorica,label="n = 2 ln(N)",color="black",linewidth=2)
ax.set_title("Expected number of bid observed n vs Potential bidders N. Common Value (m = 5)", fontsize=18)
ax.set_xlabel("Potential bidders N", fontsize=16)
ax.set_ylabel("Bids observed n", fontsize=16)
ax.set_xlim(0, 40)
ax.set_ylim(0, 8)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend()
plt.tight_layout()
plt.show()

# Gráfico para Correlated Private (Figura 7)
pujas_d_values = {d: [] for d in d_values}
for d in d_values:
    print(f"Simulando para d = {d}")
    for n in N_values:
        pujas_mean = sim_bids_fixed_d_multiple(n,m, reserve_price, d, sims, valuation_method="correlated_private", sigma_reserve=0.05, sigma_increment=0.002)
        pujas_d_values[d].append(pujas_mean)

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 14
fig, ax = plt.subplots(figsize=(10,6))

for d in d_values:
    ax.plot([0] + N_values,[0] + pujas_d_values[d],marker='o',label=f"d = {d}")
    ax.text(N_values[-1],pujas_d_values[d][-1],f"d = {d}",fontsize=14,ha='left',va='bottom')
N_continuo = np.linspace(1, 40, 400)
f_teorica = 2 * np.log(N_continuo)
ax.plot(N_continuo, f_teorica,label="n = 2 ln(N)",color="black",linewidth=2)
ax.set_title("Expected number of bid observed n vs Potential bidders N. Correlated Private (m = 5)", fontsize=18)
ax.set_xlabel("Potential bidders N", fontsize=16)
ax.set_ylabel("Bids observed n", fontsize=16)
ax.set_xlim(0, 40)
ax.set_ylim(0, 8)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend()
plt.tight_layout()
plt.show()

# Gráfico para Independent (Figura 7)
pujas_d_values = {d: [] for d in d_values}
for d in d_values:
    print(f"Simulando para d = {d}")
    for n in N_values:
        pujas_mean = sim_bids_fixed_d_multiple(n,m, reserve_price, d, sims, valuation_method="independent", sigma_reserve=0.05, sigma_increment=0.002)
        pujas_d_values[d].append(pujas_mean)

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 14
fig, ax = plt.subplots(figsize=(10,6))

for d in d_values:
    ax.plot([0] + N_values,[0] + pujas_d_values[d],marker='o',label=f"d = {d}")
    ax.text(N_values[-1],pujas_d_values[d][-1],f"d = {d}",fontsize=14,ha='left',va='bottom')
N_continuo = np.linspace(1, 40, 400)
f_teorica = 2 * np.log(N_continuo)
ax.plot(N_continuo, f_teorica,label="n = 2 ln(N)",color="black",linewidth=2)
ax.set_title("Expected number of bid observed n vs Potential bidders N. Independent (m = 5)", fontsize=18)
ax.set_xlabel("Potential bidders N", fontsize=16)
ax.set_ylabel("Bids observed n", fontsize=16)
ax.set_xlim(0, 40)
ax.set_ylim(0, 8)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend()
plt.tight_layout()
plt.show()