#ifndef PERSON_H
#define PERSON_H
//#include <iostream>
#include <vector>
#include "Disease.h"

using std::vector;

//int disease_num = 2;
enum Transfer { neither = 1, dis_one = 2 , dis_two = 3, both = 6 };
//enum class disease_state { S_SI = 0, I_SIR = 1, R = 2};
//class Disease;
class Person
{
	friend class State_R;
	friend class State_S;
	friend class State_I_R;
	friend class State_I_S;


	private:

		static const int disease_num;
		static int population;

		//states ready to use:
		State_I_R istate;

	public:

		//vector<Disease*> disease = vector<Disease*>(disease_num);
		Person();

		void update();

		void operator ++(int);
		void operator +=(Person &b);
		void print_person();
};



#endif
