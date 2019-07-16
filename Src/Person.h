#ifndef PERSON_H
#define PERSON_H
#include <iostream>
#include <random>
#include <vector>


using std::vector;

//int number_of_diseases = 2;
enum Transfer { neither = 1, dis_one = 2 , dis_two = 3, both = 6 };
enum disease_state { S = 0, I = 1, R = 2 };
class Person
{
	private:
	//int number_of_diseases = 2;
	//std::vector<int> state = vector<int>(number_of_diseases);

	int health;
	int future;
	//float recoveryTime;
	vector<float> recoveryTime={0,0};
	//vector<disease_state> state;
	//static int indexFinder(){ if };

	public:

	//static int a_cluster_, b_cluster_, ab_cluster_;
	static int supplierNum;
	static int demanderNum;
	static void initialize(float rambda);
	static float distribution(float min, float max);
	//{
			//expon.param(std::exponential_distribution<float>::param_type(1 / 200.0));
	//}
	Person();
	//Person(SamplingAlgorithm algorithm);

	Person(int a);
	void set_health(int s);
	void set_future(int s);

	void refresh();

	int get_health();
	int get_future();

	Transfer demand();
	Transfer supply();
	void turn_I(Transfer supply, int t);
	Transfer update(int t);
	void recover(int t);
	void reEvaluateSeed(int t);
	Transfer upgrade(int t);

	void set_seed(Transfer dis);

};

#endif
