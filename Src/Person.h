#ifndef PERSON_H
#define PERSON_H
//#include <iostream>
#include <vector>
#include "Disease.h"

using std::vector;

//int disease_num = 2;
enum Transfer { neither = 1, dis_one = 2 , dis_two = 3, both = 6 };
//enum class disease_state { S_SI = 0, I_SIR = 1, R = 2};
class Person
{
	private:
		static const int disease_num;

		int health = 1;
		int future = 1;
		//vector<disease_state> state;
		static int population;

	public:
		vector<Disease> disease = vector<Disease>(disease_num);
		Person();
		void set_health(int s);
		void set_future(int s);

		void refresh();

		int get_health();
		int get_future();

		Transfer demand();
		Transfer supply();
		void turn_I(Transfer supply);
		Transfer update();
		void n_update();
		void set_seed(Transfer dis);

		void operator ++(int);
		friend void operator +=(Person &a, Person &b);
};



#endif
