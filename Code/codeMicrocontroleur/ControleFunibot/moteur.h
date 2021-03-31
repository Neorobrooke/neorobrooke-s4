#include <DynamixelWorkbench.h>

void moteurSetup(uint8_t nbrMoteur, double *longueurCable);
void moteurLoop(double *vitesse, double *longueurCable);

void moteurOn();
void moteurOff();
void moteurReset();