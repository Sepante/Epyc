#ifndef OUTPUT_UTILITIES_H
#define OUTPUT_UTILITIES_H
#include <iostream>
#include <fstream>
#include "SIR.h"
#include "graph_base.h"

enum Graph_Type { erdos = 1, grid = 2, grid3D = 3, from_file = 4};
//extern Graph_Type graphT;
void get_output(Graph_Type graphT, int run, int last_time_step);
void grid_output(int n, std::ofstream& tout);


#endif
