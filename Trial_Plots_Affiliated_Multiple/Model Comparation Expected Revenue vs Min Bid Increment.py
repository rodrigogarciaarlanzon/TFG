from Simulation.Multiple_Affiliated import plot_model_comparison,compare_models


m = 5
max_min_increment = 0.2
sims = 100
Valuation_method = ["common_value", "correlated_private", "independent"]

#Comparar modelos
results = compare_models(n=20, m=m, max_min_increment=max_min_increment, sims=sims)

# Gráfico comparativo
plot_model_comparison(results)