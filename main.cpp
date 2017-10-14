#include <fstream>
#include <iostream>
#include <vector>
#include <array>
#include <set>
#include <ctime>
#include <math.h>
#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/graph_utility.hpp>
#include <boost/graph/properties.hpp>
#include <boost/config.hpp>
using namespace boost;
using std::cout;
using std::endl;
using std::vector;



float r, p = 1, q = 1;
float percol_prob = 0;
//int actives = 0;
std::set <int> actives={};
//int runNum = 1000;

//int infect_cluster;
bool dice(float prob)
{
	float r = ((float) rand() / (RAND_MAX));
	if (r < prob)
		return 1;
	else return 0;
}


typedef enum { neither = 1, both = 6, dis_one = 2, dis_two = 3 } Transfer;
//typedef enum { neither, dis_one, dis_two, both } State;

class Interaction
{
	public:
	int present = 1;
};

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
			else return neither;
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
			else return neither;
	};

	void turn_I(Transfer supply)
	{
		//std::cout << health << "," << supply << "-->";
		Transfer demand_v = demand();
		switch (demand_v)
		{
		case neither:
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

//typedef adjacency_list<listS, vecS, undirectedS, Person> Network;
typedef adjacency_list<listS, vecS, undirectedS, Person, Interaction> Network;
typedef graph_traits<Network>::edges_size_type Edge_Num;
typedef graph_traits<Network>::vertices_size_type Vertex_Num;
typedef graph_traits<Network>::vertex_iterator Vertex_iter;
typedef graph_traits<Network>::vertex_descriptor Vertex;
typedef graph_traits<Network>::edge_descriptor Edge;
typedef graph_traits<Network>::edge_iterator Edge_iter;
//Vertex_Num vert_num = 131072;
Vertex_Num vert_num = 1024;
float cnct_prob = (float)4/(float)vert_num;
//float cnct_prob = 1;

//Network society(vert_num);
Network society;
Network society_origin;

void init_states()
{
	for( Vertex vd : make_iterator_range( vertices(society) ) )
	{
		society[vd].health = 1;
		society[vd].future = 1;
	}
	//int seed = rand() % vert_num;
	int seed = 2;
	Vertex v = vertex(seed, society);
	society[v].health = 6;
	society[v].future = 6;
	society_origin = Network(society);
	actives = {};
	actives.insert(seed);
}

int cluster_size()
{
	int infect_cluster = 0;
	for( Vertex vd : make_iterator_range( vertices(society) ) )
		if (society[vd].health != 1)
		{
			infect_cluster++;
		}
	return infect_cluster;
}

void kill_some_edges(float p)
{
	society = society_origin;
	Edge_iter vi, vi_end, next;
	boost::tie(vi, vi_end) = edges(society);
	for (next = vi; vi != vi_end; vi = next)
	{
		++next;
		if(dice (p) )
			remove_edge(*vi, society);
	}
}


int main()
{
	clock_t begin = clock();
	std::ofstream fout;
	fout.open("cdata.txt");

	srand(time(0));
	int runNum = 10;
	vector<Vertex> n_set={20000};
	vector<float> p_set={0.1, 0.3, 0.4, 0.5, 0.6, 0.8, 0.9, 1};
	vector<float> q_set={0.1 ,0.5, 0.8, 1};
	q_set={1};
	p_set={0.25};
	//write system properties to file, for later use in python.
	fout<<n_set.size()<<"\n";
	fout<<p_set.size()<<"\n";
	fout<<q_set.size()<<"\n";
	fout<<runNum<<"\n";


	for(int nindex=0; nindex<=n_set.size()-1; nindex++)
		fout<<n_set[nindex]<<"\n";
	for(int pindex=0; pindex<=p_set.size()-1; pindex++)
		fout<<p_set[pindex]<<"\n";
	for(int qindex=0; qindex<=q_set.size()-1; qindex++)
		fout<<q_set[qindex]<<"\n";

	//Edge_Num edge_num = 0;
	//Network society(ERGen(gen, vert_num, edge_num), ERGen(), vert_num);
//cout << "cnct_prob: "<< cnct_prob << endl;
/* // Erdos Renyi constructor.
	for (size_t i = 0; i < vert_num; i++)
	{
		for (size_t j = i+1; j < vert_num; j++)
		{
			if ( dice(cnct_prob) )
			{
				add_edge(i, j, society);
				//std::cout << i << "-->" << j << '\n';
			}
		}
	}
*/
	std::ifstream  fin;
	fin.open("input_matrix.txt");
	if (!fin)
	{
		std::cerr << "Unable to open file datafile.txt";
		exit(1);   // call system to stop
	}
	std::string text;
	int i, j;
	while (fin >> i && fin >>j)
	{
		if(i>=0)
			add_edge(i, j, society);
		else
			remove_edge(-i, j ,society);
		//std::cout << i << '-';
		//std::cout << j << '\n';
		fin>>text;
	}

	//boost::print_graph(society);



	for (size_t run = 0; run < runNum; run++)
	{
		//std::cout << "run: " << run << '\n';
		init_states();

		for (size_t t = 0; t <= 1000000 && actives.size() >= 1 ; t++)
		{
			kill_some_edges(percol_prob);
			//infect_cluster = 0;
			//for( Vertex vd : make_iterator_range( vertices(society) ) )
			Vertex vd;
			for (std::set<int>::iterator it=actives.begin(); it!=actives.end(); it++)
		  {
				vd = *it;
				//std::cout << "iterating vd: " << vd << '\n';
				if (society[vd].supply() != 1)
				{
					for ( Vertex vi : make_iterator_range( adjacent_vertices(vd, society) ) )
					{
						society[vi].turn_I( society[vd].supply() );
					}
				}
		  }
			for (std::set<int>::iterator it=actives.begin(); it!=actives.end(); it++)
			{
				vd = *it;
				cout << "set item: " << vd << ",  health: " << society[vd].health << endl;
			}

			actives = {};
			for( Vertex vd : make_iterator_range( vertices(society) ) )
			{
				if(society[vd].update() != 1)
				{
					actives.insert(vd);
				}
				//cout << vd << ": " << society[vd].health << endl;
			}
			//std::cout << '\n';
		//	std::cout << "t: " << t << '\n';
		}
		std::cout << "run: " << run << '\t' << "infecteds: " << cluster_size() << '\n';
		fout << cluster_size() << '\n';

		//society.clear();
	}


	clock_t end = clock();
  double elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
	std::cout << "time: " << elapsed_secs << '\n';



	//cout<<cnct_prob<<endl;
	boost::print_graph(society);
	std::cout << "next:" << '\n';
	boost::print_graph(society_origin);
}
