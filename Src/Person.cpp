#include <iostream>
#include "Person.h"


Person::Person()
{
	future = state = &susceptible;
	susceptible.population++ ;
	//temp
}

bool Person::isInfector()
{
	return (state -> isInfector( ) );
}

void Person::operator ++(int)
{
	state -> sponTransit( this );
}

void Person::interact( Person supplier )
//this feature is actually handled by the future, future is changed before the end of the time-step and this is what we desire, since
//a single Person should not be infected by the same disease twice in one time-step.
{
	future -> interact( &supplier , this );
}

State * Person::getState()
{
	return state;
}

State * Person::getFuture()
{
	return future;
}

void Person::refresh()
{
	//std::cout << "boo: " << '\n';
	//state -> printState();
	//state -> population --;
	//std::cout << "pop: " << susceptible.population << '\n';
	future = &susceptible;
	state = &susceptible;
	//susceptible.population ++ ;
	//std::cout << "pop: " << state -> population << '\n';
	//temp
}

void Person::setState( State * newState )
{
	state = newState;
}

void Person::setFuture( State * newFuture )
{
	future = newFuture;
}

//void Person::update()
bool Person::update()
{
	state = future;
	return (state -> isInfector( ) );
}

void Person::printPerson()
{
	std::cout << "current: " ;
	state -> printState();
	std::cout << "future: " ;
	future -> printState();
}

void Person::setSeed( State * newState )
{
	state -> population --;
	setState( newState );
	setFuture( newState );
	newState -> population ++;
}
