#include "global.h"
#include "Person.h"
#include "graph_base.h"
#include "output_utilities.h"
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

//enum Graph_Type { erdos = 1, grid = 2, grid3D = 3, from_file = 4};
enum Disease_Type { single = 1, coinfection = 2 } ;
enum Reshuffle { no_shuffle = 0, erdos_reshuffle = 1, grid_reshuffle = 2 } ;
//Reshuffle burst_reshuffle = grid_reshuffle;
const Reshuffle burst_reshuffle = no_shuffle;
const bool grid_output_on = false;
const bool timed_output_on = false;

//Graph_Type graphT = from_file;
const Graph_Type graphT = grid;
const Disease_Type disT = single;
//Graph_Type graphT = grid;
//Graph_Type graphT = grid3D;

using namespace boost;
using std::cout;
using std::endl;
using std::vector;

std::random_device RANDOM_SEED;
std::mt19937 generator( RANDOM_SEED() );

std::ifstream  fin;
float r, p = 0.25, q = 1;
float percol_prob = 0;
std::set <int> actives={};
int run, runNum = 100;
int time_step_size = 1;
//int ab_cluster, a_cluster, b_cluster, actives_num = 0;
//int runNum = 200;
int last_time_step = 0;
bool file_ended = false;
int read_time = 0, prev_read_time = 0; //used in readfile
//enum { neither, dis_one, dis_two, both } State;
Vertex_Num vert_num = 256;
Network society(0);

void init_states(int n)
{
	susceptible.population = n;
	infected_b.population = 0;
	recovered.population = 0;
	for( Vertex vd : make_iterator_range( vertices(society) ) )
	{
		society[vd].refresh();
	}
	actives = {};

	//Vertex v = vertex(seed, society);
	/*
	Transfer seed_dis;
	if(disT == coinfection)
		seed_dis = both;
	else if(disT == single)
		seed_dis = dis_one;
	*/
	int seed = rand() % num_vertices(society);
	actives.insert(seed);
	//society[seed].turn_I( seed_dis );
	//society[seed].set_seed(seed_dis);
	society[seed].setSeed( &infected_b );

}
/*
void cluster_size()
{
	a_cluster = 0;
	b_cluster = 0;
	ab_cluster = 0;
	//actives_cluster = 0;
	for( Vertex vd : make_iterator_range( vertices(society) ) )
	{
		if (society[vd].get_health() % 6 == 0)
			ab_cluster++;
		else if (society[vd].get_health() % 2 == 0)
		{
			a_cluster++;
		}
		else if (society[vd].get_health() % 3 == 0)
			b_cluster++;
	}
}
*/

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

int main()
{
	int starting_time = 0;
	clock_t begin = clock();
	std::ofstream fout;
	std::ofstream tout;
	//if we want an animation, one run is enough.

	if(grid_output_on)
		runNum = 1;

	std::vector<int> n_set={ 16384 };
	std::vector<float> p_set={0.1, 0.15, 0.17, 0.19, 0.2, 0.225, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.8, 0.9};
	//std::vector<float> p_set={0.8, 0.9, 1};
	std::vector<float> q_set={0.1 ,0.5, 0.8, 1};
	std::vector<float> r_set={0.1 ,0.5, 0.8, 1};
	//p_set={1};
	//p_set={0.25};
	//p_set={0};
	//p_set = {0.1, 0.12, 0.14, 0.16, 0.18, 0.2, 0.22, 0.24, 0.26, 0.28 ,0.30, 0.32, 0.34, 0.36, 0.38, 0.4};
	//p_set = {0.03, 0.04, 0.045, 0.05, 0.06, 0.07, 0.08};
	//p_set = {0.04 ,0.06, 0.08, 0.10, 0.12, 0.14, 0.16, 0.18, 0.20};
	//p_set = {0.080, 0.085, 0.09, 0.095, 0.1, 0.105};
	p_set = { 0.0975 };
	p_set = { 0.5 };
	//p_set = {0.0318};
	//p_set = {0.030, 0.035, 0.040, 0.0425, 0.045, 0.0475, 0.050};
	//p_set = { 0.0475 };

	//p_set = {0.0315, 0.0317, 0.0319, 0.0321, 0.0323, 0.0325, 0.0327, 0.0329, 0.0331, 0.0333, 0.0335, 0.0337, 0.0339};
	//p_set = { 0.0315, 0.0317, 0.0319 };
	//p_set = { 0.0321, 0.0323, 0.0325 };
	//p_set = { 0.0327, 0.0329 };


	//p_set = {0.02, 0.04, 0.06, 0.08, 0.1};
	//p_set = {0.3, 0.325, 0.35, 0.375, 0.4, 0.425, 0.45, 0.475, 0.5, 0.525, 0.55, 0.575, 0.6};
	//p_set = {0.3 ,0.325, 0.35, 0.375};
	//p_set = {0.15 ,0.175, 0.2, 0.25, 0.275};
	//p_set = {0.4 ,0.5, 0.6, 0.7, 0.8, 0.9};
	//p_set = {0.1, 0.15, 0.2};
	//p_set = {0.004, 0.005, 0.006, 0.007, 0.008, 0.009, 0.001};
	//p_set = {0.005, 0.0075,0.010, 0.0125,0.015, 0.0175,0.020};
	q_set = {0.4};
	q_set = {1};
	r_set={0.0001};
	r_set={0.1};
	r = r_set[0];
	std::string file_name = "temp-results/" ; //"cdatabg.txt"

	switch (graphT)
	{
		case erdos:
		fout<<"$Erdos$\n";
		file_name.append("Erdos, ");
		break;
		case grid:
		fout<<"$grid$\n";
		file_name.append("grid, ");
		break;
		case grid3D:
		fout<<"$3D-grid$\n";
		file_name.append("grid3D, ");
		break;
		case from_file:
		//fout<<"imported from file\n";
		fout<<"$Elementary$ $School$\n";
		file_name.append("file_data, ");
		break;
	}

	file_name.append( std::to_string( n_set[0] ) ); file_name.append(", ");
	file_name.append( std::to_string( begin ) );
	file_name.append("-data.txt");
	//fout.open("../Results/cdata.txt");
	fout.open(file_name);
	tout.open("../Results/grid_visualize.csv");
	//tout<< "something" << ", " <<'\n';
	//fout.open(file_name);
	if(disT == coinfection)
		fout<<"$Coinfection$\n";
	else if(disT == single)
		fout<<"$Single$\n";
	srand(time(0));
	//srand(0);
	//std::vector<int> n_set={128, 256, 512,1024, 2048, 4096, 8192, 16384};
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

				for (run = 0; run < runNum; run++)
				{
					if (graphT == from_file)
					{
						time_step_size = 1;
						restart_read_file();
						starting_time = readfile(0);
						//starting_time = 0;
						restart_read_file();
					}

					init_states(n_set[nindex]);

					//for (size_t t = starting_time; t <= 100000000 && actives.size() >= 1 ; t += time_step_size)
					//for (size_t t = starting_time; t <= 100	 && actives.size() >= 1; t += time_step_size)
					for (size_t t = starting_time; t <= 40000	 && actives.size() >= 1 && infected_b.getPopulation() >= 1; t += time_step_size)
					{
						//emergence of the second disease
						//if(t == 20)
							//society[0].set_seed(dis_two);
						if(grid_output_on)
							grid_output(vert_num, tout);

						if(timed_output_on)
							//terminal_output(graphT, run, last_time_step);
						//std::cout << "active num: " << actives_num << '\n';
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
							//if (society[vd].supply() != neither)
							if ( society[vd].state->isInfector() )
							{
								for ( Vertex vi : make_iterator_range( adjacent_vertices(vd, society) ) )
								{
									//society[vi].turn_I( society[vd].supply() );
									society[vi].interact( society[vd] );
								}
							}
					  }
						//std::cout << actives.size() << '\n';
						actives = {};
						for( Vertex vd : make_iterator_range( vertices(society) ) )
						{
							society[vd]++;
							//if(society[vd].update() != 1)
							/*
							std::cout << "vd: " << vd << '\n';
							society[vd].print_person();
							std::cout << "after ++: " << vd;
							society[vd].print_person();
							std::cout << "after update: " << vd;
							society[vd].print_person();
							std::cout << '\n';
							*/
							//if ( society[vd].isInfector() )
							if(society[vd].update())
							{
								actives.insert(vd);
							}
						}
					}

					//if(actives_num >= 1)
					//{
						//std::cout << "we have a problem here:" << actives_num << '\n';
					//}

					if(grid_output_on)
						grid_output(vert_num, tout);
					if(run % 10 == 0)
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

						terminal_output(graphT, run, last_time_step);
						//std::cout << "active num: " << actives_num << '\n';
						cout << susceptible.population << ", ";
						cout << infected_a.population << ", ";
						cout << infected_b.population << ", ";
						cout << recovered.population << ", ";
						cout << infected_ab.population << '\n';

					}
					//cluster_size();
					//fout << ab_cluster << '\n';
					fout << 0 << ", ";
					fout << 0 << ", ";
					fout << recovered.population << '\n';
					//fout << ab_cluster;
					//fout <<", " << b_cluster << '\n';
					//cout << susceptible.population << ", ";
					//cout << infected_b.population << ", ";
					//cout << recovered.population << '\n';
				}
			}
		}
	}

	clock_t end = clock();
  double elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
	std::cout << "elapsed time: " << elapsed_secs << '\n';
}
