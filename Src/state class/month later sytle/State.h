//#include "global.h"
#ifndef STATE_H
#define STATE_H

#include <iostream>
class Person;
class State
{
	public:
		Person *person;
		State(Person * person)
		{
			person = person;
		}
    //virtual void Disease::operator ++(int)
		virtual void talk()
		{
			std::cout << "I'm empty!" << '\n';
		}
		virtual void swtch(){}

};


class Susceptible: public State
{
	public:
		void talk()
		{
			std::cout << "I'm Susceptible!" << '\n';
		}

		void swtch()
		{
			//person->state = person->infected;
			std::cout << "s" << '\n';
		}
};

class Infected: public State
{
	public:
		void talk()
		{
			std::cout << "I'm Infected!" << '\n';
			std::cout << this << '\n';
		}

		void swtch()
		{
			//person->state = person->susceptible;
			std::cout << "s" << '\n';
		}
};


#endif
