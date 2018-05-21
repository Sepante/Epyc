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

enum Graph_Type { erdos = 1, grid = 2, grid3D = 3, from_file = 4};
enum Disease_Type { single = 1, coinfection = 2 } ;
enum Reshuffle { none = 0, erdos_reshuffle = 1, grid_reshuffle = 2 } ;
//Reshuffle burst_reshuffle = grid_reshuffle;
Reshuffle burst_reshuffle = none;
const bool grid_output_on = false;
bool timed_output_on = false;

//Graph_Type graphT = from_file;
Graph_Type graphT = erdos;
Disease_Type disT = coinfection;
//Graph_Type graphT = grid;
//Graph_Type graphT = grid3D;

using namespace boost;
using std::cout;
using std::endl;
using std::vector;


std::ifstream  fin;
float r, p = 0.25, q = 1;
float percol_prob = 0;
std::set <int> actives={};
int runNum = 5000;
int time_step_size = 1;
int ab_cluster, a_cluster, b_cluster;
//int runNum = 200;
int last_time_step = 0;
bool file_ended = false;
int read_time = 0, prev_read_time = 0; //used in readfile


//typedef enum { neither, dis_one, dis_two, both } State;
/*
class Interaction
{
	public:
	int present = 1;
};
*/

//typedef adjacency_list<setS, vecS, undirectedS, SIR, Interaction> Network;
typedef adjacency_list<listS, vecS, undirectedS, SIR> Network;
typedef graph_traits<Network>::edges_size_type Edge_Num;
typedef graph_traits<Network>::vertices_size_type Vertex_Num;
typedef graph_traits<Network>::vertex_iterator Vertex_iter;
typedef graph_traits<Network>::vertex_descriptor Vertex;
typedef graph_traits<Network>::edge_descriptor Edge;
typedef graph_traits<Network>::edge_iterator Edge_iter;

Vertex_Num vert_num = 256;


Network society(3);

void init_states()
{

	for( Vertex vd : make_iterator_range( vertices(society) ) )
	{
		society[vd].refresh();
	}
	actives = {};

	//Vertex v = vertex(seed, society);
	int seed_dis;
	if(disT == coinfection)
		seed_dis = 6;
	else if(disT == single)
		seed_dis = 2;

	int seed = rand() % num_vertices(society);
	actives.insert(seed);
	//society[seed].health *= seed_dis;
	//society[seed].future *= seed_dis;
	society[seed].set_health( society[seed].get_health() * seed_dis );
	society[seed].set_future( society[seed].get_future() * seed_dis );

/*
	//seed = rand() % num_vertices(society);
	seed = (seed + 1) % num_vertices(society);
	actives.insert(seed);
	society[seed].health *= seed_dis;
	society[seed].future *= seed_dis;
*/
	//society[v].health = 2;
	//society[v].future = 2;

	//std::cout << "seed: " << seed << '\n';
}

void cluster_size()
{
	a_cluster = 0;
	b_cluster = 0;
	ab_cluster = 0;
	for( Vertex vd : make_iterator_range( vertices(society) ) )
	{
		/*
		if (society[vd].health != 1)
		{
			ab_cluster++;
		if (society[vd].health % 2 == 0 )
			a_cluster++;
		if (society[vd].health % 3 == 0 )
			b_cluster++;
		}
		*/

		if (society[vd].get_health() % 6 == 0)
			ab_cluster++;
		else if (society[vd].get_health() % 2 == 0)
			a_cluster++;
		else if (society[vd].get_health() % 3 == 0)
			b_cluster++;
	}
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

void grid_output(int n, std::ofstream& tout)
{
	int l = sqrt(n);
	for (size_t i = 0; i < l; i++)
	{
		for (size_t j = 0; j < l; j++)
		{
			tout << society[i*l + j].get_health();
			if(j == l-1)
				break;
			tout << ", ";
		}
		tout << "\n";
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
	read_time = 0, prev_read_time = 0;
	file_ended = false;
  //std::cout << "rest!" << '\n';
  //fin.clear();
  fin.seekg(0, fin.beg);
  fin.close();
  //fin.open("input_matrix.txt");
	//fin.open("../Graph_data/clean_input_matrix.txt");
	fin.open("../Graph_data/burst_creator/burst_graph.txt");
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
  int i, j;
  auto read_location = fin.tellg() ;


  for (size_t k = 0 ; !file_ended ; k++)
  {
		if(fin.eof())
		{
			file_ended = true;
			break;
		}
    read_location = fin.tellg() ;

		if(read_time <= t)
		{
			prev_read_time = read_time;
		}

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
	return (prev_read_time);
}

void get_out_put()
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
	//cluster_size();
	//cout << (a_cluster + b_cluster + ab_cluster) << '\n';
}


int main()
{
	int starting_time = 0;
	clock_t begin = clock();
	std::ofstream fout;
	std::ofstream tout;
	//if we want an animation, one run is enough.
	if(grid_output_on)
		runNum = 1;
	std::string file_name;
	//fout.open("../Results/cdata.txt");
	fout.open("../Results/cdatab.txt");
	tout.open("../Results/grid_visualize.csv");
	//tout<< "something" << ", " <<'\n';
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
			//fout<<"imported from file\n";
			fout<<"$Elementary$ $School$\n";
			break;
	}
	srand(time(0));
	//srand(0);
		//std::vector<int> n_set={128, 256, 512,1024, 2048, 4096, 8192, 16384};
	//std::vector<int> n_set={16384};
	std::vector<int> n_set={1024};
	std::vector<float> p_set={0.1, 0.15, 0.17, 0.19, 0.2, 0.225, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.8, 0.9};
	//std::vector<float> p_set={0.8, 0.9, 1};
	std::vector<float> q_set={0.1 ,0.5, 0.8, 1};
	std::vector<float> r_set={0.1 ,0.5, 0.8, 1};
	p_set={1};
	//p_set={0.25};
	//p_set = {0.1, 0.12, 0.14, 0.16, 0.18, 0.2, 0.22, 0.24, 0.26, 0.28 ,0.30, 0.32, 0.34, 0.36, 0.38, 0.4};
	p_set={0.01, 0.02, 0.03, 0.035, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10};
	//p_set = {0.3, 0.35, 0.4, 0.45, 0.5	};
	q_set = {1};
	//r_set = {1};
	//p_set = {0.1, 0.2,0.3,0.4};
	r_set={0.0001};
	//r_set={1};
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

		fout<<"ab_cluster, a_cluster, b_cluster"<<'\n';

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
						time_step_size = 1;
						restart_read_file();
						starting_time = readfile(0);
						//starting_time = 0;
						restart_read_file();
					}

					init_states();
					for (size_t t = starting_time; t <= 100000000 && actives.size() >= 1 ; t += time_step_size)
					//for (size_t t = 0; t <= 900 && actives.size() >= 1 ; t++)
					{
						if(grid_output_on)
							grid_output(vert_num, tout);

						if(timed_output_on)
							get_out_put();

						if (graphT == from_file)
						{
							last_time_step = readfile(t);
						}

						//print_graph(society);

						Vertex vd;
						for (std::set<int>::iterator it=actives.begin(); it!=actives.end(); it++)
					  {
							vd = *it;
							//std::cout << "vd: "<< vd << '\n';
							//std::cout << "supply: "<< society[vd].supply() << '\n';
							if (society[vd].supply() != neither)
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
					if(grid_output_on)
						grid_output(vert_num, tout);
					if(run % 1000 == 0)
					{
						//temporal!!!!
						if (burst_reshuffle == grid_reshuffle)
						{
							system("./grid_shuffle.sh");
						}
						else if (burst_reshuffle == erdos_reshuffle)
						{
							system("./erdos_shuffle.sh");
						}

						get_out_put();
///////////////////////
					}
					cluster_size();
					//fout << ab_cluster << '\n';
					fout << ab_cluster;
					fout <<", " << a_cluster;
					fout <<", " << b_cluster << '\n';
				}
			}
		}
	}


	clock_t end = clock();
  double elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
	std::cout << "elapsed time: " << elapsed_secs << '\n';
}
