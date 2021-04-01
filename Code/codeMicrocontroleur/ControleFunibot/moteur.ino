#include "moteur.h"
#include "GestionLog.h"


#if defined(__OPENCM904__)
  #define DEVICE_NAME "3" //Dynamixel on Serial3(USART3)  <-OpenCM 485EXP
#elif defined(__OPENCR__)
  #define DEVICE_NAME ""
#endif   

#define MOTORBAUDRATE  4500000
#define NBR_MOTOR 4
#define REG_TENSION
//#define ASS_VITESSE
#define mmprad_min 15
#define mmprad_max 30
#define mmprad_buff 5
#define mmprad_normal 18

double p_corr = 0.8/(mmprad_normal - mmprad_min);
double coef_mmprad[mmprad_buff] = {0.5,0.3,0.1,0.075,0.025};

DynamixelWorkbench dxl_wb;

uint8_t liste_moteurs[NBR_MOTOR] = {3, 2, 1, 4};
uint8_t nbrMoteur = 4;
float old_position_moteurs[NBR_MOTOR];
double old_longueur_cable[NBR_MOTOR];
double mmprad[NBR_MOTOR];
double buffer_mmprad[NBR_MOTOR][mmprad_buff];

#ifdef REG_TENSION
bool sous_tension[NBR_MOTOR];
double vitesse_corr[NBR_MOTOR];
#endif
void moteurSetMode()
{
  for (uint8_t i=0; i<nbrMoteur; i++)
    {
      dxl_wb.ping(liste_moteurs[i]);
      dxl_wb.torqueOff(liste_moteurs[i]);
      #ifdef ASS_VITESSE
      dxl_wb.setVelocityControlMode(liste_moteurs[i]);

      //modification des registres
      int32_t* data;
      dxl_wb.readRegister(liste_moteurs[i], "Profile_Acceleration",data);
      if (*data != 0) dxl_wb.writeRegister(liste_moteurs[i], "Profile_Acceleration", 0);

      dxl_wb.readRegister(liste_moteurs[i], "Velocity_Limit",data);
      if (*data != 512) dxl_wb.writeRegister(liste_moteurs[i], "Velocity_Limit",512);

      dxl_wb.readRegister(liste_moteurs[i], "Moving_Threshold",data);
      if (*data != 5) dxl_wb.writeRegister(liste_moteurs[i], "Moving_Threshold",5);

      dxl_wb.readRegister(liste_moteurs[i], "Current_Limit",data);
      if (*data != 372) dxl_wb.writeRegister(liste_moteurs[i],"Current_Limit",372);

      #else
      dxl_wb.setExtendedPositionControlMode(liste_moteurs[i]);
      dxl_wb.writeRegister(liste_moteurs[i], "Profile_Velocity", 150);
      dxl_wb.writeRegister(liste_moteurs[i], "Profile_Acceleration", 0);

      int32_t* data;
      dxl_wb.readRegister(liste_moteurs[i], "Velocity_Limit",data);
      if (*data != 200) dxl_wb.writeRegister(liste_moteurs[i], "Velocity_Limit",200);

      dxl_wb.readRegister(liste_moteurs[i], "Moving_Threshold",data);
      if (*data != 10) dxl_wb.writeRegister(liste_moteurs[i], "Moving_Threshold",10);

      dxl_wb.readRegister(liste_moteurs[i], "Current_Limit",data);
      if (*data != 1193) dxl_wb.writeRegister(liste_moteurs[i],"Current_Limit",1193);
      #endif
      dxl_wb.torqueOn(liste_moteurs[i]);
    }
  GestionLog::printlnlog("Mise à jour du mode de fonctionnement des moteurs");
} 

void moteurSetup(uint8_t nbrMoteur_, double *longueurCable)
{
    dxl_wb.init(DEVICE_NAME,MOTORBAUDRATE);
    nbrMoteur = nbrMoteur_;

    moteurSetMode();
    for (uint8_t i=0; i<nbrMoteur; i++)
    {
      dxl_wb.getRadian(liste_moteurs[i], old_position_moteurs+i);
      old_longueur_cable[i] = longueurCable[i];
      mmprad[i] = mmprad_normal;
      for (int j = 0 ; j < mmprad_buff; j++)
      {
        buffer_mmprad[i][j] = mmprad_normal;
      }
      #ifdef REG_TENSION
      sous_tension[i] = false;
      vitesse_corr[i] = 1;
      #endif
    }
    GestionLog::printlnlog("Initialisation des moteurs des moteurs");
}
void moteurReset()
{
  for(uint8_t i = 0; i < nbrMoteur; i++)
  {
    dxl_wb.ping(liste_moteurs[i]);
    dxl_wb.reboot(liste_moteurs[i]);

    mmprad[i] = mmprad_normal;
      for (int j = 0 ; j < mmprad_buff; j++)
      {
        buffer_mmprad[i][j] = mmprad_normal;
      }
      #ifdef REG_TENSION
      sous_tension[i] = false;
      vitesse_corr[i] = 1;
      #endif
  }
  moteurSetMode();
  GestionLog::printlnlog("reinitialisation des moteurs");
}

void moteurOn()
{
  for(uint8_t i = 0; i < nbrMoteur; i++)
  dxl_wb.torqueOn(liste_moteurs[i]);
  GestionLog::printlnlog("Moteurs on");
}

void moteurOff()
{
  for(uint8_t i = 0; i < nbrMoteur; i++)
  dxl_wb.torqueOff(liste_moteurs[i]);
  GestionLog::printlnlog("Moteurs off");
}

void moteurLoop(double *vitesse, double *longueurCable)
{
  //delta temps
  #ifndef ASS_VITESSE
  static long t = millis();
  long nt = millis();
  long dt = nt - t;
  t = nt;
  #endif
  static int compteur = 0;
  compteur ++;
  if (compteur >= 200)
  {
    compteur = 0;
    GestionLog::printlnlog("mmprad:");
    for (int i = 0 ; i < nbrMoteur; i++)
    {
      GestionLog::printlnlog(mmprad[i]);
    }
    GestionLog::printlog("dt = ");
    GestionLog::printlog(dt);
  }

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
      if(!sous_tension[i] && abs(deltaAng)> 0.17)
      {
        if(abs(deltaCable)>2.5)
        {
          mmprad[i] = deltaCable / deltaAng;

          //filtrage
          for(int j = 1; j < mmprad_buff; j++)
          {
            buffer_mmprad[i][j] = buffer_mmprad[i][j-1];
          }
          buffer_mmprad[i][0] = mmprad[i];

          mmprad[i] = 0;
          for(int j = 0; j < mmprad_buff; j++)
          {
            mmprad[i] += buffer_mmprad[i][j] * coef_mmprad[j];
          }

          //correction vitesse
          if (mmprad[i] < mmprad_normal)
          {
              vitesse_corr[i] = 1 - p_corr*(mmprad_normal - mmprad[i]);
          }
          else vitesse_corr[i] = 1;

          //ajout de frontiere
          if(mmprad[i] < mmprad_min) mmprad[i] = mmprad_min;
          else if (mmprad_max < mmprad[i]) mmprad[i] = mmprad_max;

          //mise à jours de mémoires pour delta
          old_position_moteurs[i] = radian;
          old_longueur_cable[i] = longueurCable[i];
        }
        else
        {
          sous_tension[i] = true;
          GestionLog::printlog("sous tension moteur ");
          GestionLog::printlog(i);
        }
      }
      //resolution des sous tension
      if(sous_tension[i])
        {
          if(abs(deltaCable) < 4 )
          {
            if (mmprad[i] < 0)
            {
              if (vitesse[i] < 80)
              vitesse[i] = 80;
            }
            else
            {
              if (vitesse[i] > -80)
              vitesse[i] = -80;
            }
          }
          else
          {
            old_longueur_cable[i] = longueurCable[i];
            old_position_moteurs[i] = radian;
            sous_tension[i] = false;
            GestionLog::printlog("tension moteur ");
            GestionLog::printlnlog(i);
          }
        }
        else
        {
          vitesse[i] *= vitesse_corr[i];
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
