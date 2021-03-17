#include "moteur.h"


#if defined(__OPENCM904__)
  #define DEVICE_NAME "3" //Dynamixel on Serial3(USART3)  <-OpenCM 485EXP
#elif defined(__OPENCR__)
  #define DEVICE_NAME ""
#endif   

#define MOTORBAUDRATE  4500000

DynamixelWorkbench dxl_wb;

uint8_t liste_moteurs[4] = {1, 3, 2, 4};
float old_position_moteurs[4];
double old_longueur_cable[4];
double mmprad[4] = {18,18,18,18};

void moteurSetup(uint8_t nbrMoteur, double *longueurCable)
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
    }
    for (uint8_t i=0; i<nbrMoteur; i++)
    {
      dxl_wb.getRadian(liste_moteurs[i], old_position_moteurs+i);
      old_longueur_cable[i] = longueurCable[i];
    }
}

void moteurLoop(uint8_t nbrMoteur, double *vitesse, double *longueurCable)
{
  //delta temps
  static long t = millis();
  long nt = millis();
  long dt = nt - t;
  t = nt;

  //controle des moteurs
  for (uint8_t i=0; i<nbrMoteur; i++)
    {

      //calibration
      float radian;
      dxl_wb.getRadian(liste_moteurs[i], &radian);
      double deltaAng = radian - old_position_moteurs[i];
      double deltaCable = longueurCable[i] - old_longueur_cable[i];

      if (abs(deltaCable) > 5 && abs(deltaAng) > 0.3)
      {
          mmprad[i] = deltaCable / deltaAng;
          old_position_moteurs[i] = radian;
          old_longueur_cable[i] = longueurCable[i];
      }

      //consigne du deplacement;
      float cible = radian + (vitesse[i]/mmprad[i])*((float)dt/1000.f);
      dxl_wb.goalPosition(liste_moteurs[i], cible);

    }
}
