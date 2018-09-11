//#include "global.h"
#include "Disease.h"
#include <iostream>

/*
void Disease::operator +=(Disease &b)
{
	switch (b.state)
	{
		case State::IR:
		case State::IS:
			if (state == State::S)
				future_state = b.state;
			break;
		//default:
	}
}
*/

void Disease::operator ++(int)
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

int main()

{
	State_I_R dis, dis2;
	/*
	//State_R x;

	//dis.print_state();
	//dis2.state = State::IR;
	dis2.state = State::IS;

	dis2.print_state();
	//dis2 += dis;
	dis2.update();
	dis2.print_state();

	//dis.print_state();
	//dis++;
	//dis.update();
	//dis.print_state();

	*/
}
