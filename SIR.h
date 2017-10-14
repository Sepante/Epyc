#ifndef SIR_H
#define SIR_H
#include <iostream>

typedef enum { neither = 1, dis_one = 2 , dis_two = 3, both = 6 } Transfer;
class SIR
{
	public:

	int health = 1;
	int future = 1;

	Transfer demand();
	Transfer supply();
	void turn_I(Transfer supply);
	Transfer update();
	
};



#endif
