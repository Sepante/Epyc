//#include "global.h"
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
#include <random>

#include <sstream> //because of the old compiler, which doesn't have to_string(float)
//#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/graph_utility.hpp>
//#include <boost/graph/properties.hpp>
//#include <boost/config.hpp>
//#include <boost/graph/connected_components.hpp>

//std::string inputAddress = "../Graph_data/network data/shuffled/DCB/";
std::string inputAddress = "../Graph_data/network data/clean/";
//std::string inputAddress = "../Graph_data/network data/agg/";


std::string inputFileName = "clean sociopattern_hospital.txt";
//std::string inputFileName = "DCB-sh giant clean brazil.txt";
//std::string inputFileName = "agg giant clean primaryschool.txt";

int seed;
//enum Graph_Type { erdos = 1, grid = 2, grid3D = 3, from_file = 4};
bool manual_cooperativity_input = false;
bool cooperate = true;
enum Disease_Type { single = 1, coinfection = 2 } ;
enum Reshuffle { no_shuffle = 0, erdos_reshuffle = 1, grid_reshuffle = 2 } ;
//Reshuffle burst_reshuffle = grid_reshuffle;
const Reshuffle burst_reshuffle = no_shuffle;
const bool grid_output_on = false;
const bool timed_output_on = false;
const bool manual_user_input = false;
const bool manual_file_input = false;
const bool manual_step_size_input = false;
SamplingAlgorithm algorithm = SamplingAlgorithm::halfGillespie;
//SamplingAlgorithm algorithm = SamplingAlgorithm::RejectionSample;

//const Graph_Type graphT = from_file;
const Disease_Type disT = coinfection;

//Graph_Type graphT = static_from_file;
Graph_Type graphT = from_file;

const int row_count = 0;
int edge_num;
const int column_count = 3;
std::vector<std::vector<int> > temporal_graph(row_count, std::vector<int>(column_count, 0));
std::ifstream fin;
bool interactionsRemaining = 1;


using namespace boost;
using std::cout;
using std::endl;
using std::vector;

//std::ifstream  fin;
float r, p = 0.25, q = 1;
float percol_prob = 0;
std::set <int> actives={};
int run, runNum = 1;

int time_step_size = 1; //for the hospital, it has been held = 20 by others.//for brazil, it's 1.//for email: 40 //for FilmMessages: 5000
int ab_cluster, a_cluster, b_cluster;
int last_time_step = 0;
bool file_ended = false;
int read_time = 0, prev_read_time = 0; //used in readfile
//enum { neither, dis_one, dis_two, both } State;
Vertex_Num vert_num = 1;
Network society(0);

void init_states()
{

	//for( Vertex vd : make_iterator_range( vertices(society) ) )
	for (size_t vd = 0; vd < vert_num; vd++) //for hpc tailored version
	{
		society[vd].refresh();
	}
	actives = {};

	//Vertex v = vertex(seed, society);
	Transfer seed_dis;
	if(disT == coinfection)
		seed_dis = both;
	else if(disT == single)
		seed_dis = dis_one;

	//int seed = rand() % num_vertices(society);
	seed = rand() % num_vertices(society);
	//seed = 2;
	actives.insert(seed);

	//society[seed].set_seed(seed_dis);

  society[ 2 ].set_seed(seed_dis);

}

void cluster_size()
{
	a_cluster = 0;
	b_cluster = 0;
	ab_cluster = 0;
	//for( Vertex vd : make_iterator_range( vertices(society) ) )
	for (size_t vd = 0; vd < vert_num; vd++) //for hpc tailored version
	{
		if (society[vd].get_health() % 6 == 0)
			ab_cluster++;
		else if (society[vd].get_health() % 2 == 0)
			a_cluster++;
		else if (society[vd].get_health() % 3 == 0)
			b_cluster++;
	}
}

int cons_static()
{

  fin.open( inputAddress + inputFileName);
  if (!fin)
  {
		//std::cout << inputAddress << '\n';
    std::cerr << "Unable to open static graph file" << inputAddress + inputFileName <<"\n";
    exit(1);   // call system to stop
  }

	std::string infoFileName = "info " + inputFileName ;

	std::ifstream infoin;
	infoin.open( inputAddress + infoFileName );
	if (!infoin)
	{
		std::cerr << "Unable to open info file"<<"\n";
		exit(1);   // call system to stop
	}

  edge_num = std::count(std::istreambuf_iterator<char>(fin), std::istreambuf_iterator<char>(), '\n');

  //temporal_graph.resize(edge_num, std::vector<int>(3));
  std::cout << "edge_num: " << edge_num << '\n';
  fin.seekg(0, fin.beg); //get back to the begining of the file, after count.
  std::string temp;
  infoin >> temp;

  infoin >> vert_num;
  std::cout << "vert_num: " << vert_num << '\n';
	infoin.close();
	int i,j;
  for (size_t edge = 0; edge < edge_num; edge++)
  {
    fin >> i ; fin >> j;
		//std::cout << i << ", " << j << '\n';
		add_edge(i, j, society);
  }
	//std::cout << "edge num = " << edge_num << '\n';
	fin.close();
	//print_graph(society);

	return vert_num; //for writing attributes to the system.
}


int readFile(int t)
{

  fin.open( inputAddress + inputFileName);
  if (!fin)
  {
		//std::cout << inputAddress << '\n';
    std::cerr << "Unable to open graph file" << inputAddress + inputFileName <<"\n";
    exit(1);   // call system to stop
  }

	std::string infoFileName = "info " + inputFileName ;


	std::ifstream infoin;
	infoin.open( inputAddress + infoFileName );
	if (!infoin)
	{
		std::cerr << "Unable to open info file"<<"\n";
		exit(1);   // call system to stop
	}

  edge_num = std::count(std::istreambuf_iterator<char>(fin), std::istreambuf_iterator<char>(), '\n');

  temporal_graph.resize(edge_num, std::vector<int>(3));
  std::cout << "edge_num: " << edge_num << '\n';
  fin.seekg(0, fin.beg); //get back to the begining of the file, after count.
  std::string temp;
  infoin >> temp;

  infoin >> vert_num;
  std::cout << "vert_num: " << vert_num << '\n';
	infoin.close();

  for (size_t edge = 0; edge < edge_num; edge++)
  {
    fin >> temporal_graph[edge][0] ; fin >> temporal_graph[edge][1] ; fin >> temporal_graph[edge][2];
		//std::cout << temporal_graph[edge][1] <<", " << temporal_graph[edge][2] << '\n';
  }
	fin.close();
	add_edge( vert_num-1, vert_num-2, society ); // for now! (temp) an ugly way to add all required vertices.
																							 // since we don't use the edges of the graph, it doesn't affect our problem.

	return vert_num; //for writing attributes to the system.
}

int FlashForward(int seed) //jumps in time, in order to get to the time, which the seed appears for the first time
										//so we don't lose time waiting for it.
										//((currently only for 1 seed))
{
	std::cout << "seed: " << seed << '\n';
	//auto edgeNum = temporal_graph. ;
	for (size_t edget = 0; edget < temporal_graph.size(); edget++)
	{
		if( temporal_graph[ edget ][1] == seed || temporal_graph[ edget ][2] == seed )
		{
			//std::cout << temporal_graph[ edget ][0] << '\n';
			return temporal_graph[ edget ][0];
		}
	}
	std::cout << "alarm! seed node wasn't even in the graph data." << '\n';
}

//because of the old compiler, which doesn't have to_string(float)
namespace patch
{
	template < typename T > std::string to_string( const T& n )
	{
			std::ostringstream stm ;
			stm << n ;
			return stm.str() ;
	}
}


int main()
{
	//Person::initialize(0.1);
	//std::vector<int> n_set={128, 256, 512,1024, 2048, 4096, 8192, 16384};
	std::vector<int> n_set={0};
	std::vector<float> p_set={0.1, 0.15, 0.17, 0.19, 0.2, 0.225, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.8, 0.9};
	//std::vector<float> p_set={0.8, 0.9, 1};
	std::vector<float> q_set={0.1 ,0.5, 0.8, 1};
	std::vector<float> r_set={0.1 ,0.5, 0.8, 1};

	//p_set={1};
	//p_set={0.25};
	//p_set={0};
	//p_set = {0.1, 0.12, 0.14, 0.16, 0.18, 0.2, 0.22, 0.24, 0.26, 0.28 ,0.30, 0.32, 0.34, 0.36, 0.38, 0.4};
	//p_set = {0.2, 0.3, 0.35, 0.4, 0.45, 0.5	};
	//p_set = {0.3, 0.325, 0.35, 0.375, 0.4, 0.425, 0.45, 0.475, 0.5, 0.525, 0.55, 0.575, 0.6};
	//p_set = {0.3 ,0.325, 0.35, 0.375};
	//p_set = {0.15 ,0.175, 0.2, 0.25, 0.275};
	//p_set = {0.4 ,0.5, 0.6, 0.7, 0.8, 0.9};
	//p_set = {0.1, 0.15, 0.2};
	//p_set = {0.004, 0.005, 0.006, 0.007, 0.008, 0.009, 0.001};
	//p_set = {0.005, 0.0075,0.010, 0.0125,0.015, 0.0175,0.020};
	//p_set = {0.005, 0.010 ,0.015 ,0.020 ,0.025 ,0.03};
	//p_set = { 0.01    , 0.011875, 0.01375 , 0.015625, 0.0175  , 0.019375, 0.02125 , 0.023125, 0.025 };
	//p_set = {0.1 , 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3 , 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4
	//, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49};
	//p_set = { 0.1 , 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21 };
	//p_set = { 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3 , 0.31 };
	//p_set = { 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4 };
	//		p_set = { 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49 };

	//p_set = {0.0015, 0.0020 , 0.0025}; //sociopattern_hospital
	//p_set = {0.010, 0.0125, 0.015, 0.0175, 0.020, 0.0225, 0.025, 0.0275, 0.030};
	//p_set = {0.0325, 0.035, 0.0375, 0.040, 0.0425, 0.045, 0.0475, 0.050, 0.0525};
	//p_set = { 0.055, 0.0575, 0.060, 0.0625, 0.065, 0.0675, 0.070 };
	//p_set = {0.01, 0.02, 0.03, 0.04, 0.050, 0.06, 0.07 };
	//p_set = {0.0675,0.07	};
	//p_set = {0.01,0.0125,0.015,0.0175,0.02,0.0225,0.025,0.0275,0.03,0.0325,0.035,0.0375,0.04,0.0425,0.045,0.0475};
	//p_set = {0.05,0.0525,0.055,0.0575, 0.06,0.0625,0.065,0.0675,0.07 };
	//p_set = { 0.0875 };
	//p_set = {0.000625, 0.00125 , 0.001875, 0.0025  , 0.003125,
    //   0.00375 , 0.004375, 0.005   , 0.005625, 0.00625 , 0.006875,
      // 0.0075  , 0.008125, 0.00875 , 0.009375, 0.01};
	p_set = {1};
	//p_set = { 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07 };
	q_set = {1};
	//r_set={0.0005};
	//r_set={0.0002};
	/*

	r_set={1};

	r = r_set[0];
	if(manual_cooperativity_input)
	{
		std::cout << "set the cooperativity boolean value" << '\n';
		std::cin >> cooperate;
	}
	if(manual_user_input)
	{
		std::cout << "enter a value for p:" << '\n';
		std::cin>>p_set[0];
		std::cout << "enter a value for r:" << '\n';
		std::cin>>r_set[0];
		r = r_set[0];
		std::cout << "enter a value for number of runs:" << '\n';
		std::cin>>runNum;
	}
	if (manual_file_input)
	{
		inputAddress = "";
		inputFileName = "";
		std::cout << "enter network file address:" << '\n';
		std::cin.ignore();
		std::getline(std::cin, inputAddress);
		std::cout << "enter network file title:" << '\n';
		//std::cin.ignore();
		getline(std::cin, inputFileName);
		std::cout << inputAddress << '\n';
		std::cout << inputFileName << '\n';
		//std::cin.getline( inputFileName, 100 );
	}
	if (manual_step_size_input)
	{
		std::cout << "enter the step size: ";
		std::cin >> time_step_size;
	}



	std::random_device rd;
	//std::cout << "rd: "<<rd() << '\n';
	//srand(rd());
	int randSeed;
	std::cin >> randSeed;
	srand(randSeed);
	int starting_time = 0;
	clock_t begin = clock();
	std::ofstream fout;
	std::ofstream tout;
	//if we want an animation, one run is enough.
	if(grid_output_on)
		runNum = 1;
	std::string outputFileAddress = "../Results/";
	std::string outputFileName = inputFileName;

	if(!cooperate)
		outputFileName = outputFileName + " non-coop";
	std::string graphType;
	//fout.open("../Results/cdata.txt");
	switch (graphT)
	{
		case erdos:
		graphType = "Erdos";
		//file_name.append("Erdos, ");
		break;
		case grid:
		graphType = "grid";
		//file_name.append("grid, ");
		break;
		case grid3D:
		//fout<<"$3D-grid$\n";
		graphType = "grid3D";
		//file_name.append("grid3D, ");
		break;
		case from_file:
		case static_from_file:
		graphType = inputFileName;
		//fout<<"imported from file\n";
		//fout<<file_name;
		//file_name.append(input_file_name);
		break;
	}
	auto randcode = rand();
	auto randlong = (long long int) randcode;
	//std::cout << "randcode: " << randcode << '\n';
	//std::cout << "randlong: " << randlong << '\n';
	std::string coopOrNot = "";
	if(!cooperate)
		coopOrNot = " non-coop ";
	fout.open( outputFileAddress + graphType + " " + coopOrNot + patch::to_string( p_set[0] ) + " " + std::to_string( randlong ) + "-data.txt" );
	//fout.open( outputFileAddress + graphType + " " + "-data.txt" );
	if(disT == coinfection)
		fout<<"$Coinfection$\n";
	else if(disT == single)
		fout<<"$Single$\n";

	fout << '$' << graphType << '$' << '\n';
	if(grid_output_on)
		tout.open("../Results/grid_visualize.csv");

	//srand(0);

	//write system properties to file, for later use in python.
	fout<<n_set.size()<<"\n";
	fout<<p_set.size()<<"\n";
	fout<<q_set.size()<<"\n";
	fout<<r_set.size()<<"\n";
	fout<<runNum<<"\n";


	//for(int nindex=0; nindex<n_set.size(); nindex++)
      n_set[0] = readFile(0);
				if(true)
				{
					init_states();

					if( graphT == from_file )
					//else if (false)
					{
						int edge = 0;

						for (size_t t = starting_time; t < 2; t += time_step_size)
						{

							std::cout << "t: " << t << '\n';
							//for (edge; temporal_graph[edge][0] <= t < edge_num; edge++)
							int passedLoops = 0;
							while (  temporal_graph[ edge % edge_num ][0] + passedLoops * temporal_graph[ edge_num - 1 ][0] <= t )
							{
								edge++ ;
								if( edge > edge_num )
									passedLoops ++ ;
								//society[ temporal_graph[ edge % edge_num ][1] ].turn_I( society[ temporal_graph[ edge % edge_num ][2] ].supply(), t );
								//std::cout << "node 1: " << temporal_graph[ edge % edge_num ][1] << '\n';
								//std::cout << "node 2: " << temporal_graph[ edge % edge_num ][2] << '\n';
								society[ temporal_graph[ edge % edge_num ][2] ].turn_I( society[ temporal_graph[ edge % edge_num ][1] ].supply(), t );

							}


						}
					}

				}
				*/

				//patch::exponent.param(std::exponential_distribution<float>::param_type(1 / 100.0));
				//std::cout << exponent( gen ) << '\n';
				//for (size_t i = 0; i < 10; i++) {
//					std::cout << exponent( gen ) << '\n';
				//}
				std::random_device randomSeed;

}
