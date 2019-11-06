import numpy as np
import pandas as pd
import networkx as nx

input_file_address = "../"

input_file_name = "agg clean sociopattern_conference_contact.txt"
input_file_name = "agg giant clean primaryschool.txt"

input_file_names = ["agg clean sociopattern_hospital.txt",
        "agg clean sociopattern_conference_contact.txt", 
                    "agg giant clean primaryschool.txt"]
for input_file_name in input_file_names:
    graph_edges = pd.read_csv( input_file_address + input_file_name, sep = '\t', header = None )
    graph_edges = np.array(graph_edges)
    G = nx.Graph()
    
    for edge in graph_edges:
        G.add_edge( edge[0], edge[1] )
    
    adj_matrix = nx.to_numpy_matrix(G)
    k = np.array([val for (node, val) in G.degree()])
    
    phi = k.mean() / (  (k**2).mean() - k.mean()  )
    clean_name = input_file_name.split('.txt')[0]
    clean_name = clean_name.split('clean ')[1]
    print(clean_name, np.round(phi, 4) )