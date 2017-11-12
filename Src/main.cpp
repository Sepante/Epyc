#include "global.h"
#include "SIR.h"
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
#include <boost/graph/connected_components.hpp>

typedef enum { erdos = 1, from_file = 2} Graph_Type;
Graph_Type graphT = from_file;
//Graph_Type graphT = erdos;

using namespace boost;
using std::cout;
using std::endl;
using std::vector;


std::ifstream  fin;
float r = 1, p = 0.25, q = 1;
float percol_prob = 0;
//int actives = 0;
std::set <int> actives={};
int runNum = 5000;

//int infect_cluster;



//typedef enum { neither, dis_one, dis_two, both } State;

class Interaction
{
	public:
	int present = 1;
};


//typedef adjacency_list<listS, vecS, undirectedS, SIR> Network;
typedef adjacency_list<listS, vecS, undirectedS, SIR, Interaction> Network;
typedef graph_traits<Network>::edges_size_type Edge_Num;
typedef graph_traits<Network>::vertices_size_type Vertex_Num;
typedef graph_traits<Network>::vertex_iterator Vertex_iter;
typedef graph_traits<Network>::vertex_descriptor Vertex;
typedef graph_traits<Network>::edge_descriptor Edge;
typedef graph_traits<Network>::edge_iterator Edge_iter;
//Vertex_Num vert_num = 131072;
Vertex_Num vert_num = 256;
//float cnct_prob = (float)4/(float)vert_num;
//float cnct_prob = 1;

//Network society(vert_num);
Network society(8);

void init_states()
{
	for( Vertex vd : make_iterator_range( vertices(society) ) )
	{
		society[vd].health = 1;
		society[vd].future = 1;
	}
	int seed = rand() % num_vertices(society);
	//int seed = 2;
	Vertex v = vertex(seed, society);
	society[v].health = 6;
	society[v].future = 6;
	//society[v].health = 2;
	//society[v].future = 2;
	actives = {};
	actives.insert(seed);
	//std::cout << "seed: " << seed << '\n';
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
/*
void kill_some_edges(float p)
{
	Edge_iter vi, vi_end, next;
	boost::tie(vi, vi_end) = edges(society);
	for (next = vi; vi != vi_end; vi = next)
	{
		++next;
		if(dice (p) )
			remove_edge(*vi, society);
	}
}
*/
void cons_Erdos(int n)
{
	float cnct_prob = (float)4/(float)n;
	society.clear();
	//society(32);
	for (size_t i = 0; i < n; i++)
	{
		for (size_t j = i+1; j < n; j++)
		{
			if ( dice(cnct_prob) )
			{
				add_edge(i, j, society);
				//add_edge(j, i, society);
			}
		}
	}
	//std::cout << "Erdos running" << '\n';
}

void restart_read_file()
{
  //std::cout << "rest!" << '\n';
  //fin.clear();
  fin.seekg(0, fin.beg);
  fin.close();
  fin.open("input_matrix.txt");
  if (!fin)
  {
    std::cerr << "Unable to open file datafile.txt";
    exit(1);   // call system to stop
  }
}

int readfile(int t)
{
	//society.clear();
	Edge_iter vi, vi_end, next;
	boost::tie(vi, vi_end) = edges(society);
	for (next = vi; vi != vi_end; vi = next)
	{
		++next;
			remove_edge(*vi, society);
	}
  std::string temp;
  int read_time, i, j;
  auto read_location = fin.tellg() ;

  for (size_t k = 0 ; ; k++)
  {
    read_location = fin.tellg() ;
    fin >> read_time;
    if (read_time > t)
		{
			//std::cout << "read time: " << read_time << '\n';
			//std::cout << "break:  t: " << t << ", read time: " <<read_time << '\n';
			break;
		}
    //std::cout << "Enter!" << '\n' << '\n';
    fin >> i ; fin >>j ;
		//std::cout << "k: " << k << '\n';
		//std::cout << "t: " << t << '\n';
		//std::cout << i << " - " << j << '\n' << '\n';
		add_edge(i, j, society);
		//fin >> temp;
		//fin>> temp;
  }
  fin.clear();
  fin.seekg(read_location, fin.beg);
	//std::cout << "t = " << t << ", edge num = " << num_edges(society)  <<'\n';
	return read_time;
}

int main()
{
	int starting_time = 0;
	clock_t begin = clock();
	std::ofstream fout;
	fout.open("cdata.txt");

	srand(time(0));
	//std::vector<int> n_set={128, 256, 512,1024, 2048, 4096, 8192, 16384};
	//std::vector<int> n_set={16384};
	std::vector<int> n_set={256};
	std::vector<float> p_set={0.1, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.6, 1};
	//std::vector<float> p_set={0.8, 0.9, 1};
	std::vector<float> q_set={0.1 ,0.5, 0.8, 1};

	q_set={1};
	p_set={0.25};
	//p_set = {1};
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


	for(int nindex=0; nindex<n_set.size(); nindex++)
	{
		vert_num = n_set[nindex];
		if (graphT == erdos)
		{
			cons_Erdos(vert_num);
		}
		for (size_t pindex = 0; pindex < p_set.size(); pindex++)
		{
			p = p_set[pindex];
			for (size_t qindex = 0; qindex < q_set.size(); qindex++)
			{
				q = q_set[qindex];

				for (size_t run = 0; run < runNum; run++)
				{
					if (graphT == from_file)
					{
						restart_read_file();
						starting_time = readfile(0);
						restart_read_file();
					}

					init_states();
					for (size_t t = starting_time; t <= 100000000 && actives.size() >= 1 ; t++)
					//for (size_t t = 0; t <= 900 && actives.size() >= 1 ; t++)
					{
						//boost::print_graph(society);
						//std::cout << "t: " << t << '\n';
						if (graphT == from_file)
						{
							readfile(t);
						}
						Vertex vd;
						//std::cout << "bang: " << actives.size() << '\n';
						for (std::set<int>::iterator it=actives.begin(); it!=actives.end(); it++)
					  {
							vd = *it;
							//std::cout << "vd: "<< vd << '\n';
							//std::cout << "supply: "<< society[vd].supply() << '\n';
							if (society[vd].supply() != 1)
							{
								//std::cout << "num_vertices: " << num_vertices(society) << '\n';
								//std::cout << "infection time: " << t << '\n';
								//if(t == 0)

									//std::cout << "t " << t << '\n';
									//std::cout << "num_edges " << num_edges(society) << '\n';

								for ( Vertex vi : make_iterator_range( adjacent_vertices(vd, society) ) )
								{
									society[vi].turn_I( society[vd].supply() );
								}
							}
					  }
						for (std::set<int>::iterator it=actives.begin(); it!=actives.end(); it++)
						{
							vd = *it;
						}


						actives = {};
						for( Vertex vd : make_iterator_range( vertices(society) ) )
						{
							if(society[vd].update() != 1)
							{
								actives.insert(vd);
							}
						}
					}
					if(run % 200 == 0)
					{
						if(graphT == erdos)
							std::cout << "Erdos: " << "n: " << num_vertices(society) << ", p: " << p << ", q: " << q << ", r: " << r << ", run: " << run << std::endl;
						if(graphT == from_file)
							std::cout << "file: " << "n: " << num_vertices(society) << ", p: " << p << ", q: " << q << ", r: " << r << ", run: " << run << std::endl;
					}
					fout << cluster_size() << '\n';
				}
			}
		}
	}


	clock_t end = clock();
  double elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
	std::cout << "elapsed time: " << elapsed_secs << '\n';
}
