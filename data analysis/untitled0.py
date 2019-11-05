#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 19:45:32 2019

@author: sepante
"""
import matplotlib.pyplot as plt
import networkx as nx
#G = nx.generators.circular_ladder_graph(10)
G = nx.generators.random_graphs.barabasi_albert_graph(10,5)
Q = nx.generators.random_graphs.erdos_renyi_graph(10,0.3)
nx.draw(Q)