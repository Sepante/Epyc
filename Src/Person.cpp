#include "global.h"
#include "Person.h"
#include <iostream>

//int Person::ab_cluster_ = 0;
//int Person::a_cluster_ = 0;
//int Person::b_cluster_ = 0;
int Person::supplierNum = 0;
int Person::demanderNum = 0;

std::random_device randomSeed;
std::default_random_engine gene( randomSeed( ) );
float gen = 2000;
//std::normal_distribution<float> gaussian(1,2);
//std::exponential_distribution<float> expon(0);
//std::normal_distribution<float> expon(3 * 24 * 3600, 1 * 24 * 3600);
//std::exponential_distribution<double> expon( 1/(20000) );

float expon(float gen)
{
	return gen;
}

//Person::exp(1);
//gaussian agg;
void Person::initialize(float rambda)
{
	//expon.param(std::exponential_distribution<float>::param_type( rambda ));
	std::cout << "inited!" << '\n';
}

float Person::distribution(float min, float max)
{
	while (true)
	{
		float randomNumber = expon(gen);
		if (randomNumber >= min && randomNumber <= max)
				return randomNumber;
	}
}

Person::Person()
{
	//std::cout << expon.param() << '\n';
	//expon.param(std::exponential_distribution<float>::param_type(1 / 100.0));
	health = 1;
	future = 1;
	//for now, it has to change if we want to increase the performance by being able to jump the interaction-less steps.
	recoveryTime[0] = 0;
	recoveryTime[1] = 0;
	//std::cout << "g: " << gen() << '\n';
	//std::cout << "g: " << expon(gen) << '\n';
	//gen.seed(0);
	//if(algorithm == SamplingAlgorithm::halfGillespie)
	//	std::cout << "halo" << '\n';
}
///*
//Person::Person(SamplingAlgorithm algorithm)
Person::Person(int a)
{
	health = 1;
	future = 1;
	//for now, it has to change if we want to increase the performance by being able to jump the interaction-less steps.
	recoveryTime[0] = 0;
	recoveryTime[1] = 0;
	//if(algorithm == SamplingAlgorithm::halfGillespie)
	std::cout << "halo" << '\n';
}
//*/

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
void Person::turn_I(Transfer supply, int t) // transfers diseases, using chances p & q.
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
				if (dice(0.5)) // by 0.5 chance the order of infections will be swapped.
				{
					dis_first = dis_two;
					dis_second = dis_one;
				}

				if (dice(p)) // if the first disease is transmitted.
				{
					if (dice(q)) // if the second one is transmitted too.
					{
						future *= (dis_first*dis_second) ;
						//if( algorithm == SamplingAlgorithm::halfGillespie )
						{
							recoveryTime[0] = t + expon(gen);
							recoveryTime[1] = t + expon(gen);
							//std::cout << "recov time" << recoveryTime[0] << '\n';
						}

					}
					else // if the second one is not transmitted.
					{
						future *= dis_first;
						//if( algorithm == SamplingAlgorithm::halfGillespie )
							recoveryTime[ dis_first - 2 ] = t + expon(gen); //temporal, ugly way of finding the index of the disease (dis - 2)
					}
				}
				else if (dice(p)) //if the first disease is not and the second IS transmitted. (the chance for each disease is p.)
				{
					future *= dis_second;
					//if( algorithm == SamplingAlgorithm::halfGillespie )
						recoveryTime[ dis_second - 2 ] = t + expon(gen); //temporal, ugly way of finding the index of the disease (dis - 2)
				}
			}
			else if (dice(p)) //if the demand is both and the supply is not, the reciever will get anything the supply offers, by probability p.
			{
				future *= supply;
				//std::cout << "supply: " << supply << '\n';


				//if( algorithm == SamplingAlgorithm::halfGillespie )
					if (supply == 2 || supply == 3 ) // only this case raised an error, because there's a possibility of supply = 1. but overall this design is ugly and has to change.
						recoveryTime[ supply - 2 ] = t + expon(gen); //temporal, ugly way of finding the index of the disease (dis - 2)
			}
			//std::cout << "First item selected!" << std::endl;
 			break;
    default:
      //std::cout << "Second item selected!" << std::endl;
			if (supply == demand_v || supply == both) //if demand only asks for one disease and the supply can provide it.
				if(dice(q))
				{
					future *= demand_v;
					//if( algorithm == SamplingAlgorithm::halfGillespie )
						recoveryTime[ demand_v - 2 ] = t + expon(gen);

				}
      break;
		}
		//std::cout << health << '\n';
	};
//used in rejection_based algorithm.
Transfer Person::update(int t) // updates the future (which is used to calculate the supply) and recoveres the node.
{

	//updating the infection
	health = future;


	if( supply() != neither )
	{
		supplierNum ++;
	}
	if( demand() == neither )
	{
		demanderNum --;
	}

	return supply();

}

void Person::set_seed(Transfer dis) // has to be modified for the instance
// that the node has previously infected by the same disease.
// later note: "seems to be modified now, for adding if(health == 1)"
{
	if(health == 1)
	{
		health *= dis;
		future *= dis;
		if( dis == both )
		{
			recoveryTime[0] = expon(gen);
			recoveryTime[1] = expon(gen);
		}
		else if ( dis == dis_one || dis == dis_two )
			recoveryTime[ dis - 2 ] = expon(gen); //temporal, ugly way of finding the index of the disease (dis - 2)


		//if(dis == both)
		//ab_cluster_ ++;
		//else if(dis_one)
		//a_cluster_ ++;
	}
	//std::cout << "r time: " << recoveryTime[0] << '\n';
}

void Person::reEvaluateSeed(int t)
{
	//recoveryTime[0] = t + expon(gen);
	//recoveryTime[1] = t + expon(gen);
	recoveryTime[0] += t;
	recoveryTime[1] += t;
}


/*
void Person::turn_R(Transfer dis) //used only in the gillespie algorithm form for recoveries.
{
	health *= dis;
	future *= dis;
}
*/
void Person::recover(int t)
{
	//std::cout << "this dude is recovering: " << '\n';
	if( algorithm == SamplingAlgorithm::halfGillespie)
	{
		if (supply() % 2 == 0)
			if (t >= recoveryTime[0])
			{
				future *= 2;
				//std::cout << "I got recovered on t: " << t << '\n';

			}
		if (supply() % 3 == 0)
			if (t >= recoveryTime[1])
				future *= 3;
	//std::cout << "future: " << future << '\n';

	}

	if( algorithm == SamplingAlgorithm::RejectionSample)
	{
		if (supply() % 2 == 0)
			if (dice (r) )
			{
				//health *= 2;
				//std::cout << "I got recovered on t: " << t << '\n';
				future *= 2;
			}
		if (supply() % 3 == 0)
			if (dice (r) )
			{
				//health *= 3;
				future *= 3;
			}
	}
}

Transfer Person::upgrade(int t)
{
	recover(t);
	return update(t);
}
