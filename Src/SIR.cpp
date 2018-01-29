#include "global.h"
#include "SIR.h"
#include <iostream>



Transfer SIR::demand() //returns the demand value of the node.
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

Transfer SIR::supply() //returns the supply value of the node.
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
void SIR::turn_I(Transfer supply) // transfers diseases, usins chances p & q.
{
		Transfer demand_v = demand();
		switch (demand_v)
		{
		case neither: //if the reciever(demand) is already (or has been) infected by both diseases.
			//std::cout << "Invalid selection!" << std::endl;
			break;
    case both: //if the reciever(demand) is susceptible to both diseases.
			if (supply == both) // supply and demand are in "both" state.
			{
				auto dis_first = dis_one, dis_second = dis_two;
				if (dice(0.5)) // by 0.5 chance the order of infections will be swaped.
				{
					dis_first = dis_two;
					dis_second = dis_one;
				}

				if (dice(p)) // if the first disease is transmitted.
				{
					if (dice(q)) // if the second one is transmitted too.
						future *= (dis_first*dis_second) ;
					else // if the second one is not transmitted.
						future *= dis_first;
				}
				else if (dice(p)) //if the first disease is not and the second IS transmitted. (the chance for each disease is p.)
					future *= dis_second;
			}
			else if (dice(p)) //if the demand is both and the supply is not, the reciever will get anything the supply offers, by chance p.
				future *= supply;
			//std::cout << "First item selected!" << std::endl;
 			break;
    default:
      //std::cout << "Second item selected!" << std::endl;
			if (supply == demand_v || supply == both) //if demand only asks for one disease and the supply can provide it.
				if(dice(q))
					future *= demand_v;
      break;
		}
		//std::cout << health << '\n';
	};
//used in rejection_based algorithm.
Transfer SIR::update() // updates the future (which is used to calculate the supply) and recovres the node.

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
