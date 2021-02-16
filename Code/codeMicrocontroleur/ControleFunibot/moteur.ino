#include "moteur.h"


#if defined(__OPENCM904__)
  #define DEVICE_NAME "3" //Dynamixel on Serial3(USART3)  <-OpenCM 485EXP
#elif defined(__OPENCR__)
  #define DEVICE_NAME ""
#endif   

#define BAUDRATE  57600

DynamixelWorkbench dxl_wb;

uint8_t liste_moteurs[4] = {3, 2, 4, 1};

void moteurSetup()
{
    dxl_wb.init(DEVICE_NAME,BAUDRATE);

    for (uint8_t i=0; i<4; i++)
    {
      dxl_wb.ping(liste_moteurs[i]);
      dxl_wb.wheelMode(liste_moteurs[i], 0);
    }
}

void moteurLoop()
{
  for (int8_t count = 0; count <= 4; count++)
    {
      if(count >= 0 && count < 4)dxl_wb.goalVelocity((uint8_t)liste_moteurs[count], (int32_t)200);
      if(count - 1 >= 0)dxl_wb.goalVelocity((uint8_t)liste_moteurs[count-1], (int32_t)100);
      if(count - 2 >= 0)dxl_wb.goalVelocity((uint8_t)liste_moteurs[count-2], (int32_t)0);
      delay(100);
    }

  
    dxl_wb.goalVelocity(liste_moteurs[0], (int32_t)0);
    dxl_wb.goalVelocity(liste_moteurs[1], (int32_t)0);
    dxl_wb.goalVelocity(liste_moteurs[2], (int32_t)0);
    dxl_wb.goalVelocity(liste_moteurs[3], (int32_t)0);
}