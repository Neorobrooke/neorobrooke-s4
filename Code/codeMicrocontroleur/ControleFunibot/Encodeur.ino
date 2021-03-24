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
}

int Encodeur::pinInterrupt()
{
    return digitalPinToInterrupt(pin1);
}
int Encodeur::pinInterrupt2()
{
    return digitalPinToInterrupt(pin2);
}

void Encodeur::interruptFct()
{

    int pin2_h = digitalReadFast(pin2);
    int pin1_h = digitalReadFast(pin1);

    if (pin1_h ^ pin2_h) {
        valeur ++;
    } 
    else {
        valeur --;
    }
}

void Encodeur::interruptFct2()
{

    int pin2_h = digitalReadFast(pin2);
    int pin1_h = digitalReadFast(pin1);

    if (pin1_h ^ pin2_h) {
        valeur --;
        Serial.println("-");
        Serial.println(pin1_h);
        Serial.println(pin2_h);
    } 
    else {
        valeur ++;
        Serial.println("+");
        Serial.println(pin1_h);
        Serial.println(pin2_h);
    }
}

void Encodeur::setup()
{
  pinMode(pin1, INPUT_PULLUP);
  pinMode(pin2, INPUT_PULLUP);
}
