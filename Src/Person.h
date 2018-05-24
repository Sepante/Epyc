#ifndef PERSON_H
#define PERSON_H
//#include <iostream>
#include <vector>

using std::vector;

//int number_of_diseases = 2;
enum Transfer { neither = 1, dis_one = 2 , dis_two = 3, both = 6 };
enum disease_state { S = 0, I = 1, R = 2 };
class Person
{
	private:
	int number_of_diseases = 2;

	std::vector<int> state = vector<int>(number_of_diseases);


	int health = 1;
	int future = 1;
	//vector<disease_state> state;

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

	void set_seed(Transfer dis);
};



#endif
