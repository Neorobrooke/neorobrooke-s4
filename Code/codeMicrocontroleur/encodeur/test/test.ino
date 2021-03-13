#include "Encodeur.h"

Encodeur enc(4,A1);
void interupt0()
{
    enc.interruptFct();
}
void interupt02()
{
    enc.interruptFct2();
}

void setup()
{
   attachInterrupt(enc.pinInterrupt(),interupt0,CHANGE);
   //attachInterrupt(enc.pinInterrupt2(),interupt02,CHANGE);
}


void loop()
{
    Serial.println(enc.read());
    delay(1000);
}
