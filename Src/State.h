#include <iostream>
#include <random>
#include "global.h"
#ifndef STATE_H
#define STATE_H

class Person;
class State
{
	private:
	protected:
		std::string name;
		std::discrete_distribution<int> dist{ 1 };
	public:
		int population = 0;
		State();
		virtual bool isInfector(){return false;};
		virtual void sponTransit(Person * person){};
		int getPopulation();
		virtual void printState();
		virtual void interact( Person * supplier, Person * receiver ){};
};

class Susceptible: public State
{
	private:
		std::string name = "S";
		float pr = 0.5 * p*(-p-q+2);
		std::discrete_distribution<int>::param_type toABweights { (1-p) * (1-p), pr, pr, p*q };
		std::vector<State *> toABtargets ;
	public:
		Susceptible();
		void interact( Person * supplier, Person * receiver );
		void printState();
};
/*
class SimpleState: public State
{
	private:
		//std::random_device realRandomSeed;  //Will be used to obtain a seed for the random number engine
		//std::discrete_distribution<int> dist {0,1};
	public:
		State * transTarget;
		State * interactTarget;
		bool isInfector(){return true;};
		SimpleState( State * transTarget, State * interactTarget ):
		transTarget (transTarget),
		interactTarget (interactTarget) {}

		virtual void interact( Person * supplier, Person * receiver );
		virtual void sponTransit(Person * person);
		virtual void printState();
};

*/
class Infected_AB: public State
{
	private:

		std::discrete_distribution<int>::param_type fromABweights { 1 - r - r - r*r , r, r, r*r };
		std::vector<State *> fromABtargets ;
	public:
		Infected_AB();
		void sponTransit( Person * person) ;
};

class Recovered: public State
{
public:
	void printState(){ std::cout << "R" << '\n'; }
};

extern Susceptible susceptible;
extern Recovered recovered;
extern Infected_AB infected_ab;
//extern SimpleState infected_a;
//extern SimpleState infected_b;

#endif
