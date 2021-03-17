# pragma once

class Encodeur
{
    private:
    volatile int valeur;
    int pin1;  //le port 1 doit être une port d'interupt
    int pin2;  //le port 2 doit être un port digital
    public:
    int read(); //block les interrupts pour évité la modification de la valeur durant la lecture, retourne la valeur de l'encodeur
    Encodeur(int pinInterrupt, int pinDigital); //les pins sont en format digital
    void interruptFct();     //fonction pour attachInterrupt
    void interruptFct2();
    int pinInterrupt(); //la pin est dans le bon format pour la fonction attachInterrupt
    int pinInterrupt2();
    void setup();
};