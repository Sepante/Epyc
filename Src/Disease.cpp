#include "global.h"
#include "Disease.h"
#include <iostream>

Disease operator +=(Disease &a, Disease &b)
{
	switch (b.state)
	{
		case State::IR:
		case State::IS:
			if (a.state == State::S)
				a.future_state = b.state;
			break;
		//default:
	}
}

State Disease::operator ++(int)
{
	switch (state)
	{
		case State::IR:
			future_state = State::R;
			break;
		case State::IS:
			future_state = State::S;
			break;
	}
}

//State Disease::operator ++()
//{

//}

void Disease::update()
{

	state = future_state;
}

bool Disease::is_infector ()
{
	if(state == State::IR || state == State::IS)
		return true;
	else
		return false;
}

void Disease::print_state()
{
	switch (state) {
		case State::IS:
			std::cout << "IS" << '\n';
			break;
		case State::IR:
			std::cout << "IR" << '\n';
			break;
		case State::S:
			std::cout << "S" << '\n';
			break;
		case State::D:
			std::cout << "D" << '\n';
			break;
		case State::R:
			std::cout << "R" << '\n';
			break;
	}
}

/*
int main()
{
	Disease disease[2];
	disease[1].state = State::IR;
	disease[0].print_state();
	disease[0] += disease[1];
	disease[0].print_state();
	disease[0]++;
	disease[0].print_state();
	disease[0]++;
	disease[0].update();
	disease[0].print_state();
	disease[0]++;
	disease[0].update();
	disease[0].print_state();
}
*/
