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

typedef enum { erdos = 1, grid = 2, grid3D = 3, from_file = 4} Graph_Type;
typedef enum { single = 1, coinfection = 2 } Disease_Type;
//Graph_Type graphT = from_file;
Graph_Type graphT = erdos;
Disease_Type disT = coinfection;
//Graph_Type graphT = grid;
///Graph_Type graphT = grid3D;

using namespace boost;
using std::cout;
using std::endl;
using std::vector;


std::ifstream  fin;
float r, p = 0.25, q = 1;
float percol_prob = 0;
std::set <int> actives={};
int runNum = 1000;
//int runNum = 200;
int last_time_step = 0;
bool file_ended = false;


//typedef enum { neither, dis_one, dis_two, both } State;

class Interaction
{
	public:
	int present = 1;
};


//typedef adjacency_list<listS, vecS, undirectedS, SIR> Network;
typedef adjacency_list<setS, vecS, undirectedS, SIR, Interaction> Network;
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
	actives = {};

	int seed = rand() % num_vertices(society);
	//Vertex v = vertex(seed, society);
	int seed_dis;
	if(disT == coinfection)
		seed_dis = 6;
	else if(disT == single)
		seed_dis = 2;

	society[seed].health *= seed_dis;
	society[seed].future *= seed_dis;

	actives.insert(seed);
	/*
	seed = rand() % num_vertices(society);
	actives.insert(seed);
	society[seed].health *= 3;
	society[seed].future *= 3;
	*/
	//society[v].health = 2;
	//society[v].future = 2;

	//std::cout << "seed: " << seed << '\n';
}

int cluster_size()
{
	int infect_cluster = 0;
	for( Vertex vd : make_iterator_range( vertices(society) ) )
	{
		if (society[vd].health != 1)
		//if (society[vd].health % 6 == 0 )
		{
			infect_cluster++;
		}
//		if (society[vd].health % 3 == 0)
			//std::cout << "alarm!" << '\n';
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

void cons_grid(int n)
{
	society.clear();
	int l = sqrt(n);
	for (size_t i = 0; i < n; i++)
	{
		int j = (i + 1) % n;
		add_edge(i, j, society);

		j = (i + l) % n;
		add_edge(i, j, society);
	}
}

void cons_grid3D(int n)
{
	society.clear();
	int l = cbrt(n);
	for (size_t i = 0; i < n; i++)
	{
		int j = (i + 1) % n;
		add_edge(i, j, society);

		j = (i + l) % n;
		add_edge(i, j, society);

		j = (i + l*l) % n;
		add_edge(i, j, society);
	}
}

void restart_read_file()
{
	file_ended = false;
  //std::cout << "rest!" << '\n';
  //fin.clear();
  fin.seekg(0, fin.beg);
  fin.close();
  //fin.open("input_matrix.txt");
	fin.open("clean_input_matrix.txt");
  if (!fin)
  {
    std::cerr << "Unable to open file datafile.txt";
    exit(1);   // call system to stop
  }
}

int readfile(int t)
{
	Edge_iter vi, vi_end, next;
	boost::tie(vi, vi_end) = edges(society);
	for (next = vi; vi != vi_end; vi = next)
	{
		++next;
			remove_edge(*vi, society);
	}
	if (file_ended) // if the file is ended, break the function.
	{
		std::cout << "file ended." << '\n';
		return 9999999;
	}
  std::string temp;
  int read_time, i, j;
  auto read_location = fin.tellg() ;


  for (size_t k = 0 ; !file_ended ; k++)
  {
		if(fin.eof())
		{
			file_ended = true;
			break;
		}
    read_location = fin.tellg() ;
    fin >> read_time;
    if (read_time > t)
		{
			break;
		}

    fin >> i ; fin >>j ;
		add_edge(i, j, society);
		//fin >> temp;
		//fin>> temp;
  }

  fin.clear();
  fin.seekg(read_location, fin.beg);
	return read_time;
}

int main()
{
	int starting_time = 0;
	clock_t begin = clock();
	std::ofstream fout;
	std::string file_name;
	fout.open("cdata.txt");

	//fout.open(file_name);
	if(disT == coinfection)
		fout<<"$Coinfection$\n";
	else if(disT == single)
		fout<<"$Single$\n";

	switch (graphT)
	{
		case erdos:
			fout<<"$Erdos$\n";
			break;
		case grid:
			fout<<"$grid$\n";
			break;
		case grid3D:
			fout<<"$3D_grid$\n";
			break;
		case from_file:
			fout<<"imported from file\n";
			break;
	}
	srand(time(0));
	//srand(0);
	//std::vector<int> n_set={128, 256, 512,1024, 2048, 4096, 8192, 16384};
	//std::vector<int> n_set={16384};
	std::vector<int> n_set={512};
	std::vector<float> p_set={0.1, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.6, 1};
	//std::vector<float> p_set={0.8, 0.9, 1};
	std::vector<float> q_set={0.1 ,0.5, 0.8, 1};
	std::vector<float> r_set={0.1 ,0.5, 0.8, 1};
	//n_set = {4};
	q_set={1};
	p_set={0.4, 0.42, 0.45, 0.47, 0.5, 0.52, 0.55, 0.58, 0.6, 0.7};
	p_set = {0.4, 0.5, 0.6};
	r_set={1};
	r = r_set[0];
	//write system properties to file, for later use in python.
	fout<<n_set.size()<<"\n";
	fout<<p_set.size()<<"\n";
	fout<<q_set.size()<<"\n";
	fout<<r_set.size()<<"\n";
	fout<<runNum<<"\n";


	for(int nindex=0; nindex<=n_set.size()-1; nindex++)
		fout<<n_set[nindex]<<"\n";
	for(int pindex=0; pindex<=p_set.size()-1; pindex++)
		fout<<p_set[pindex]<<"\n";
	for(int qindex=0; qindex<=q_set.size()-1; qindex++)
		fout<<q_set[qindex]<<"\n";
	for(int rindex=0; rindex<=r_set.size()-1; rindex++)
		fout<<r_set[rindex]<<"\n";

	for(int nindex=0; nindex<n_set.size(); nindex++)
	{
		vert_num = n_set[nindex];
		if (graphT == erdos)
		{
			cons_Erdos(vert_num);
		}
		else if (graphT == grid)
		{
			cons_grid(vert_num);
		}
		else if (graphT == grid3D)
		{
			cons_grid3D(vert_num);
		}


		for (size_t pindex = 0; pindex < p_set.size(); pindex++)
		{
				p = p_set[pindex];
			for (size_t qindex = 0; qindex < q_set.size(); qindex++)
			{
				q = q_set[qindex];
				//for now!
				//q = p;

				for (size_t run = 0; run < runNum; run++)
				{
					if (graphT == from_file)
					{
						restart_read_file();
						starting_time = readfile(0);
						restart_read_file();
					}

					init_states();
					for (size_t t = starting_time; t <= 100000000 && actives.size() >= 1 ; t+=200)
					//for (size_t t = 0; t <= 900 && actives.size() >= 1 ; t++)
					{
						if (graphT == from_file)
						{
							last_time_step = readfile(t);
						}
						Vertex vd;
						for (std::set<int>::iterator it=actives.begin(); it!=actives.end(); it++)
					  {
							vd = *it;
							//std::cout << "vd: "<< vd << '\n';
							//std::cout << "supply: "<< society[vd].supply() << '\n';
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
						{
							std::cout << "Erdos: " << "n: " << num_vertices(society) << ", p: " << p << ", q: " << q << ", r: " << r << ", run: " << run << std::endl;
						}
						else if(graphT == grid)
						{
							std::cout << "Grid: " << "n: " << num_vertices(society) << ", p: " << p << ", q: " << q << ", r: " << r << ", run: " << run << std::endl;
						}
						else if(graphT == grid3D)
						{
							std::cout << "3D Grid: " << "n: " << num_vertices(society) << ", p: " << p << ", q: " << q << ", r: " << r << ", run: " << run << std::endl;
						}
						else if(graphT == from_file)
						{
							std::cout << "file: " << "n: " << num_vertices(society) << ", p: " << p << ", q: " << q << ", r: " << r << ", run: " << run <<", last_time_step: " << last_time_step << '\n';
						}
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
