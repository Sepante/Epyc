#include <iostream>
#include <fstream>
#include <vector>
#include <array>
#include <set>
#include <ctime>
#include <math.h>
using namespace std;

int L = pow (2, 7);
//int L = 10;
int n = L*L;
//int n =100;
float cnct_prob = (float)4/(float)n;
vector<vector<int>>  adj_matrix(n, vector<int>(n));
int seed;
int i;
set <int> actives={};
set <int> actives_cp=actives;

int I_num[]={1,1};
int S_num = n-1;
float p, q;
vector<int> state(n, 1);
vector<int> state_cp;

int been_I(int cell_state, int dis_index = 1, bool now = 0)
{
	// dis_index = 1 means any disease, 2 means the first and 3 means the second disease.
	bool returnval;
	if(dis_index == 1)
		returnval = cell_state >= 2 ;
	else
		returnval = cell_state%dis_index==0;
	if(!now)
		return returnval;
	else // now
	{
		if(returnval == 0)
			return 0;
		else
		{
			
		
			if(dis_index == 1)
				if( cell_state==2 || cell_state==3 || cell_state==6) // I states, not R.
					return 1;
				else
					return 0;
			else
			{
				int dis_pwd = dis_index * dis_index;
				return !(cell_state%dis_pwd==0);
			}
		}
	}
}

void constr_erdos(float cnct_prob) //construct adjacency matrix in the case of erdos renyi graph.
{
	float r;
	for (int i=0; i<= n-1; i++)
		for (int j=i+1; j<= n-1; j++)
		{
			r = ((float) rand() / (RAND_MAX));
			if(r <= cnct_prob)
				adj_matrix[i][j] = adj_matrix[j][i] = 1;
			else
				adj_matrix[i][j] = adj_matrix[j][i] = 0;
		}

		
						//output				
				/*
		for(int i=0; i<=n-1; i++)
		{
			for(int j=0; j<=n-1; j++)
				cout<<adj_matrix[i][j]<<"\t";
			cout<<endl;
		}
*/

}


void turn_R(int i, int dis_index)
{
	state[i]*=dis_index;				//turn_R after spreading between the neighbors. (one step)
	I_num[dis_index-2]--;
	if(state[i]==36 || state[i]==(dis_index*dis_index) )
	{
		actives.erase(i);
		//cout<<i<<" erased for being "<<state[i]<<endl;
	}
	
	else;
		//cout<<i<<"not erased for being "<<state[i]<<endl;
		

}

void turn_I(int i, int dis_index)
{
	if( !been_I(state[i], dis_index) ) // isn't already infected by this disease.
	{
		
		float r;
		int other_dis = ((dis_index+1)%2)+2;
		if( state[i] == 1 )// has not been infected by other disease (and by the previous condition, by this disease) even in this step, so has to be 1.
		{
			r = ((float) rand() / (RAND_MAX));
			if(r <= p)
			{
				state[i]*=dis_index;
				I_num[dis_index-2]++; //dis_index is 2 or 3, but indexes for I_num are 0 & 1, so we have to use -2.
				actives.insert(i);
				S_num--;
			}
		}
		else //has been infected by the other disease.
		{
			//cout<<state[i]<<endl;
			r = ((float) rand() / (RAND_MAX));
			if(r <= q)
			{
				state[i]*=dis_index;
				I_num[dis_index-2]++; //dis_index is 2 or 3, but indexes for I_num are 0 & 1, so we have to use -2.
				actives.insert(i);
			}
		}
		
		
	}	
}

void turn_grid_neighbs_I(int i, int dis_index)
{
	turn_I((i-1+n)%n, dis_index); //n is added to avoid negative remainder values.
	turn_I((i+1+n)%n, dis_index);
	turn_I((i+L+n)%n, dis_index);
	turn_I((i-L+n)%n, dis_index);
}

void turn_general_neighbs_I(int i, int dis_index)
{
	for (int j=0; j<= n-1; j++)
		if(adj_matrix[i][j] )
		{
			turn_I(j, dis_index);
		}
			
}

void initialize() //initialize variables for the next run
{
	S_num = n-1;
	I_num[0]=I_num[1]=1;
	fill(state.begin(), state.end(), 1);
	//initial seed
	seed = rand()%n;
	state[seed] = 6;
	state_cp = state;
	actives={seed};
	actives_cp = actives;
}

int main()
{
	constr_erdos(cnct_prob); //construct adjacency matrix in the case of erdos renyi graph.
	
	ofstream fout;
	fout.open ("cdata.txt");
	
	srand(time(0));
	
	int dis_index;
	int runNum = 100000;
	vector<float> p_set={0.1 ,0.2, 0.3, 0.4, 0.45, 0.5, 0.55, 0.6, 0.7, 0.8, 0.9, 1};
	vector<float> q_set={0.1 ,0.2, 0.4, 0.6, 0.8, 1};
	p_set={0.25};
	//q_set={0.1, 0.5};
	q_set={1};
	
	//write system properties to file, for later use in python.
	fout<<n<<"\n";
	fout<<p_set.size()<<"\n";
	fout<<q_set.size()<<"\n";
	fout<<runNum<<"\n";
	for(int pindex=0; pindex<=p_set.size()-1; pindex++)
		fout<<p_set[pindex]<<"\n";
	for(int qindex=0; qindex<=q_set.size()-1; qindex++)
		fout<<q_set[qindex]<<"\n";
	
	//loop on different p values.
	for(int pindex=0; pindex<=p_set.size()-1; pindex++)
	{
		p=p_set[pindex];
		//loop on different q values.
		for(int qindex=0; qindex<=q_set.size()-1; qindex++)
		{
			q=q_set[qindex];
			//loop on different realizations.
			for(int run = 0; run<=runNum-1; run++)
			{
			initialize(); //initialize variables for the next run
				//the main time loop of the program.
				for(int t=1; t<=100000000000 && actives.size() >= 1; t++) //I_num[0]+I_num[1] >= 1 is to check if there remains any active nodes to further change the state.
				{
					state_cp = state;
					actives_cp = actives;
					
					//loop on the infected nodes, in order to spread the infection, and afterwards turning them to recovered nodes.
					for (set<int>::iterator it=actives_cp.begin(); it!=actives_cp.end(); it++)
					{
				
						i = *it;
						//cout<< state[i]<<endl;
						
						dis_index = (rand()%2)+2; //which disease to start spreading first for node.
						
						for (int dummy=0; dummy <= 1 ; dummy++, dis_index = ((dis_index+1)%2)+2) //this for, runs over two dis_indexes, dummy doesn't matter.
						{
							//cout<<"dummy: "<<dummy<<endl;
							if(been_I (state_cp[i], dis_index, 1) ) // if the node is sick right now with diseas=dis_index. we use state_cp because it doens't count if the node has been infected in current time step.
							{
								turn_grid_neighbs_I(i, dis_index);
								//turn_general_neighbs_I(i, dis_index);
								
								turn_R(i, dis_index);				//turn_R after spreading between the neighbors. (one step)
								
			
							}				
						}
						
					}

				//cout<<"t: "<<t<<endl;
				//cout<<"R: "<<n-S_num<<endl;
					//output				
				/*
					for(int i=0; i<=L-1; i++)
					{
						
						for(int j=0; j<=L-1; j++)
							cout<<state[i*L+j]<<"\t";
						cout<<endl;
					}
				*/
				
				//fout<<n-S_num<<" ";
				
				}
				if(run%(runNum/10)==0)
					cout << "n: " << n << "p: " << p << "q: " << q << "run: " << run << endl;
				//cout<<"R: "<<(float)(n-S_num)/n<<endl;
				fout<<(n-S_num)<<"\n";
				//cout<<(n-S_num)<<"\n";
			}
		}
	}
}

