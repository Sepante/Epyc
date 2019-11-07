#include "graph_base.h"

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

void cons_stochastic_block_network(int n, float disparity_prob)
{
	float cnct_prob = (float)4/(float)n;
	float same_block_prob = cnct_prob * ( 1 + disparity_prob );
	float other_block_prob = cnct_prob * ( 1 - disparity_prob );

	society.clear();
	//society(32);
	float i_block = 0, j_block = 0;
	for (size_t i = 0; i < n; i++)
	{
		if (i <= int(n / 2))
			i_block = 0;
		else
			i_block = 1;


		for (size_t j = i+1; j < n; j++)
		{
			if (j <= int(n / 2))
			j_block = 0;
			else
			j_block = 1;
			if (i_block == j_block)
				if ( dice(same_block_prob) )
				{
					add_edge(i, j, society);
					//add_edge(j, i, society);
				}
			else
				if ( dice(other_block_prob) )
				{
					add_edge(i, j, society);
				}

		}
	}
	//std::cout << "Erdos running" << '\n';
	//print_graph(society);
}
