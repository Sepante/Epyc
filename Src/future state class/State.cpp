#include "State.h"
#include "global.h"
#include <iostream>

State::State(string name, State * const t,State * const o,State * const d)
  :name(name), target(t), offer(o), demand(d)
  //void State::temp(int &t)
{
//  target = &t;
  /*
  name = name1;
  target = t;
  offer = o;
  demand = d;
  //offer = NULL;
  std::cout << target << '\n';
  std::cout << offer << '\n';
*/
}
int main()
{
  int a;
  State S("S" ,&S, &S, NULL);
  std::cout << S.target << '\n';
  std::cout << S.offer << '\n';
  //State R("R", )
}
