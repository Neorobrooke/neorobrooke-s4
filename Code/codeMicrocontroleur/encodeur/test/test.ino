#include "Encodeur.h"

Encodeur enc(2,0);
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
   enc.setup();
   attachInterrupt(enc.pinInterrupt(),interupt0,CHANGE);
   //attachInterrupt(enc.pinInterrupt2(),interupt02,CHANGE);
}


void loop()
{
    Serial.println(enc.read());
    Serial.println(digitalRead(0));
    Serial.println(digitalRead(2));
    Serial.println("fin");
    delay(1000);
}
