#include "global.h"
#include "Person.h"
#include <iostream>
float q=0,p=0,r=0;
bool dice(float probb) {return true;}
int Person::population = 0;
const int Person::disease_num = 1;
Person::Person()
{
	population++;
	//disease = disease;
	//std::cout<<"I am created. "<<population<<std::endl;
}
void Person::refresh()
{
	health = 1;
	future = 1;
}

int Person::get_health()
{
	return health;
}

int Person::get_future()
{
	return future;
}

Transfer Person::demand() //returns the demand value of the node.
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

Transfer Person::supply() //returns the supply value of the node.
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
void Person::turn_I(Transfer supply) // transfers diseases, using chances p & q.
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
Transfer Person::update() // updates the future (which is used to calculate the supply) and recovres the node.
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

void Person::set_seed(Transfer dis) // has to be modified for the instance
// that the node has previously infected by the same disease.
{
	health *= dis;
	future *= dis;
}

void Person::n_update()
{
	for (size_t disease_ind = 0; disease_ind <= Person::disease_num -1 ; disease_ind++)
		disease[disease_ind].update();
}

void Person::operator ++(int)
{
	for (size_t disease_ind = 0; disease_ind <= Person::disease_num -1 ; disease_ind++)
		disease[disease_ind]++;
}

void operator +=(Person &a, Person &b)
{
	for (size_t disease_ind = 0; disease_ind <= Person::disease_num -1 ; disease_ind++)
		a.disease[disease_ind] += b.disease[disease_ind];
}

/*
void Person::turn_R(Transfer dis) //used only in the gillespie algorithm form for recoveries.
{
	health *= dis;
	future *= dis;
}
*/
int main()
{
	Disease dis;
	Person a,b;
	a.disease[0].print_state();
	/*
	a.disease[0].state = State::IR;
	a.disease[0].print_state();
	//a++;
	a.disease[0].print_state();
//	a.n_update();
	a.disease[0].print_state();

	std::cout << "now for 1:" << '\n';
	b.disease[0].print_state();
	b+=a;
	b.disease[0].print_state();
	b.n_update();
	b.disease[0].print_state();
	b++;
	b.disease[0].print_state();
	b.n_update();
	b.disease[0].print_state();

	//a+=b;
	//x++;
	//y.turn_I(neither);
	*/
}
