import numpy
import matplotlib.pyplot
import pandas
from itertools import combinations
from networkx import DiGraph
from vrpy import VehicleRoutingProblem

X1 = numpy.array([2.33969,2.33650,2.32698,2.32159,2.29991])
#print(X1)
Y1 = numpy.array([48.84563,48.83730,48.83320,48.84117,48.84126])
#print(Y1)
x_s = 2.36815
y_s = 48.74991
X = X1 - x_s
Y = Y1 - y_s

#%% avec networkx et vrpy

def distance_cartesienne(x1, x2, y1, y2):
    return numpy.sqrt(numpy.square(x1-x2)+numpy.square(y1-y2))

G3 = DiGraph()

for (i, (xval, yval)) in enumerate(zip(X, Y)):
    G3.add_edge("Source", i, cost = distance_cartesienne(xval, 0, yval, 0))
    G3.add_edge(i, "Sink", cost = distance_cartesienne(xval, 0, yval, 0))
    G3.nodes[i]["demand"] = 1

for ((i, (x1, y1)), (j, (x2, y2))) in combinations(list(enumerate(zip(X, Y))), 2):
    G3.add_edge(i, j, cost = distance_cartesienne(x1, x2, y1, y2))
    G3.add_edge(j, i, cost = distance_cartesienne(x1, x2, y1, y2))

probleme_optimisation = VehicleRoutingProblem(G3, load_capacity = 9999)
probleme_optimisation.solve()

#print(probleme_optimisation.best_value)
#print(probleme_optimisation.best_routes)

matplotlib.pyplot.figure(figsize=(10,10))
matplotlib.pyplot.scatter(X, Y, color = 'red', marker = 'x')

for route in probleme_optimisation.best_routes.values():
    itineraire_X = [0] + [X[p] for p in route[1:-1]] + [0]
    itineraire_Y = [0] + [Y[p] for p in route[1:-1]] + [0]
    for (a, b, c, d) in zip(itineraire_X[:-1], itineraire_Y[:-1], [x2-x1 for (x1, x2) in zip(itineraire_X[:-1], itineraire_X[1:])], [y2-y1 for (y1, y2) in zip(itineraire_Y[:-1], itineraire_Y[1:])]):
        matplotlib.pyplot.arrow(a, b, c, d, width = 0.0001, color = 'black', length_includes_head = True, head_width = 0.001)
matplotlib.pyplot.title("Routage d'une tournée des 6 destinations au départ du dépôt SOGARIS")
matplotlib.pyplot.show()

#%% avec le service d’itinéraire du GéoPortail :
import requests
import json

G4 = DiGraph()

for (i, (xval, yval)) in enumerate(zip(X1, Y1)):
    r = requests.get(f"https://wxs.ign.fr/essentiels/geoportail/itineraire/rest/1.0.0/route?resource=bdtopo-osrm&start={x_s},{y_s}&end={xval},{yval}").json()
    distance_reelle = r['distance']
    G4.add_edge("Source", i, cost = distance_reelle)
    G4.add_edge(i, "Sink", cost = distance_reelle)
    G4.nodes[i]["demand"] = 1

for ((i, (x1, y1)), (j, (x2, y2))) in combinations(list(enumerate(zip(X1, Y1))), 2):
    r = requests.get(f"https://wxs.ign.fr/essentiels/geoportail/itineraire/rest/1.0.0/route?resource=bdtopo-osrm&start={x1},{y1}&end={x2},{y2}").json()
    distance_reelle = r['distance']
    G4.add_edge(i, j, cost = distance_reelle)
    G4.add_edge(j, i, cost = distance_reelle)

probleme_optimisation = VehicleRoutingProblem(G4, load_capacity = 9999)
probleme_optimisation.solve()

#print(probleme_optimisation.best_value)
#print(probleme_optimisation.best_routes)

matplotlib.pyplot.figure(figsize=(10,10))
matplotlib.pyplot.scatter(X, Y, color = 'red', marker = 'x')

for route in probleme_optimisation.best_routes.values():
    itineraire_X = [0] + [X[p] for p in route[1:-1]] + [0]
    itineraire_Y = [0] + [Y[p] for p in route[1:-1]] + [0]
    for (a, b, c, d) in zip(itineraire_X[:-1], itineraire_Y[:-1], [x2-x1 for (x1, x2) in zip(itineraire_X[:-1], itineraire_X[1:])], [y2-y1 for (y1, y2) in zip(itineraire_Y[:-1], itineraire_Y[1:])]):
        matplotlib.pyplot.arrow(a, b, c, d, width = 0.0001, color = 'blue', length_includes_head = True, head_width = 0.001)
matplotlib.pyplot.title("Routage d'une tournée des 6 destinations avec distances réelles au départ du dépôt SOGARIS")
matplotlib.pyplot.show()


#%% avec osmnx
import osmnx
import requests
import json

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

print(itineraire_X)
print(itineraire_Y)

fig, ax = osmnx.plot_graph(osmnx.project_graph(G2))
origine = osmnx.distance.nearest_nodes(G2,itineraire_X[0],itineraire_Y[0])
etape1 = osmnx.distance.nearest_nodes(G2,itineraire_X[1],itineraire_Y[1])
route = osmnx.shortest_path(G2,origine,etape1)
route_list = []
#origine = osmnx.distance.nearest_nodes(G2, X=2.34017, Y=48.84635)
#destination = osmnx.distance.nearest_nodes(G2, X=2.35036, Y=48.8413)
for i in range(len(itineraire_X)-1):
    origine = osmnx.distance.nearest_nodes(G2,itineraire_X[i],itineraire_Y[i])
    arrivee = osmnx.distance.nearest_nodes(G2,itineraire_X[i+1],itineraire_Y[i+1]) 
    route = osmnx.shortest_path(G2,origine,arrivee)
    route_list.append(route)

fig, ax = osmnx.plot_graph_routes(G2, route_list, node_size=0)


"""
origine = osmnx.distance.nearest_nodes(G2,itineraire_X[0],itineraire_Y[0])
etape1 = osmnx.distance.nearest_nodes(G2,itineraire_X[1],itineraire_Y[1])
route = osmnx.shortest_path(G2,origine,etape1)
for i in range(1,len(itineraire_X)-1):
    etape_depart = osmnx.distance.nearest_nodes(G2,itineraire_X[i],itineraire_Y[i])
    etape_suivante = osmnx.distance.nearest_nodes(G2,itineraire_X[i+1],itineraire_Y[i+1]) 
    route_suivante = osmnx.shortest_path(G2,origine,arrivee)"""
