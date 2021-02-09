//mettre les fichiers suivant dans la librairie
#include "Funibot.h"

#define periodeCommunication 500
#define periodeControle 300
#define periodeMoteur 50
#define periodeEncodeur 10

#define NBR_CABLES 4

struct aglomerationVariable
{
    //timers
    long lastCommunication = 0;
    long lastControle = 0;
    long lastMoteur = 0;
    long lastEncodeur = 0;

    //robot
    Funibot bot;
    FuniMath::Vecteur objectif;
    unsigned char regime = 0; //0 := arret, 1 := direction, 2 := position
    double vitesse = 1;
    //retour encodeur
    double cable[NBR_CABLES] = {0,0,0,0};
    //commande au moteur
    double commandeVitesseCable[NBR_CABLES] = {0};
};

//création des variables globales
aglomerationVariable global;

//fonctions lancées à chaques périodes

//fonction de communication, communication entre utilisateur et microcontroleur
void communication()
{
}

//fonction de controle, choisie la vitesse des moteurs
void controle()
{
    //mise à jour de la longueur des cables
    for(unsigned i = 0; i < NBR_CABLES; i++)
    {
        global.bot.setLongueurCable(i,global.cable[i]);
    }
    //en fonction du régime
    switch (global.regime)

    {
    //arrêt
    case 0:
        for(unsigned i = 0; i < NBR_CABLES; i++)
        {
            global.commandeVitesseCable[i] = 0;
        }
        break;
    //direction
    case 1:
        global.bot.deplacementDirectionnel(global.objectif,(double)periodeControle/(double)1000.0,global.vitesse,global.commandeVitesseCable);
        break;
    //position
    case 2:
        global.bot.deplacementPosition(global.objectif,(double)periodeControle/(double)1000.0,global.vitesse,global.commandeVitesseCable);
        break;
    //défaut
    default:
        for(unsigned i = 0; i < NBR_CABLES; i++)
        {
            global.commandeVitesseCable[i] = 0;
        }
        break;
    }
}

//fonction des moteurs, controle les moteurs et s'assure d'obtenir la bonne vitesse
void moteurs()
{
}

//fonction des encodeurs, assure un bon suivie de la longueur des cables
void encodeurs()
{
}

//setup
void setup()
{
    //valeurs initiales des cable

    global.lastCommunication = millis();
    global.lastMoteur = millis();
    global.lastControle = millis();
    global.lastEncodeur = millis();
}

//loop
void loop()
{
    long temps = millis();
    //Fonction de communication
    if(temps - global.lastCommunication >= periodeCommunication)
    {
        communication();
        global.lastCommunication = millis();
    }
    //Fonction de contrôle
    if (temps - global.lastControle >= periodeControle)
    {
        controle();
        global.lastControle = millis();
    }
    //Fonction des encodeurs
    if(temps - global.lastEncodeur >= periodeEncodeur)
    {
        encodeurs();
        global.lastEncodeur = millis();
    }
    //Fonction des moteurs
    if(temps - global.lastMoteur >= periodeControle)
    {
        moteurs();
        global.lastMoteur = millis();
    }
}
