import numpy
import matplotlib.pyplot
import pandas
from itertools import combinations
from networkx import DiGraph
from vrpy import VehicleRoutingProblem
import osmnx
import requests
import json

X1 = numpy.array([2.33969,2.33650,2.32698,2.32159,2.29991])
#print(X1)
Y1 = numpy.array([48.84563,48.83730,48.83320,48.84117,48.84126])
#print(Y1)
x_s = 2.36815
y_s = 48.74991
X = X1 - x_s
Y = Y1 - y_s

## On reprend la configuration de la question 1.c), et on la modifie pour la calculer au la consommation au fur et à mesure du trajet

# Pour une vitesse de 15 km/h (on a choisi cette vitesse en regardant les temps de trajet et les longueurs de trajet estimées par osmnx pour des questions de cohérence):
P = P = 0.3*60*(15/3.6)*(0.5*1.2*((15/3.6)**2)*0.46*(10**(-3))*4.56 + 3500*9.81*(2.15*(10**(-3)) + 0.015*((15/3.6)**2))) # puissance fois rendement (avec unités correctes)

G2 = osmnx.graph_from_address(
 address="60 boulevard Saint-Michel, Paris, France",
 dist=2000,
 dist_type="network",
 network_type="drive",
)

G5 = DiGraph()

for (i, (xval, yval)) in enumerate(zip(X1, Y1)):
    r = requests.get(f"https://wxs.ign.fr/essentiels/geoportail/itineraire/rest/1.0.0/route?resource=bdtopo-osrm&start={x_s},{y_s}&end={xval},{yval}").json()
    distance_reelle = r['distance']
    G5.add_edge("Source", i, cost = distance_reelle)
    G5.add_edge(i, "Sink", cost = distance_reelle)
    G5.nodes[i]["demand"] = 1

for ((i, (x1, y1)), (j, (x2, y2))) in combinations(list(enumerate(zip(X1, Y1))), 2):
    r = requests.get(f"https://wxs.ign.fr/essentiels/geoportail/itineraire/rest/1.0.0/route?resource=bdtopo-osrm&start={x1},{y1}&end={x2},{y2}").json()
    distance_reelle = r['distance']
    G5.add_edge(i, j, cost = distance_reelle)
    G5.add_edge(j, i, cost = distance_reelle)

probleme_optimisation = VehicleRoutingProblem(G5, load_capacity = 9999)
probleme_optimisation.solve()

for route in probleme_optimisation.best_routes.values():
    itineraire_X = [x_s] + [X1[p] for p in route[1:-1]] + [x_s]
    itineraire_Y = [y_s] + [Y1[p] for p in route[1:-1]] + [y_s]

#print(itineraire_X)
#print(itineraire_Y)

fig, ax = osmnx.plot_graph(osmnx.project_graph(G2))
route_list = []
consommation = 0
#origine = osmnx.distance.nearest_nodes(G2, X=2.34017, Y=48.84635)
#destination = osmnx.distance.nearest_nodes(G2, X=2.35036, Y=48.8413)
for i in range(len(itineraire_X)-1):
    origine = osmnx.distance.nearest_nodes(G2,itineraire_X[i],itineraire_Y[i])
    arrivee = osmnx.distance.nearest_nodes(G2,itineraire_X[i+1],itineraire_Y[i+1]) 
    route = osmnx.shortest_path(G2,origine,arrivee)
    route_list.append(route)
    r = requests.get(f"https://wxs.ign.fr/essentiels/geoportail/itineraire/rest/1.0.0/route?resource=bdtopo-osrm&start={itineraire_X[i]},{itineraire_Y[i]}&end={itineraire_X[i+1]},{itineraire_Y[i+1]}").json()
    t = r['duration']
    print(f"temps de trajet : {t}")
    print(f"longueur de trajet : {r['distance']}")
    consommation += P*t
    

fig, ax = osmnx.plot_graph_routes(G2, route_list, node_size=0)
print(f"La consommation énergétique est de {int(consommation)} J")
