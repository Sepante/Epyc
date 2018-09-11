#include "global.h"
#include "Person.h"
#include <iostream>
#include "graph_base.h"
#include <random>
#include "output_utilities.h"
#include <fstream>
#include <array>
#include <set>
#include <ctime>
#include <math.h>
#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/graph_utility.hpp>
#include <boost/graph/properties.hpp>
#include <boost/config.hpp>
#include <boost/graph/connected_components.hpp>
/*
*/

float p = 0.05, q = 1, r = 1;
std::random_device RANDOM_SEED;
std::mt19937 generator( RANDOM_SEED() );

//std::vector<int> targets = {0,1,2,3};

/*
int targetDeclare(std::vector<int>& targets, std::vector<float>& weights)
{
	//std::cout << targets[0] << '\n';
	std::random_device realRandomSeed;  //Will be used to obtain a seed for the random number engine
	std::mt19937 generator( realRandomSeed() );
	//std::uniform_int_distribution<> d	istribution(1, 9);
	std::discrete_distribution<int> dist {1,1};

	dist.param( {0,1,2,3} );
	dist.param( {weights[0], weights[1], weights[2], weights[3]} );
	//std::cout << targets [ dist(generator) ] << '\n';
	return (targets [ dist(generator) ]);
	//std::cout << dist.param()[0] << '\n';
}
*/
//std::vector<int> bins{0,1,2,3};
int main()
{

	//static std::discrete_distribution<int> dist {1,1,10};
	//Susceptible susceptible;
	//std::cout << susceptible.dist (generator) << '\n';
	//susceptible.dist.param ( {1,1,100} );
	//std::cout << susceptible.dist (generator) << '\n';

	//std::cout << infected_b.dist (generator) << '\n';
}
