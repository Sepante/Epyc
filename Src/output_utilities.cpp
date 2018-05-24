#include "output_utilities.h"

void terminal_output(Graph_Type graphT, int run, int last_time_step)
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
