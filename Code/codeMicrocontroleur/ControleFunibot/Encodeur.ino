#include "Encodeur.h"

int Encodeur::read()
{
    noInterrupts();
    int out = valeur;
    interrupts();
    return out;
}

Encodeur::Encodeur(int pinInterrupt, int pinDigital):
pin1(pinInterrupt),pin2(pinDigital),valeur(0)
{
  pinMode(pin1, INPUT);
  pinMode(pin2, INPUT);
}

int Encodeur::pinInterrupt()
{
    return digitalPinToInterrupt(pin1);
}

void Encodeur::interruptFct()
{
    bool pin1_h = digitalRead(pin1);
    bool pin2_h = digitalRead(pin2);

    if (pin1_h ^ pin2_h) {
        valeur ++;
    } 
    else {
        valeur --;
    }
}