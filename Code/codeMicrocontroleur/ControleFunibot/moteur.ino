#include "moteur.h"


#if defined(__OPENCM904__)
  #define DEVICE_NAME "3" //Dynamixel on Serial3(USART3)  <-OpenCM 485EXP
#elif defined(__OPENCR__)
  #define DEVICE_NAME ""
#endif   

#define MOTORBAUDRATE  4500000
#define mmprad -18

DynamixelWorkbench dxl_wb;

uint8_t liste_moteurs[4] = {1, 4, 2, 3};
float position_moteurs[4];

void moteurSetup(uint8_t nbrMoteur)
{
    dxl_wb.init(DEVICE_NAME,MOTORBAUDRATE);

    while(!Serial);
    for (uint8_t i=0; i<nbrMoteur; i++)
    {
      dxl_wb.ping(liste_moteurs[i]);
      dxl_wb.torqueOff(liste_moteurs[i]);
      dxl_wb.setExtendedPositionControlMode(liste_moteurs[i]);
      dxl_wb.writeRegister(liste_moteurs[i], "Profile_Velocity", 0);
      dxl_wb.writeRegister(liste_moteurs[i], "Profile_Acceleration", 0);
      dxl_wb.torqueOn(liste_moteurs[i]);
      //dxl_wb.wheelMode(liste_moteurs[i], 1);
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
      /*if (deplacement > PI)
        deplacement -= 2*PI;
      if (deplacement < -PI)
        deplacement += 2*PI;*/
      longueurCable[i] += deplacement*mmprad;
      float cible = radian + (vitesse[i]/mmprad)*dt;
      dxl_wb.goalPosition(liste_moteurs[i], cible);
      //dxl_wb.goalVelocity(liste_moteurs[i], (float)(vitesse[i]/mmprad));

    }
}
