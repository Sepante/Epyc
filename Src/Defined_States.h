#include <iostream>
#include "Person.h"

#ifndef DEFINED_STATES_H
#define STATE_H

class Person;
class Susceptible: public State
{
	private:
	public:
		static int population;
		Susceptible();
		virtual void spon_transit(Person * person){} ;
		void interact( Person * supplier, Person * receiver );
		int get_population();
		void print_state();
};

class Infected: public State
{
	private:
	public:
		static int population;
		Infected();
		//virtual void spon_transit(Person * person);
		//virtual void interact( Person * supplier, Person * receiver );
		void spon_transit(Person * person);
		void interact( Person * supplier, Person * receiver ){};
		void print_state();
};
/*
class Infected_A: public Infected
{
	private:
	public:
		void interact( Person * supplier, Person * receiver ) ;
};
*/
/*
class Person
{
	public:
		Person();
	  State * state;
		State * future;

		State * getState();
		State * getFuture();

		void setState( State * newState );
		void setFuture( State * newFuture );

		void print_person();
		void operator ++(int);

		void interact(Person supplier);
		void update();

};
*/

#endif
