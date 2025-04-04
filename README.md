Right now this project is in active development, and it isn't very far along.
The code is pretty simple, but for using it as a simulation here's the command to place planets:
addPlanet(x, y, m, dx, dy)
X and Y specify the position of the planet, m the mass (which can be positive or negative) and dx and dy are optional arguments that default to 0 and and determine the planet's initial velocity.

There are also a few changeable variables:

- Scale determines the size of the screen. The screen size is 600/scale.
- visualScale determines the size of the planets when they are rendered. This is a purely aesthetic setting, and does not change how the program operates. I recommend keeping this between 0.5 and 2.
- gravity is the gravitational constant. Right now it is set so that the program behaves (hopefully) accurately such that the mass variable is multiplied by 1*10^24, one pixel on the screen is 1*10^6 Km, and one in-game second is 1*10^6 real-life seconds, with gravity functioning like it does in the real universe.

A few other changeable things:

- In the showMotion function, the _passTime_ method has a parameter, _time_ that determines the simulation fidelity (how accurate the simulation is to real gravity). The lower this parameter is, the more accurate the program, but the worse it will perform.
- The time.sleep() method in showMotion determines the frame rate of the program. Relative to the _time_ parameter in passTime it determines the speed of the program. Right now _time_ is 0.01 and time.sleep() has a value of 0.001, meaning the program runs at 0.01/0.001 = 10x speed.
- In a few places, the cleanValues method appears (In passTime and mergePlanets). This function serves to round the values of each planet (position and velocity) to avoid floating-point errors. This function can be altered to change how many digits each value is rounded by. Increasing this would mean more accuracy but more floating point errors which could decrease the accuracy.
