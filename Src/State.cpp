#include <iostream>
#include "State.h"
#include "global.h"
#include "Person.h"

//int State::population = 0;
//int SimpleState::population = 0;
//int Susceptible::population = 0;


Susceptible susceptible;
Recovered recovered;
//SimpleState infected_b (&recovered_b, &) ;
//SimpleState infected_a (&recovered_a, ) ;
Infected_AB infected_ab;

State::State()
{
	//name = title;
	//population++;
}

int State::getPopulation()
{
	return population;
}

void State::printState()
{
	std::cout << name << '\n';;
}


void Susceptible::interact( Person * supplier, Person * receiver )
{
	if( supplier -> getState() == &infected_a || supplier -> getState() == &infected_b )
	{
		if ( dice(p) )
		{
			receiver -> setFuture( supplier -> getState() );
			population--;

			(supplier -> getState() )->population++; // temp
			//(receiver -> getFuture() )->population++;
		}
	}
	else if( supplier -> getState() == &infected_ab  )
	{
		if ( auto target_ind = dist(generator) )
		{
			receiver -> setFuture( toABtargets [ target_ind ] );
			population--;

			(receiver -> getFuture() )->population++;
		}
	}
}
/*
void SimpleState::interact( Person * supplier, Person * receiver )
{
	if( (supplier -> getState() == &infected_a || supplier -> getState() == &infected_b) )
	{
		if ( dice(q) )
		{
			receiver -> setFuture( supplier -> getState() );
			population--;
			( supplier -> getState() ) -> population++;
		}
	else if( supplier -> getState() == &infected_ab  )
		if ( dice(q) )
		{
			receiver -> setFuture( supplier -> getState() );
			population--;
			( supplier -> getState() ) -> population++;
		}
	}
}

void SimpleState::sponTransit(Person * person)
{
	if ( dice (r) )
	{
		person -> future = transTarget;
		//person -> future = &susceptible;
		population--;
		transTarget -> population++;
		//transTarget -> printState();
	}
}
*/
Susceptible::Susceptible()
{
	//dist.param( {weights[0], weights[1], weights[2], weights[3]} );
	dist.param( toABweights );
	toABtargets  = { &susceptible, &infected_a, &infected_b, &infected_ab };
}

Infected_AB::Infected_AB()
{
	//dist.param( {weights[0], weights[1], weights[2], weights[3]} );
	dist.param( fromABweights );
	fromABtargets  = { &infected_ab, &infected_a, &infected_b};
}


void Susceptible::printState()
{
  std::cout << "S" << '\n';
}

void SimpleState::printState()
{
  std::cout << "I" << '\n';
}

void Infected_AB::sponTransit(Person * person)
{
	if ( auto target_ind = dist(generator) )
	{
		person -> setFuture( fromABtargets [ target_ind ] );
		population--;

		(person -> getFuture() ) -> population++;
	}
}

//std::random_device SimpleState::RANDOM_SEED;
//std::mt19937 SimpleState::generator( RANDOM_SEED() );
//std::discrete_distribution<int> State::dist{ 1,4 };
