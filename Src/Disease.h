#ifndef DISEASE_H
#define DISEASE_H
#include "global.h"
enum class State { S, IR, IS, R, D }; //IS: infection type which recovers back to S,
                                  //IR: infection type which recovers to R.
                                  //D: totally dead agent.
enum class TransitionMethod { delay, probability };

class Disease
{
  private:
  const bool dependent = false;
  const TransitionMethod transition_method = TransitionMethod::probability;

  public:
  State state = State::S;
  State future_state = State::S;
  //State operator ++();
  State operator ++(int);

  void update();

  bool is_infector();
  friend Disease operator +=(Disease &a, Disease &b);
  void print_state();

};

#endif
