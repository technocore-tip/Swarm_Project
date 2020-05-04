
#include <webots/Robot.hpp>

// All the webots classes are defined in the "webots" namespace
using namespace webots;

// This is the main program of your controller.
// It creates an instance of your Robot instance, launches its
// function(s) and destroys it at the end of the execution.
// Note that only one instance of Robot should be created in
// a controller program.
// The arguments of the main function can be specified by the
// "controllerArgs" field of the Robot node
int main(int argc, char **argv) {

  Robot *robot = new Robot();

  int timeStep = (int)robot->getBasicTimeStep();


  while (robot->step(timeStep) != -1) {

  };

  delete robot;
  return 0;
}
