#include <iostream>
#include <fstream>
#include <vector>
#include <array>
#include <set>
#include <ctime>
#include <math.h>
#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/graph_utility.hpp>
#include <boost/graph/properties.hpp>


float r, p = 0.5, q = 1;
std::set <int> actives={};
bool dice(float prob)
{
	float r = ((float) rand() / (RAND_MAX));
	if (r <= prob)
		return 1;
	else return 0;
}

typedef enum { none = 1, both = 6, dis_one = 2, dis_two = 3 } Transfer;
//typedef enum { none, dis_one, dis_two, both } State;

class Person
{
	public:
	int health = 1;
	int future = 1;
	Transfer demand()
	{
		if(future == 1)
			return both;
			else if (future == 3 || future == 9)
			{
				return dis_one;
			}
			else if (future == 2 || future == 4)
			{
				return dis_two;
			}
			else return none;
	};

	Transfer supply()
	{
		if(health == 6)
			return both;
			else if (health == 2 || health == 18)
			{
				return dis_one;
			}
			else if (health == 3 || health == 12)
			{
				return dis_two;
			}
			else return none;
	};

	void turn_I(Transfer supply)
	{
		//std::cout << health << "," << supply << "-->";
		Transfer demand_v = demand();
		switch (demand_v)
		{
		case none:
			//std::cout << "Invalid selection!" << std::endl;
			break;
    case both:
			if (supply == both) // supply and demand are in "both" state.
			{
				auto dis_first = dis_one, dis_second = dis_two;
				if (dice(0.5))
				{
					dis_first = dis_two;
					dis_second = dis_one;
				}

				if (dice(p))
				{
					if (dice(q))
						future *= (dis_first*dis_second) ;
					else
						future *= dis_first;
				}
				else if (dice(p))
					future *= dis_second;
			}
			else if (dice(p))
				future *= supply;
			//std::cout << "First item selected!" << std::endl;
 			break;
    default:
      //std::cout << "Second item selected!" << std::endl;
			if (supply == demand_v || supply == both)
				future *= demand_v;
      break;
		}
		//std::cout << health << '\n';
	};

	Transfer update()
	{
		health = supply()*future;
		future = health;
		return supply();
	}
};

using namespace boost;
using std::cout;
using std::endl;

typedef adjacency_list<listS, vecS, undirectedS, Person> Network;
typedef graph_traits<Network>::edges_size_type Edge_Num;
typedef graph_traits<Network>::vertices_size_type Vertex_Num;
typedef graph_traits<Network>::vertex_iterator Vertex_iter;
typedef graph_traits<Network>::vertex_descriptor Vertex;

int main()
{
	//	srand(12);
	Vertex_Num vert_num = 20;
	Edge_Num edge_num = 0;
	//Network graph(ERGen(gen, vert_num, edge_num), ERGen(), vert_num);
	float cnct_prob = (float)4/(float)edge_num;
	Network graph(vert_num);

	for (size_t i = 0; i < vert_num; i++)
	{
		for (size_t j = i+1; j < vert_num; j++)
		{
			if ( dice(cnct_prob) )
			{
				add_edge(i, j, graph);
					//std::cout << i << ", " << j << '\n';
			}
		}
	}
	boost::print_graph(graph);
	int seed = rand() % vert_num;
	Vertex v = vertex(seed, graph);
	graph[v].health = 6;
	actives.insert(seed);
	for (size_t t = 0; t <= 8 && actives.size() >= 1 ; t++)
	{
	//	std::cout << "time: "<< t << '\n';
		for( Vertex vd : make_iterator_range( vertices(graph) ) )
	  {
			if (graph[vd].supply() != 1)
			{
					//std::cout << graph[vd].health << '\n';
				for ( Vertex vi : make_iterator_range( adjacent_vertices(vd, graph) ) )
				{
					graph[vi].turn_I( graph[vd].supply() );
					//std::cout << "neighb: " << vi << '\n';
					//std::cout << vi << ":  " << graph[vi].health << '\n';
				}
			}
			//std::cout << vd << ":  " << graph[vd].health << '\n';
	  }
		for( Vertex vd : make_iterator_range( vertices(graph) ) )
		{
			actives = {};
			if(graph[vd].update() != 1)
			{
				actives.insert(vd);
				std::cout << "supplier: " << graph[vd].supply() << '\n';
			}
			else
			std::cout << "non-supplier: " << graph[vd].supply() << '\n';
			//std::cout << vd << ": " << graph[vd].health << '\n';
		}
		std::cout << '\n';
	}
}
