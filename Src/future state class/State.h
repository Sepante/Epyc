#ifndef STATE_H
#define STATE_H
#include <string>
using std::string;
class State
{
  private:

  public:
     //State * const demand;
     //State * const target;
     //State * const offer;
     State * const demand;
     State * const target;
     State * const offer;
     const string name;
     int n=5;
     State(string name, State * const t,State * const o, State * const d);
     void temp(int &t);
     void operator ++();
};

#endif
