from Simulation.Multiple_Proxy_Bidding_Simulation import prob_kth_max_val_wins_by_position_multiple, expected_profit_k_ght_max_valuation_by_position_multiple, plot_expected_profits_multiple, plot_probabilities_multiple
"""
Fig. 9. Simulation results showing (a) the probability of winning, and (b) the expected profit,when
the bidders with the highest and second highest valuations bid first, at a random time, and last.
There are 20 bidders with valuations drawn uniformly on [0,1] and s = 0. Results are averaged
over 107 auctions.
"""

#Replicación Figuras 9
n = 20
d_values = [0,0.02, 0.04, 0.06, 0.08, 0.1]
m = 5
#Figura 9(a)
results_9a = prob_kth_max_val_wins_by_position_multiple(n,m, d_values, sims=1000, k=1)
plot_probabilities_multiple(d_values, results_9a, 1, m)
#Figura 9(c)
results_9c = prob_kth_max_val_wins_by_position_multiple(n,m, d_values, sims=1000, k=2)
plot_probabilities_multiple(d_values, results_9c, 2, m)
#Figura 9(b)
results_9b = expected_profit_k_ght_max_valuation_by_position_multiple(n,m, d_values, sims=1000, k=1)
plot_expected_profits_multiple(d_values, results_9b, 1, m)
#Figura 9(d)
results_9d = expected_profit_k_ght_max_valuation_by_position_multiple(n,m, d_values, sims=1000, k=2)
plot_expected_profits_multiple(d_values, results_9d, 2, m)
