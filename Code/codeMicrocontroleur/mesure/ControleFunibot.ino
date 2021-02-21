
#include <ArduinoJson.h> //nécessite ArduinoJson : arduinojson.org
#include "Funibot.h"
#include "moteur.h"

#define BAUDRATE  57600

#define periodeCommunication 500
#define periodeControle 300
#define periodeMoteur 50
#define periodeEncodeur 10

#define NBR_CABLES 2

struct aglomerationVariable
{
    //timers
    long lastCommunication = 0;
    long lastControle = 0;
    long lastMoteur = 0;
    long lastEncodeur = 0;

    //retour encodeur
    double cable[NBR_CABLES] = {100,100};
    //commande au moteur
    double commandeVitesseCable[NBR_CABLES] = {0};
    double commandeMoteur[NBR_CABLES] = {0};

    //communication
    volatile bool event = false;
};

//création des variables globales
aglomerationVariable global;

//fonctions lancées à chaques périodes

//fonction de communication, communication entre utilisateur et microcontroleur
void serialEvent(){
  global.event=true;
}

void communication()
{
    if (global.event)
    {
        StaticJsonDocument<512> input;
        deserializeJson(input,Serial);
        if(input["m"] == 0)
            {
            for(int i = 0; i < NBR_CABLES; i++)
                global.commandeMoteur[i] = PI;
            serializeJson(input,Serial);
            Serial.println();
            }
        else if(input["m"] == 1)
            {
            for(int i = 0; i < NBR_CABLES; i++)
                global.commandeMoteur[i] = -PI;
            serializeJson(input,Serial);
            Serial.println();
            }
        global.event = false;
    }
}


//fonction des moteurs, controle les moteurs et s'assure d'obtenir la bonne vitesse
void moteurs()
{
    moteurLoop(NBR_CABLES,global.commandeMoteur);
}

//fonction des encodeurs, assure un bon suivie de la longueur des cables
void encodeurs()
{
}

//setup
void setup()
{
    //communication série
    Serial.begin(BAUDRATE);
    
    //enregistrement du temps
    long temps = millis();
    global.lastCommunication = temps;
    global.lastEncodeur = temps;

    moteurSetup(NBR_CABLES);
}

//loop
void loop()
{
    long temps = millis();
    //Fonction de communication
    if(temps - global.lastCommunication >= periodeCommunication)
    {
        communication();
        global.lastCommunication = temps;
    }
    //Fonction des moteurs
    if(temps - global.lastMoteur >= periodeControle)
    {
        moteurs();
        global.lastMoteur = temps;
    }
}