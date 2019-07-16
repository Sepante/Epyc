#ifndef GLOBAL_H
#define GLOBAL_H
#include <random>
extern float r, p, q;
extern float rambda;
enum class SamplingAlgorithm {RejectionSample, halfGillespie};
extern SamplingAlgorithm algorithm;


bool dice(float prob);
#endif
