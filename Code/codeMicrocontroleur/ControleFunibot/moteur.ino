#include "moteur.h"


#if defined(__OPENCM904__)
  #define DEVICE_NAME "3" //Dynamixel on Serial3(USART3)  <-OpenCM 485EXP
#elif defined(__OPENCR__)
  #define DEVICE_NAME ""
#endif   

#define BAUDRATE  57600
#define mmprad -2.387

DynamixelWorkbench dxl_wb;

uint8_t liste_moteurs[4] = {1, 2, 3, 4};
float position_moteurs[4];

void moteurSetup(uint8_t nbrMoteur)
{
    dxl_wb.init(DEVICE_NAME,BAUDRATE);

    for (uint8_t i=0; i<nbrMoteur; i++)
    {
      dxl_wb.ping(liste_moteurs[i]);
      dxl_wb.wheelMode(liste_moteurs[i], 0);
    }
    for (uint8_t i=0; i<nbrMoteur; i++)
    {
      dxl_wb.getRadian(liste_moteurs[i], position_moteurs+i);
    }
}

void moteurLoop(uint8_t nbrMoteur, double *vitesse, double *longueurCable, int dt)
{
  for (uint8_t i=0; i<nbrMoteur; i++)
    {
      float radian;
      dxl_wb.getRadian(liste_moteurs[i], &radian);
      float deplacement = radian - position_moteurs[i];
      position_moteurs[i] = radian;
      if (deplacement > PI)
        deplacement -= 2*PI;
      if (deplacement < -PI)
        deplacement += 2*PI;
      longueurCable[i] += deplacement*mmprad;
      dxl_wb.goalVelocity(liste_moteurs[i], (float)(vitesse[i]/mmprad));

    }
}