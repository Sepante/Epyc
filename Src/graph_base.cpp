#ifndef GRAPH_BASE_H
#define GRAPH_BASE_H
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


#endif
