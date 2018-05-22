#include "SIR.h"
#include <iostream>
#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/graph_utility.hpp>
#include <boost/graph/properties.hpp>
#include <boost/config.hpp>
#include <boost/graph/connected_components.hpp>

using namespace boost;

typedef adjacency_list<listS, vecS, undirectedS, SIR> Network;
typedef graph_traits<Network>::edges_size_type Edge_Num;
typedef graph_traits<Network>::vertices_size_type Vertex_Num;
typedef graph_traits<Network>::vertex_iterator Vertex_iter;
typedef graph_traits<Network>::vertex_descriptor Vertex;
typedef graph_traits<Network>::edge_descriptor Edge;
typedef graph_traits<Network>::edge_iterator Edge_iter;
