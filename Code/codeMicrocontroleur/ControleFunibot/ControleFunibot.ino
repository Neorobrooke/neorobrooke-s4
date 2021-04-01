
#include <ArduinoJson.h> //nécessite ArduinoJson : arduinojson.org
#include "Funibot.h"
#include "moteur.h"
#include "Encodeur.h"
#include "GestionLog.h"


#define version "v t2"

#define BAUDRATE  57600

#define periodeControle 100

#define NBR_CABLES 4


struct aglomerationVariable
{
    bool outOfZone = false;
    //encodeur
    Encodeur encod [4] = 
    {
        Encodeur(2,1),
        Encodeur(4,5),
        Encodeur(7,6),
        Encodeur(8,9)
    };
    const double mmParTic = 0.75071069;

    //timers
    long lastControle = 0;

    //robot
    Funibot bot;
    FuniMath::Vecteur objectif;
    unsigned char regime = 0; //0 := arret, 1 := direction, 2 := position
    double vitesse = 50;
    double seuilPosition = 5;

    //retour encodeur
    double cable[NBR_CABLES] = {1300,1300,1300,1300};
    double offsetCable[NBR_CABLES] = {0,0};

    //commande au moteur
    double commandeVitesseCable[NBR_CABLES] = {0};
    bool moteur_On = true;

    //communication
    bool SerialEvent = false;
    bool rappel = false;

    //profile accumulatif
    long timeProfile[6];
};

//création des variables globales
aglomerationVariable global;

//fonction de modification de la taille des cable
inline void setCable(int id, double taille)
{
    global.cable[id] = taille;
    global.offsetCable[id] = taille - global.encod[id].read() * global.mmParTic;
}

//fonction de communication, communication entre utilisateur et microcontroleur

void mainCommunication()
{
    StaticJsonDocument<256> input;
    deserializeJson(input,Serial);

    String type = (const char*)input["type"];
    if(type == "ack") return;
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
        if(type == "get")
        {
            StaticJsonDocument<1024> output;
            GestionErreurs::Erreur err;
            if (global.outOfZone)
            {
                err.id = 23;
                err.majeur = false;
                err.moment = millis();
                global.outOfZone = false;
            }
            else
            {
                err = global.bot.erreurs.takeFront();
            }

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
                    setCable(id,longueur);
                }

                input["type"] = "ack";
                input["args"]["id"] = id;
                input["args"]["long"] = global.bot.getLongueurCable(id);
                serializeJson(input,Serial);
                Serial.println();
            }
            if(mode == "sol")
            {
                double longueur = input["args"]["long"];
                global.bot.setSol(longueur);
                input["type"] = "ack";
                input["args"]["long"] = global.bot.getSol();
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
            if(mode == "sol")
            {
                input["type"] = "ack";
                input["args"]["long"] = global.bot.getSol();
                serializeJson(input,Serial);
                Serial.println();
            }
        }
    }
    else if (comm == "mot")
    {
        if(type == "set")
        {
            String mode = (const char*)input["args"]["mode"];

            if (mode == "on")
            {
                moteurOn();
                global.moteur_On = true;
            }
            else if(mode == "off")
            {
                moteurOff();
                global.moteur_On = false;
            }
            else if (mode == "reset")
            {
                moteurReset();
                global.moteur_On = true;
            }
            else
            {
                return;
            }

            input["type"] = "ack";
            serializeJson(input,Serial);
            Serial.println();
        }
        else if(type == "get")
        {
            input["type"] = "ack";
            if (global.moteur_On)
                input["args"]["mode"] = "on";
            else
                input["args"]["mode"] = "off";
            serializeJson(input,Serial);
            Serial.println();
        }

    }
    else if(comm == "reg")
    {
        if (type == "get")
        {
            input["type"] = "ack";
            if (global.regime == 1)
                input["args"]["tache"] = "dir";
            else if (global.regime == 2)
                input["args"]["tache"] = "pos";
            else
                input["args"]["tache"] = "arr";
            serializeJson(input,Serial);
            Serial.println();
        }
    }
    else if(comm == "dur")
    {
        if (type == "get")
        {
            if (global.regime != 2)
            {
                input["args"]["tmp"] = 0;
            }
            else
            {
                double distance = (global.bot.getPosition() - global.objectif).norme();
                input["args"]["tmp"] = distance / global.vitesse;
            }
            input["type"] = "ack";
            serializeJson(input,Serial);

            Serial.println();
        }
    }
    else if(comm == "att")
    {
        if (type == "set")
        {
            if (global.regime == 2)
            {
                input["args"]["val"] = true;
                input["args"]["fin"] = false;
                global.rappel = true;
            }
            else
            {
                input["args"]["val"] = false;
                input["args"]["fin"] = false;
            }
            input["type"] = "ack";
            serializeJson(input,Serial);
            Serial.println();
        }
    }
    else if(comm == "log")
    {
        if(type == "get")
        {
            StaticJsonDocument<128 + log_size> out;

            out["comm"] = "log";
            out["type"] = "ack";
            out["args"]["msg"] = GestionLog::log;
            serializeJson(out,Serial);
            Serial.println();
            GestionLog::clear();
        }
    }
    
}

void serialEvent(){
  mainCommunication();
}

void rappel(bool valide)
{
    StaticJsonDocument<256> out;

            out["comm"] = "dur";
            out["type"] = "set";
            out["args"]["val"] = valide;
            out["args"]["fin"] = true;
            serializeJson(out,Serial);
            Serial.println();
            global.rappel = false;
}

//fonction de controle, choisie la vitesse des moteurs
void controle()
{
    //mise à jour de la longueur des cables
    for(unsigned i = 0; i < NBR_CABLES; i++)
    {
        global.bot.setLongueurCable(i,global.cable[i]);
    }

    if(!global.bot.erreurs.empty()) 
    {
        global.regime == 0;
        //envoie un rappel à l'utilisateur si celui-ci à été demandé
        if(global.rappel)
            rappel(false);
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
    {
        FuniMath::Vecteur dirr = global.objectif/global.objectif.norme();
        double distDeplacement = global.vitesse * ((double)periodeControle / (double)1000);
        FuniMath::Vecteur cible = global.bot.getPosition() + 2* distDeplacement * dirr; //facteur de sécurité de 2
        
        if (NBR_CABLES < 3 || global.bot.isSafe(cible))
        {
            global.outOfZone = false;
            global.bot.deplacementDirectionnel(global.objectif,(double)periodeControle/(double)1000.0,global.vitesse,global.commandeVitesseCable);
        }
        else
        {
            global.outOfZone = true;
            global.regime = 0;
            for(unsigned i = 0; i < NBR_CABLES; i++)
            {
                global.commandeVitesseCable[i] = 0;
            }
        }
        break;
    }
    //position
    case 2:
    {
        FuniMath::Vecteur position = global.bot.getPosition();
        FuniMath::Vecteur deplacement = global.objectif - position;
        double normeDeplacement = deplacement.norme();
        if (normeDeplacement < global.seuilPosition)
        {
            global.regime = 0;
            for(unsigned i = 0; i < NBR_CABLES; i++)
            {
                global.commandeVitesseCable[i] = 0;
            }

            //envoie un rappel à l'utilisateur si celui-ci à été demandé
            if(global.rappel)
                rappel(true);
        }
        else
        {

            deplacement = deplacement / normeDeplacement;
            double distDeplacement = global.vitesse * (double)periodeControle / (double)1000;
            FuniMath::Vecteur cible = position + 2* distDeplacement * deplacement;
            if (NBR_CABLES < 3 || global.bot.isSafe(cible))
            {
                global.outOfZone = false;
                global.bot.deplacementPosition(global.objectif,(double)periodeControle/(double)1000.0,global.vitesse,global.commandeVitesseCable);
            }
            else
            {
                //envoie un rappel à l'utilisateur si celui-ci à été demandé
                if(global.rappel)
                    rappel(false);

                global.outOfZone = true;
                global.regime = 0;
                for(unsigned i = 0; i < NBR_CABLES; i++)
                {
                    global.commandeVitesseCable[i] = 0;
                }
            }
        }
        break;
    }
    //défaut
    default:
        for(unsigned i = 0; i < NBR_CABLES; i++)
        {
            global.commandeVitesseCable[i] = 0;
        }
        break;
    }

    //arrêt en cas d'erreur majeure
    if (!global.bot.erreurs.empty())
    {
        for (int i = 0; i < global.bot.erreurs.size(); i++)
        {
            if (global.bot.erreurs[i].majeur)
            global.regime = 0;
        }
    }
}

//fonction des moteurs, controle les moteurs et s'assure d'obtenir la bonne vitesse
void moteurs()
{
    if(global.moteur_On)
    moteurLoop(global.commandeVitesseCable,global.cable);
}

//fonction des encodeurs, assure un bon suivie de la longueur des cables
void encodeurs()
{
    for(int i = 0; i < NBR_CABLES; i++)
    {
        global.cable[i] = global.encod[i].read() * global.mmParTic + global.offsetCable[i];
    }
}

//fonctions pour les interrupts des encodeurs
void interrupt0 ()
{
    global.encod[0].interruptFct();
}
void interrupt1 ()
{
    global.encod[1].interruptFct();
}
void interrupt2 ()
{
    global.encod[2].interruptFct();
}
void interrupt3 ()
{
    global.encod[3].interruptFct();
}
//setup
void setup()
{
    GestionLog::printlnlog(version);
    //communication série
    Serial.begin(BAUDRATE);
    
    for(int i = 0 ; i < NBR_CABLES; i++) global.encod[i].setup();


    
    //mise en place des poles:
    global.bot.addPole(FuniMath::Vecteur(0,0,0),FuniMath::Vecteur(0,0,0));
    global.bot.addPole(FuniMath::Vecteur(1180,0,0),FuniMath::Vecteur(0,0,0));
    global.bot.addPole(FuniMath::Vecteur(1180,0,1180),FuniMath::Vecteur(0,0,0));
    global.bot.addPole(FuniMath::Vecteur(0,0,1180),FuniMath::Vecteur(0,0,0));
    
    //enregistrement du temps
    long temps = millis();
    global.lastControle = temps;

    //mise en place de la distance initiale des cables
    for (int i = 0; i< NBR_CABLES; i++)setCable(i,global.cable[i]);

    //mise en place des interrupts
    attachInterrupt(global.encod[0].pinInterrupt(),interrupt0, CHANGE);
    attachInterrupt(global.encod[1].pinInterrupt(),interrupt1, CHANGE);
    attachInterrupt(global.encod[2].pinInterrupt(),interrupt2, CHANGE);
    attachInterrupt(global.encod[3].pinInterrupt(),interrupt3, CHANGE);

    //initialisation des moteurs
    moteurSetup(NBR_CABLES,global.cable);

}

//loop
void loop()
{
    long temps = millis();

    if (temps - global.lastControle >= periodeControle)
    {
        encodeurs();
        controle();
        moteurs();
        global.lastControle = temps;
    }
    
}
