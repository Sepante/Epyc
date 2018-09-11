#ifndef GLOBAL_H
#define GLOBAL_H
#include <random>
extern float r, p, q;
//extern int actives_num;
bool dice(float prob);

extern std::random_device RANDOM_SEED;
extern std::mt19937 generator;

#endif
