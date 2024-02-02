#OBJECTIF DU PROGRAMME (Q2 légèrement modifiée): donner 6 points au programme qui va créer un itinéraire entre chaque point les concatener

import osmnx as ox
import networkx as nx
import geopandas as gpd
from shapely.geometry import Point, LineString
import matplotlib.pyplot as plt 
import tkinter as tk
import requests
import json
from tkinter import ttk
import pandas as pd

# Fonction pour obtenir le meilleur itinéraire entre deux points
def get_best_route(start_point, end_point):
    global city_graph
    # Télécharger le graphe de la ville de Paris
    city_graph = ox.graph_from_place('Paris, France', network_type='drive')

    # Obtenir le noeud le plus proche du point de départ
    orig_node = ox.distance.nearest_nodes(city_graph, start_point[1], start_point[0])
    # Obtenir le noeud le plus proche du point d'arrivée
    dest_node = ox.distance.nearest_nodes(city_graph, end_point[1], end_point[0])

    # Calculer le meilleur itinéraire
    route = nx.shortest_path(city_graph, orig_node, dest_node, weight='length')
    
    # Convertir la géométrie en un objet GeoDataFrame
    #route_geometry = ox.plot_graph_route(city_graph, route, route_linewidth=6, node_size=0, bgcolor='k', edge_color='r', show=False)

    return route




def algo():
    start_point = D[choixdep.get()]  # Coordonnées de la Tour Eiffel
    choix_2=D[choix2.get()]
    choix_3=D[choix3.get()]
    choix_4=D[choix4.get()]
    end_point = D[choixfin.get()]    # Coordonnées du Louvre
    fenetre.destroy()
    Point=[start_point,choix_2,choix_3,choix_4,end_point]
    route=[]
    for i in range(0,4):
        r=get_best_route(Point[i],Point[i+1])
        route.append(r)
    fig,ax = ox.plot_graph_routes(city_graph,route,node_size=1)
    return


D={'Tour Eiffel': (48.8566, 2.3522), 
'Louvre':(48.8566, 2.2944), 
'Mines Paris' : (48.84563, 2.33969),
'Observatoire de Paris' : (48.83730,2.33650,),
'Marie du 14e' : (48.83320,2.32698),
'Gare Montparnasse TGV' : (48.84117,2.32159),
'Mairie du 15e' : (48.84126,2.29991),
'Arc de Triomphe': (48.8738,2.295),
'Intercontinental': (48.870834,2.330427),
'Grand Palais': (48.866135,2.312962)}



fenetre = tk.Tk()
fenetre.title("Projet info")
fenetre.geometry('300x300')
titre = tk.Label(fenetre, text = "Sélectionner un point de départ:")
titre.pack()
L=['Départ']
for lieux in D.keys():
    L.append(lieux)
choixdep = ttk.Combobox(fenetre, values=L)
choixdep.pack()



titre3 = tk.Label(fenetre, text = "Sélectionner une étape")
titre3.pack()
choix2 = ttk.Combobox(fenetre, values=L)
choix2.pack()

titre3 = tk.Label(fenetre, text = "Sélectionner une étape")
titre3.pack()
choix3 = ttk.Combobox(fenetre, values=L)
choix3.pack()
titre3 = tk.Label(fenetre, text = "Sélectionner une étape")
titre3.pack()
choix4 = ttk.Combobox(fenetre, values=L)
choix4.pack()

titre2 = tk.Label(fenetre, text = "Sélectionner un point d'arrivé:")
titre2.pack()
choixfin = ttk.Combobox(fenetre, values=L)
choixfin.pack()
Valider = tk.Button(fenetre, text="Valider", command=algo)
Valider.pack()  

fenetre.mainloop()
