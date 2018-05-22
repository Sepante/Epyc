#ifndef SIR_H
#define SIR_H
#include <iostream>

enum Transfer { neither = 1, dis_one = 2 , dis_two = 3, both = 6 };
class SIR
{
	private:
	int health = 1;
	int future = 1;

	public:
	void set_health(int s);
	void set_future(int s);

	void refresh();

	int get_health();
	int get_future();

	Transfer demand();
	Transfer supply();
	void turn_I(Transfer supply);
	Transfer update();

};



#endif
