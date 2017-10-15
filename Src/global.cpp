#include <iostream>

bool dice(float prob)
{
	float r = ((float) rand() / (RAND_MAX));
	if (r < prob)
		return 1;
	else return 0;
}
