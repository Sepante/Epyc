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

//std::string inputAddress = "../Graph_data/network data/shuffled/DCW/";
//std::string inputAddress = "../Graph_data/network data/shuffled/DCWB/";
//std::string inputAddress = "../Graph_data/network data/shuffled/SO/";
std::string inputAddress = "../Graph_data/network data/shuffled/SOU/";
//std::string inputAddress = "../Graph_data/network data/giant/";
//std::string inputAddress = "../Graph_data/network data/clean/";
//std::string inputAddress = "../Graph_data/network data/agg/";

//std::string inputFileName = "clean sociopattern_conference_contact.txt";
//std::string inputFileName = "clean sociopattern_hospital.txt";
//std::string inputFileName = "SO-sh giant clean primaryschool.txt";
std::string inputFileName = "SOU-sh giant clean primaryschool.txt";
//std::string inputFileName = "DCWB-sh giant clean primaryschool.txt";
//std::string inputFileName = "DCW-sh giant clean primaryschool.txt";
//std::string inputFileName = "agg giant clean primaryschool.txt";
//std::string inputFileName = "agg clean sociopattern_hospital.txt";
//std::string inputFileName = "clean sociopattern_conference_contact.txt";
//std::string inputFileName = "clean sociopattern_hospital.txt";
//std::string inputFileName = "giant clean primaryschool.txt";
//std::string inputFileName = "giant clean brazil.txt";

int seed;
//distr.param(std::uniform_int_distribution<int>::param_type(5, 13));
//enum Graph_Type { erdos = 1, grid = 2, grid3D = 3, from_file = 4};
const bool manual_cooperativity_input = false;
bool cooperate = true;
enum Disease_Type { single = 1, coinfection = 2 } ;
enum Reshuffle { no_shuffle = 0, erdos_reshuffle = 1, grid_reshuffle = 2 } ;
//Reshuffle burst_reshuffle = grid_reshuffle;
const Reshuffle burst_reshuffle = no_shuffle;
const bool grid_output_on = false;
const bool timed_output_on = true;
const bool manual_user_input = true;
const bool manual_file_input = false;
const bool manual_step_size_input = false;

const bool seed_farming = false; //to loop over different values of initial diseased node.
const bool output_seed_num = false;

const bool temporal_periodic_boundary_condition = true;
int maxPassedLoops = 1000;

SamplingAlgorithm algorithm = SamplingAlgorithm::RejectionSample;
//SamplingAlgorithm algorithm = SamplingAlgorithm::halfGillespie;
int last_time;
long double last_time_mean = 0;
int last_time_max, last_time_min = 9999;
//const Graph_Type graphT = from_file;
const Disease_Type disT = coinfection;

//Graph_Type graphT = static_from_file;
//Graph_Type graphT = from_file;
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

const //std::ifstream  fin;
int seedsNum = 1;
float r, p = 0.25, q = 1;
float rambda;
float percol_prob = 0;
std::set <int> actives={};
//int run, runNum = 1;
int run, runNum = 10;

int time_step_size = 20; //for the hospital, it has been held = 20 by others.//for brazil, it's 1.//for email: 40 //for FilmMessages: 5000
//int time_step_size = 1; //for the hospital, it has been held = 20 by others.//for brazil, it's 1.//for email: 40 //for FilmMessages: 5000
int ab_cluster, a_cluster, b_cluster;
int AB_cluster, A_cluster, B_cluster;
int last_time_step = 0;
bool file_ended = false;
int read_time = 0, prev_read_time = 0; //used in readfile
//enum { neither, dis_one, dis_two, both } State;
Vertex_Num vert_num = 1;
Network society(0);

void init_states(int seedsNum)
{
	//std::cout << "our seed is : " <<seed << '\n';

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

	if(!seed_farming)
		seed = rand() % num_vertices(society);

	for( size_t i = 0; i < seedsNum; i++ )
	{
		seed = rand() % num_vertices(society);
		//seed = 0;

		actives.insert(seed);
		society[seed].set_seed(seed_dis);
	}
  //society[ 2 ].set_seed(seed_dis);
}

void cluster_size() //has to be removed in favor of an online counting
{
	a_cluster = 0;
	b_cluster = 0;
	ab_cluster = 0;

	A_cluster = 0;
	B_cluster = 0;
	AB_cluster = 0;
	//for( Vertex vd : make_iterator_range( vertices(society) ) )
	for (size_t vd = 0; vd < vert_num; vd++) //for hpc tailored version
	{
		if (society[vd].get_health() % 6 == 0)
		{
			ab_cluster++;
			if (society[vd].get_health() == 6)
				AB_cluster++;
			else
			{
				if (society[vd].get_health() % 4 != 0)
				{
					A_cluster++;
				}
				if (society[vd].get_health() % 9 != 0)
				{
					B_cluster++;
				}
			}

		}

		else if (society[vd].get_health() % 2 == 0)
		{
			a_cluster++;
			if (society[vd].get_health() % 4 != 0)
			{
				A_cluster++;
			}
		}
		else if (society[vd].get_health() % 3 == 0)
		{
			b_cluster++;
			if (society[vd].get_health() % 9 != 0)
			{
				B_cluster++;
			}

		}
	}
}

void simple_output(std::ofstream &fileobj, bool fullresults,bool output_seed_num = false, int tseed = 0)
{
	if(output_seed_num)
	{
		//std::cout << "yeah" << '\n';
		fileobj << tseed << ", ";
	}
	cluster_size();
	fileobj << ab_cluster;
	fileobj <<", " << a_cluster;
	fileobj <<", " << b_cluster;

	if(fullresults)
	{
		fileobj <<", " << AB_cluster;
		fileobj <<", " << A_cluster;
		fileobj <<", " << B_cluster;
	}
	fileobj << '\n';
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
	//std::cout << "seed: " << seed << '\n';
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
	//std::vector<int> x(10);
	//std::iota(std::begin(x), std::end(x), 0); //0 is the starting number
	//for( Vertex vd : make_iterator_range( x ) )
		//std::cout << vd << '\n';

	//std::cout << "number of seeds: " << seedsNum << '\n';

	//std::vector<int> n_set={128, 256, 512,1024, 2048, 4096, 8192, 16384};
	std::vector<int> n_set={75};
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
	p_set = {0.145}; //primaryschool
	//p_set = {0.325}; //brazil
	//p_set = {0.00001}; agg conference
	//r_set = {0.001};//hospital
	//p_set = {0.06}; //hospital
	//p_set = { , 0.0005, 0.0006, 0.0007, 0.0008, 0.0009, 0.001 };
	//p_set = {0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09};
	//p_set = {0.01};
	q_set = {1};
	r_set = {1};
	//p_set = {0.00001, 0.000012, 0.000014, 0.000016, 0.000018, 0.000020, 0.000022, 0.000024, 0.000026, 0.000028, 0.000030, 0.000032, 0.000034, 0.000036, 0.000038, 0.000040};
	//r_set={0.0005};
	r = r_set[0];
	rambda =  (r /  time_step_size );
	rambda = 0.001 / 20.0;
	//Person::initialize( rambda );
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
		//std::cout << "/* message */"<< '\n' << '\n'<< '\n'<< '\n'<< '\n'<< '\n';
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
	srand(rd());
	//srand(0);
	int starting_time = 0;
	clock_t begin = clock();
	std::ofstream fout;
	std::ofstream animout;
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
		animout.open("../Results/grid_visualize.csv");

	if(timed_output_on)
	{
		tout.open("../Results/" + std::to_string( randlong ) + " timed-data.txt");
		tout << "run,t,ab,a,b,AB,A,B" << '\n';
	}
		//srand(0);

	//write system properties to file, for later use in python.
	fout<<n_set.size()<<"\n";
	fout<<p_set.size()<<"\n";
	fout<<q_set.size()<<"\n";
	fout<<r_set.size()<<"\n";
	fout<<runNum<<"\n";


	//for(int nindex=0; nindex<n_set.size(); nindex++)
	int nindex = 0;
	vert_num = readFile(0);
	//std::cout << "vert_num: " << vert_num << '\n';
	//for(seed = 0 ; seed <= vert_num - 1; seed ++)
	{
		//std::cout << "who's counting me?" << '\n';
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
    else if (graphT == from_file)
    {
      n_set[0] = readFile(0);
      Person::demanderNum = vert_num;
    }
		else if( graphT == static_from_file )
		{
			n_set[0] = cons_static();
			vert_num = n_set[0];
			Person::demanderNum = vert_num;
			//std::cout << "dd: " << Person::demanderNum << '\n';
		}

		//if(seed == 0 )//freaking temporal
		{
		for(int nindex=0; nindex<=n_set.size()-1; nindex++)
		fout<<n_set[nindex]<<"\n";
		for(int pindex=0; pindex<=p_set.size()-1; pindex++)
		fout<<p_set[pindex]<<"\n";
		for(int qindex=0; qindex<=q_set.size()-1; qindex++)
		fout<<q_set[qindex]<<"\n";
		for(int rindex=0; rindex<=r_set.size()-1; rindex++)
		fout<<r_set[rindex]<<"\n";

		if(output_seed_num)
		{
			fout<<"seed, ";
		}

		fout<<"ab_cluster, a_cluster, b_cluster"<<'\n';
		}
		for (size_t pindex = 0; pindex < p_set.size(); pindex++)
		{
			p = p_set[pindex];
			for (size_t qindex = 0; qindex < q_set.size(); qindex++)
			{
				q = q_set[qindex];
				//for now!
				if (!cooperate)
					q = p;
        /*
				if (graphT == from_file)
				{
					readFile(0);
				}
        */
				for (run = 0; run < runNum; run++)
				{
					init_states(seedsNum);
					//for (size_t t = starting_time; t <= 100000000 && actives.size() >= 1 ; t += time_step_size)

					if( graphT != from_file )
					{
						for (size_t t = starting_time; t <= 100000000 && actives.size() >= 1 ; t += time_step_size)
						{
							//std::cout << "t: " << t << '\n';
							//emergence of the second disease
							//if(t == 20)
								//society[0].set_seed(dis_two);
							if(grid_output_on)
								grid_output(vert_num, animout);

							if(timed_output_on)
							{
								tout << run <<", ";
								tout << t - starting_time <<", ";
								simple_output(tout, true);
							}
								//terminal_output(graphT, run, last_time_step);

							//if (graphT == from_file)
							//{
								//last_time_step = readfile(t);
							//}

							//print_graph(society);

							Vertex vd;
							for (std::set<int>::iterator it=actives.begin(); it!=actives.end(); it++)
						  {
								vd = *it;
								//std::cout << "vd: "<< vd << '\n';
								//std::cout << "supply: "<< society[vd].supply() << '\n';
								if (society[vd].supply() != neither)
								{
									//std::cout << vd << ": " << '\n';
									for ( Vertex vi : make_iterator_range( adjacent_vertices(vd, society) ) )
									{
										//std::cout << "vi: "<< vi << '\t';
										society[vi].turn_I( society[vd].supply(), t );
									}
								}
						  }
							actives = {};
							for( Vertex vd : make_iterator_range( vertices(society) ) )
							{
								//society[vd].recover(t);
								if(society[vd].upgrade(t) != 1)
								//if(society[vd].update() != 1)
								{
									actives.insert(vd);
								}
							}
						}
					}

					if( graphT == from_file )
					//else if (false)
					{
						//std::cout << "seed is: " << seed << '\n';
						starting_time = FlashForward(seed);
						//starting_time =
						if( algorithm == SamplingAlgorithm::halfGillespie )
						{
							society[seed].reEvaluateSeed( starting_time ); // to increase the recover time of the seed, based on the FlashForwarded time.s
						}
						//std::cout << "starting_time: " << starting_time << '\n';
						//print_graph(society);
						int edge = 0;
						//std::cout << "t: " << t << '\n';
						//for (size_t t = starting_time; (t <= -1) && interactionsRemaining ; t += time_step_size)
						if ( algorithm == SamplingAlgorithm::RejectionSample )
						{
							for (size_t t = starting_time; t < 100000000000 && interactionsRemaining ; t += time_step_size)
							{

								if(timed_output_on)
								{
									tout << run <<", ";
									tout << t - starting_time <<", ";
									simple_output(tout, true);
								}


								last_time = t;
								int passedLoops = 0;
								if(!temporal_periodic_boundary_condition)
								{
									maxPassedLoops = 0;
									std::cout << "non-periodic!" << '\n' << '\n';

								}
								while (  temporal_graph[ edge % edge_num ][0] + passedLoops * temporal_graph[ edge_num - 1 ][0] <= t && passedLoops <= maxPassedLoops)
								{
									edge++ ;
									if( edge > edge_num )
										passedLoops ++ ;
									society[ temporal_graph[ edge % edge_num ][1] ].turn_I( society[ temporal_graph[ edge % edge_num ][2] ].supply(), t );
									society[ temporal_graph[ edge % edge_num ][2] ].turn_I( society[ temporal_graph[ edge % edge_num ][1] ].supply(), t );

								}

								//for( Vertex vd : make_iterator_range( vertices(society) ) )

								for (size_t vd = 0; vd < vert_num; vd++) //for hpc tailored version
								{
									//society[vd].recover(t);
									//society[vd].update();
									society[vd].upgrade(t);
									//std::cout << "vd: " << vd << '\n';
								}

	              if( Person::demanderNum == 0 || Person::supplierNum == 0 )      //SIR only
								{
									interactionsRemaining = 0;                                    //SIR only
									//std::cout << "interactionsRemaining = 0 " << '\n';
								}

	              Person::supplierNum = 0;                                     //SIR only
	              Person::demanderNum = vert_num;                                     //SIR only
								//if(!((t - starting_time) % 1))
								//{
									//std::cout << "t: " << t - starting_time << '\n';
									//std::cout<<"edge time: "<<temporal_graph[ edge % edge_num ][0] <<'\n';
								//}
							}
						}
						else if( algorithm == SamplingAlgorithm::halfGillespie )
						{


							int t = 0;
							int lastEdget = 0;
							for (size_t edge = 0; edge < 100000000000 && interactionsRemaining ; edge++)
							{
								std::cout << "edge" << '\n';
								t = temporal_graph[ edge % edge_num ][0];
								std::cout << "t: " << t << '\n';
								society[ temporal_graph[ edge % edge_num ][1] ].turn_I( society[ temporal_graph[ edge % edge_num ][2] ].supply(), t );
								society[ temporal_graph[ edge % edge_num ][2] ].turn_I( society[ temporal_graph[ edge % edge_num ][1] ].supply(), t );

								//for( Vertex vd : make_iterator_range( vertices(society) ) )
								if ( t != lastEdget )
									for (size_t vd = 0; vd < vert_num; vd++) //for hpc tailored version
									{
										//society[vd].recover(t);
										//society[vd].update();
										society[vd].upgrade(t);
										//std::cout << "vd: " << vd << '\n';
									}
									/*
									if( Person::demanderNum == 0 || Person::supplierNum == 0 )      //SIR only
									{
										interactionsRemaining = 0;                                    //SIR only
										std::cout << "demand: " << Person::supplierNum << '\n';
									}

								Person::supplierNum = 0;                                     //SIR only
								Person::demanderNum = vert_num;                                     //SIR only
								*/
								//if(!((t - starting_time) % 1))
								//{
									//std::cout << "t: " << t - starting_time << '\n';
									//std::cout<<"edge time: "<<temporal_graph[ edge % edge_num ][0] <<'\n';
								//}

								lastEdget = t;
								if(timed_output_on)
								{
									tout << run <<", ";
									tout << t - starting_time <<", ";
									simple_output(tout, true);
								}

							}
						}
						//std::cout << "last time: " << last_time << '\n';
            interactionsRemaining = 1;                                      //SIR only
					}
					//last_time_mean += (double)last_time / runNum;
					//last_time_max = fmax( last_time_max, last_time );
					//last_time_min = fmin( last_time_min, last_time );
					if(grid_output_on)
						grid_output(vert_num, animout);
					if(run % 100 == 0)
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
					}

					//cluster_size();
					//fout << ab_cluster << '\n';
					//fout << ab_cluster;
					//fout <<", " << a_cluster;
					//fout <<", " << b_cluster << '\n';

					simple_output(fout, false, output_seed_num, seed);
					if( graphT == from_file )
						if(Person::demanderNum != 0 && Person::supplierNum != 0)
						{
							std::cout << "demanderNum: " << Person::demanderNum << '\n';
							std::cout << "supplierNum: " << Person::supplierNum << '\n';
							std::cout << "the simulation could go on!" << '\n';
						}
				}
			}
		}
	}

	//std::cout << "last time mean: " << last_time_mean << '\n';
	//std::cout << "last time max: " << last_time_max << '\n';
	//std::cout << "last time min: " << last_time_min << '\n';
	fout.close();
	animout.close();

	clock_t end = clock();
  double elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
	std::cout << "elapsed time: " << elapsed_secs << '\n';
	std::cout << "random code: " << randlong << '\n';
	std::cout << "time_step_size: " << time_step_size << '\n';
}
