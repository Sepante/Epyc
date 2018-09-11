#include <iostream>
#include "Defined_States.h"

int Infected::population = 0;
int Susceptible::population = 0;

int Susceptible::get_population()
{
	return population;
}

Susceptible::Susceptible()
{
	population++;
}

void Susceptible::interact( Person * supplier, Person * receiver )
{
	if( supplier -> getState() == &infected_a || supplier -> getState() == &infected_b )
		receiver -> setFuture( supplier -> getState() );
}

//void Susceptible::spon_transit(){}

void Infected::spon_transit(Person * person)
{
	person -> future = &susceptible;
}

Infected::Infected()
{
	population++;
}



void Susceptible::print_state()
{
  std::cout << "S" << '\n';
}


void Infected::print_state()
{
  std::cout << "I_A" << '\n';
}
