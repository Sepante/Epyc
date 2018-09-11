#ifndef PERSON_H
#define PERSON_H
//#include <iostream>
#include <vector>
#include "State.h"

using std::vector;

class Person
{

	private:
		static int population;


	public:
		//Susceptible susceptible(this);
		//Infected infected(this);
		State state(this);
		Person();

		void update();

		void operator ++(int);
		void operator +=(Person &b);
		void print_person();
};




#endif
