from Simulation.Proxy_Bidding_Simulation import ejecutar_simulaciones_d
"""
Fig. 3. Comparison of simulation (solid lines) and calculated (circles) results showing the dependence 
of the expected auction revenue on the minimum bid increment for both the eBay proxy
bidding system and pedestrian bidding. Results are for 2 bidders with valuations drawn uniformly
on [0,1] and s = 0. Simulation results are averaged over 500,000 auctions.
Únicamente mostramos el caso para eBay Proxy Bidding. Máximo incremento mínimo de puja d = 0.5. Extraído de la obra de los autores. 10000 simulaciones.
"""
ejecutar_simulaciones_d(2, 0.5)