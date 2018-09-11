#include "global.h"
#include "Person.h"
#include <iostream>
///////temp
float q=0,p=0,r=0;
bool dice(float probb) {return true;}
///////temp

int Person::population = 0;
const int Person::disease_num = 1;
Person::Person()
{
	population++;
	disease[0] = &istate;
	int disease_ind = 0;
	//disease[1] = &istate;
	//disease = disease;
	//std::cout<<"I am created. "<<population<<std::endl;
}

void Person::update()
{
	for (disease_ind = 0; disease_ind <= Person::disease_num -1 ; disease_ind++)
		disease[disease_ind]->update();
}

void Person::operator ++(int)
{
	for (disease_ind = 0; disease_ind <= Person::disease_num -1 ; disease_ind++)
		*disease[disease_ind]++;
}

void Person::operator +=(Person &b)
{
	for (disease_ind = 0; disease_ind <= Person::disease_num -1 ; disease_ind++)
		*disease[disease_ind] += *b.disease[disease_ind];
}

void Person::print_person()
{
	for (disease_ind = 0; disease_ind <= Person::disease_num -1 ; disease_ind++)
		disease[disease_ind]->print_state();
	std::cout << '\n';
}

int main()
{
	//Disease dis;
	Person a,b;
	//std::cout << (a.disease[0]) << '\n';
	//std::cout << (a.disease[1]) << '\n';
	//a.disease[0]->state = State::IR;
	a.print_person();
	(a.disease[0])->print_state();
	a.disease[0]->state = State::IS;
	a.print_person();
	a++;
	a.update();
	a.print_person();
	/*
	a.disease[0].print_state();
	a++;
	a.disease[0].print_state();
	a.update();
	a.disease[0].print_state();

	std::cout << "now for 1:" << '\n';
	b.disease[0].print_state();
	b+=a;
	b.disease[0].print_state();
	b.n_update();
	b.disease[0].print_state();
	b++;
	b.disease[0].print_state();
	b.n_update();
	b.disease[0].print_state();

	//a+=b;
	//x++;
	//y.turn_I(neither);
	*/
}
