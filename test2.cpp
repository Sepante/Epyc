#include <iostream>
#include <fstream>
#include <vector>
#include <array>
#include <numeric>
#include <ctime>
#include <math.h>
#include<set>
using namespace std;

int main()
{
	set <int> actives={88,4,99};
	set <int> actives_cp=actives;
	int i;
	actives.erase(99);
	for (set<int>::iterator it=actives.begin(); it!=actives.end(); it++)
	{

		i = *it;
		cout<< *it<<endl;
	}
	cout<<actives.size();
}

