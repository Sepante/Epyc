//#include "global.h"
#include "Person.h"
#include <iostream>
///////temp
float q=0,p=0,r=0;
bool dice(float probb) {return true;}
///////temp
int Person::population = 0;
Person::Person()
{
	population++;
}

/*
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
*/

int main()
{
	//Disease dis;
	Person a,b;
	std::cout << "done" << '\n';
}
