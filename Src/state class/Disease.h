#ifndef DISEASE_H
#define DISEASE_H
#include "global.h"
enum class State { S, IR, IS, R, D }; //IS: infection type which recovers back to S,
                                      //IR: infection type which recovers to R.
                                      //D: totally dead agent.
enum class TransitionMethod { delay, probability };
class Person;
class Disease
{
  protected:
    const bool dependent = false;
    const TransitionMethod transition_method = TransitionMethod::probability;
    Person *person;

  public:
    State state = State::S;
    State future_state = State::S;
    //State operator ++();
    void operator ++(int);
    void update();
    //bool is_infector();
    //virtual void operator +=(Disease neighbor);
    virtual void operator +=(Disease &neighbor) = 0;
    virtual void interact( Disease &neighbor ) = 0;
    void print_state();
    //virtual Disease funny_func() = 0;

};

class State_S: public Disease
{
  void interact( Disease &neighbor )
  {}

  void operator +=(Disease &b)
  {

  	switch (b.state)
  	{
      //if the neighbor is either IR or IS, change the state into that.
      //case person.:
  		case State::IS:
  				future_state = b.state;
  			break;
  		//default:
  	}
  }
};

class State_I_R: public Disease
{
  void interact( Disease &neighbor )
  {}

  void operator +=(Disease &neighbor)
  {}


};

class State_R: public Disease
{
  void interact( Disease &neighbor )
  {}

  void operator +=(Disease &neighbor)
  {}

};

class State_I_S: public Disease
{
  void interact( Disease &neighbor )
  {}

  void operator +=(Disease &neighbor)
  {}

};


#endif
