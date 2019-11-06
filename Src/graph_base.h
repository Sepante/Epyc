#ifndef GRAPH_BASE_H
#define GRAPH_BASE_H


#include <iostream>
#include <boost/graph/adjacency_list.hpp>
//#include <boost/graph/graph_utility.hpp>
//#include <boost/graph/properties.hpp>
//#include <boost/config.hpp>
//#include <boost/graph/connected_components.hpp>
#include "Person.h"
#include "global.h"

using namespace boost;
typedef adjacency_list<listS, vecS, undirectedS, Person> Network;
//typedef adjacency_list<listS, vecS, undirectedS, Person(SamplingAlgorithm algorithm)> Network2(SamplingAlgorithm algorithm);
//typedef adjacency_list<listS, vecS, undirectedS, Person(int a)> Network2(int a);
typedef graph_traits<Network>::edges_size_type Edge_Num;
typedef graph_traits<Network>::vertices_size_type Vertex_Num;
typedef graph_traits<Network>::vertex_iterator Vertex_iter;
typedef graph_traits<Network>::vertex_descriptor Vertex;
typedef graph_traits<Network>::edge_descriptor Edge;
typedef graph_traits<Network>::edge_iterator Edge_iter;

extern Network society;
//extern Network2 society;
//int qqq;

//graph constructor functions
void cons_Erdos(int n);
void cons_grid(int n);
void cons_grid3D(int n);
void cons_stochastic_block_network(int n, float disparity_prob);
#endif
