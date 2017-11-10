#include "global.h"
#include "SIR.h"
#include <iostream>



Transfer SIR::demand()
{
		if(future == 1)
			return both;
		else if (future == 3 || future == 9)
		{
			return dis_one;
		}
		else if (future == 2 || future == 4)
		{
			return dis_two;
		}
		else return neither;
	};

Transfer SIR::supply()
{
		if(health == 6)
			return both;
			else if (health == 2 || health == 18)
			{
				return dis_one;
			}
			else if (health == 3 || health == 12)
			{
				return dis_two;
			}
			else return neither;
	};
void SIR::turn_I(Transfer supply)
{
		Transfer demand_v = demand();
		switch (demand_v)
		{
		case neither:
			//std::cout << "Invalid selection!" << std::endl;
			break;
    case both:
			if (supply == both) // supply and demand are in "both" state.
			{
				auto dis_first = dis_one, dis_second = dis_two;
				if (dice(0.5))
				{
					dis_first = dis_two;
					dis_second = dis_one;
				}

				if (dice(p))
				{
					if (dice(q))
						future *= (dis_first*dis_second) ;
					else
						future *= dis_first;
				}
				else if (dice(p))
					future *= dis_second;
			}
			else if (dice(p))
				future *= supply;
			//std::cout << "First item selected!" << std::endl;
 			break;
    default:
      //std::cout << "Second item selected!" << std::endl;
			if (supply == demand_v || supply == both)
				if(dice(q))
					future *= demand_v;
      break;
		}
		//std::cout << health << '\n';
	};

Transfer SIR::update()
{

	auto prev_supply = supply();

	//updating the infection
	health = future;

	//recoveries:
	if (prev_supply % 2 == 0)
		if (dice (r) )
			health *= 2;
	if (prev_supply % 3 == 0)
		if (dice (r) )
			health *= 3;

	future = health;
	return supply();
}
