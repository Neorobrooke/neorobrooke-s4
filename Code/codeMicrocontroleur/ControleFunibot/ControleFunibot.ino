
#include <ArduinoJson.h> //nécessite ArduinoJson : arduinojson.org
#include "Funibot.h"
#include "moteur.h"

#define BAUDRATE  57600

#define periodeCommunication 500
#define periodeControle 100
#define periodeMoteur 100
#define periodeEncodeur 10

#define NBR_CABLES 2

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
    double vitesse = 200;
    double seuilPosition = 0.5;
    //retour encodeur
    double cable[NBR_CABLES] = {710,790};
    //commande au moteur
    double commandeVitesseCable[NBR_CABLES] = {0};

    //communication
    bool SerialEvent = false;

    //profile accumulatif
    long timeProfile[6];
};

//création des variables globales
aglomerationVariable global;

//fonctions lancées à chaques périodes

//fonction de communication, communication entre utilisateur et microcontroleur


void mainCommunication()
{
    StaticJsonDocument<512> input;
    deserializeJson(input,Serial);

    String comm = (const char*)input["comm"];
    if(comm == "pot")
    {
        
        String type = input["type"];
        if(type == "get" )
        {
            int id = input["args"]["id"];
            FuniMath::Vecteur pot = global.bot.getPole(id);
            //construction de la réponse
            StaticJsonDocument<512> output;

            output["comm"] = "pot";
            output["type"] = "ack";

            output["args"]["id"] = id;
            output["args"]["pos_x"] = pot.x;
            output["args"]["pos_y"] = pot.y;
            output["args"]["pos_z"] = pot.z;

            //encoie de la réponse
            serializeJson(output,Serial);
            Serial.println();
            
        }
        else if(type == "set")
        {
            int id = input["args"]["id"];
            double x = input["args"]["pos_x"];
            double y = input["args"]["pos_y"];
            double z = input["args"]["pos_z"];

            if(global.bot.getNbrPole() <= id ) //pole inexistant
                global.bot.addPole(FuniMath::Vecteur(x,y,z),FuniMath::Vecteur(0,0,0));
            else //pole existant
                global.bot.setPole(id,FuniMath::Vecteur(x,y,z),FuniMath::Vecteur(0,0,0));
            //envoie d'une réponse
            input["args"]["id"] = id;
            input["type"] = "ack";
            serializeJson(input,Serial);
            Serial.println();
        }
    }
    else if (comm == "dep")
    {
            String type = (const char*)input["type"];
            if(type == "set")
            {
                String mode = (const char*)input["args"]["mode"];
                if (mode == "stop") 
                {
                    global.regime = 0; //arret
                    input["type"] = "ack";
                    serializeJson(input,Serial);
                    Serial.println();
                }
                else
                {
                    double x = input["args"]["axe_x"];
                    double y = input["args"]["axe_y"];
                    double z = input["args"]["axe_z"];
                    global.objectif = FuniMath::Vecteur(x,y,z);

                    if(mode == "start")
                    {
                        global.regime = 1; //déplacement dans la direction de objectif
                        input["type"] = "ack";
                        serializeJson(input,Serial);
                        Serial.println();
                    }
                    else if(mode == "distance")
                    {
                        FuniMath::Vecteur position = global.bot.getPosition();
                        global.objectif = global.objectif + position;
                        global.regime = 1; //déplacement jusqu'à la position de objectif
                        input["type"] = "ack";
                        serializeJson(input,Serial);
                        Serial.println();
                    }
                }
                
            }
        
    }
    else if (comm == "pos")
    {
        String type = (const char*)input["type"];
        if(type == "get")
        {
            StaticJsonDocument<1024> output;
            FuniMath::Vecteur position = global.bot.getPosition();

            output["comm"] = "pos";
            output["type"] = "ack";

            output["args"]["pos_x"] = position.x;
            output["args"]["pos_y"] = position.y;
            output["args"]["pos_z"] = position.z;

            serializeJson(output,Serial);
            Serial.println();
        }
        if(type == "set")
        {
            double x = input["args"]["pos_x"];
            double y = input["args"]["pos_y"];
            double z = input["args"]["pos_z"];
            global.objectif = FuniMath::Vecteur(x,y,z);
            global.regime = 2; //déplacement jusqu'à la position global.objectif
            //reponse
            input["type"] = "ack";
            serializeJson(input,Serial);
            Serial.println();
        }
    }
    else if (comm == "err")
    {
        String type = (const char*)input["type"];
        if(type == "get")
        {
            StaticJsonDocument<1024> output;
            GestionErreurs::Erreur err = global.bot.erreurs.takeFront();

            output["comm"] = "err";
            output["type"] = "ack";

            output["args"]["id"] = err.id;
            output["args"]["maj"] = err.majeur;
            output["args"]["t"] = err.moment;
            output["args"]["err_sup"] = global.bot.erreurs.size();

            serializeJson(output,Serial);
            Serial.println();
        }
    }
    else if (comm == "cal")
    {
        String type = (const char*)input["type"];
        if(type == "set")
        {
            String mode = (const char*)input["args"]["mode"];
            if(mode == "cable")
            {
                int id = input["args"]["id"];
                double longueur = input["args"]["long"];
                global.bot.setLongueurCable(id,longueur);

                if(id < NBR_CABLES)
                {
                    global.cable[id] = longueur;
                }

                input["type"] = "ack";
                input["args"]["id"] = id;
                input["args"]["long"] = global.bot.getLongueurCable(id);
                serializeJson(input,Serial);
                Serial.println();
            }
        }
        else if(type == "get")
        {
            String mode = (const char*)input["args"]["mode"];
            if(mode == "cable")
            {
                int id = input["args"]["id"];

                input["type"] = "ack";
                input["args"]["long"] = global.bot.getLongueurCable(id);
                serializeJson(input,Serial);
                Serial.println();
            }
        }
    }
}

void serialEvent(){
  mainCommunication();
}

//fonction de controle, choisie la vitesse des moteurs
void controle()
{
    //mise à jour de la longueur des cables
    for(unsigned i = 0; i < NBR_CABLES; i++)
    {
        global.bot.setLongueurCable(i,global.cable[i]);
    }

    if(!global.bot.erreurs.empty()) global.regime == 0;
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
        if ((global.bot.getPosition() - global.objectif).norme_carree() < global.seuilPosition)
        {
            global.regime = 0;
            for(unsigned i = 0; i < NBR_CABLES; i++)
            {
                global.commandeVitesseCable[i] = 0;
            }
        }
        else
        {
            global.bot.deplacementPosition(global.objectif,(double)periodeControle/(double)1000.0,global.vitesse,global.commandeVitesseCable);
        }
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
    moteurLoop(NBR_CABLES,global.commandeVitesseCable,global.cable);
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
    //mise en place des poles:
    global.bot.addPole(FuniMath::Vecteur(0,0,0),FuniMath::Vecteur(0,0,0));
    global.bot.addPole(FuniMath::Vecteur(1180,0,0),FuniMath::Vecteur(0,0,0));
    
    //enregistrement du temps
    long temps = millis();
    global.lastCommunication = temps;
    global.lastMoteur = temps;
    global.lastControle = temps;
    global.lastEncodeur = temps;

    moteurSetup(NBR_CABLES);
}

//loop
void loop()
{
    long temps = millis();
    //Fonction de communication
    /*if(global.SerialEvent)
    {
         Serial.println(global.SerialEvent);
        global.SerialEvent = false;
        mainCommunication();
        Serial.println(global.SerialEvent);
    }*/
    //Fonction de contrôle
    if (temps - global.lastControle >= periodeControle)
    {
        controle();
        moteurs();
        global.lastControle = temps;
    }
    /*//Fonction des encodeurs
    if(temps - global.lastEncodeur >= periodeEncodeur)
    {
        encodeurs();
        global.lastEncodeur = temps;
    }
    //Fonction des moteurs
    if(temps - global.lastMoteur >= periodeControle)
    {
        moteurs();
        global.lastMoteur = temps;
    }*/

    
}
