#include "moteur.h"


#if defined(__OPENCM904__)
  #define DEVICE_NAME "3" //Dynamixel on Serial3(USART3)  <-OpenCM 485EXP
#elif defined(__OPENCR__)
  #define DEVICE_NAME ""
#endif   

#define MOTORBAUDRATE  4500000
#define NBR_MOTOR 4
#define REG_TENSION
#define ASS_VITESSE

DynamixelWorkbench dxl_wb;

uint8_t liste_moteurs[NBR_MOTOR] = {3, 2, 1, 4};
float old_position_moteurs[NBR_MOTOR];
double old_longueur_cable[NBR_MOTOR];
double mmprad[NBR_MOTOR] = {18,18,18,18};

#ifdef REG_TENSION
bool sous_tension[NBR_MOTOR];
#endif

void moteurSetup(uint8_t nbrMoteur, double *longueurCable)
{
    dxl_wb.init(DEVICE_NAME,MOTORBAUDRATE);

    while(!Serial);
    for (uint8_t i=0; i<nbrMoteur; i++)
    {
      dxl_wb.ping(liste_moteurs[i]);
      dxl_wb.torqueOff(liste_moteurs[i]);
      #ifdef ASS_VITESSE
      dxl_wb.setVelocityControlMode(liste_moteurs[i]);
      dxl_wb.writeRegister(liste_moteurs[i], "Profile_Acceleration", 0);
      dxl_wb.writeRegister(liste_moteurs[i], "Velocity_Limit",200);
      #else
      dxl_wb.setExtendedPositionControlMode(liste_moteurs[i]);
      dxl_wb.writeRegister(liste_moteurs[i], "Profile_Velocity", 0);
      dxl_wb.writeRegister(liste_moteurs[i], "Profile_Acceleration", 0);
      #endif
      dxl_wb.torqueOn(liste_moteurs[i]);
    }
    for (uint8_t i=0; i<nbrMoteur; i++)
    {
      dxl_wb.getRadian(liste_moteurs[i], old_position_moteurs+i);
      old_longueur_cable[i] = longueurCable[i];
      #ifdef REG_TENSION
      sous_tension[i] = false;
      #endif
    }
}

void moteurLoop(uint8_t nbrMoteur, double *vitesse, double *longueurCable)
{
  //delta temps
  #ifndef ASS_VITESSE
  static long t = millis();
  long nt = millis();
  long dt = nt - t;
  t = nt;
  #endif

  //controle des moteurs
  for (uint8_t i=0; i<nbrMoteur; i++)
    {

      //prise de données
      float radian;
      dxl_wb.getRadian(liste_moteurs[i], &radian);
      double deltaAng = radian - old_position_moteurs[i];
      double deltaCable = longueurCable[i] - old_longueur_cable[i];
      #ifdef ASS_VITESSE
      if (deltaAng > PI)
        deltaAng -= PI;
      else if (deltaAng < -PI)
        deltaAng += PI;
      #endif

      #ifndef REG_TENSION
      //calibration
      if (abs(deltaCable) > 5 && abs(deltaAng) > 0.3)
      {
          mmprad[i] = deltaCable / deltaAng;
          old_position_moteurs[i] = radian;
          old_longueur_cable[i] = longueurCable[i];
      }
      #else
      //calibration
      if(!sous_tension[i] && abs(deltaAng)> 0.3)
      {
        if(abs(deltaCable)>2)
        {
          mmprad[i] = deltaCable / deltaAng;
          old_position_moteurs[i] = radian;
          old_longueur_cable[i] = longueurCable[i];
        }
        else
        {
          sous_tension[i] = true;
        }
      }
      //resolution des sous tension
      if(sous_tension[i])
        {
          if(abs(deltaCable) < 2 )
          {
            if (mmprad[i] < 0)
            {
              if (vitesse[i] < 0.5)
              vitesse[i] = 0.5;
            }
            else
            {
              if (vitesse[i] > -0.5)
              vitesse[i] = -0.5;
            }
          }
          else
          {
            old_longueur_cable[i] = longueurCable[i];
            old_position_moteurs[i] = radian;
            sous_tension[i] = false;
          }
        }
      #endif

      //consigne du deplacement;
      #ifdef ASS_VITESSE
      float cible = vitesse[i]/mmprad[i];
      dxl_wb.goalVelocity(liste_moteurs[i], cible);
      #else
      float cible = radian + (vitesse[i]/mmprad[i])*((float)dt/1000.f);
      dxl_wb.goalPosition(liste_moteurs[i], cible);
      #endif
    }
}
