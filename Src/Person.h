#include <iostream>
#include "State.h"
//#include "Defined_States.h"

#ifndef PERSON_H
#define PERSON_H


class Person
{
	public:
		Person();
	  State * state;
		State * future;

		State * getState();
		State * getFuture();

		bool isInfector();

		void setState( State * newState );
		void setFuture( State * newFuture );

		void refresh();

		void printPerson();
		void operator ++(int);

		void interact(Person supplier);
		bool update();

		void setSeed( State * newState );

};

#endif
