//mettre les fichiers suivant dans la librairie
#include <Arduino_JSON.h> //nécessite Arduino_JSON
#include "Funibot.h"
#include "moteur.h"

#define BAUDRATE  57600

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
    double seuilPosition = 1;
    //retour encodeur
    double cable[NBR_CABLES] = {0,0,0,0};
    //commande au moteur
    double commandeVitesseCable[NBR_CABLES] = {0};

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

inline JSONVar readJson()
{
    global.event = false;
    return JSON.parse(Serial.readString());
}

inline void sendJson(JSONVar output)
{
    Serial.println(JSON.stringify(output));
}

inline double getDouble(JSONVar number)
{
    double out = (double) number;
    if (isnan(out))return 0.0;
    else return out;
}

inline int getInt(JSONVar number)
{
    return (int)getDouble(number);
}

void communication()
{
    if (global.event)
    {
        JSONVar input = readJson();
        if (input.hasOwnProperty("comm"))
        {
            String comm = (const char*)input["comm"];
            if(comm == "pot")
            {
                if (input.hasOwnProperty("type") && input.hasOwnProperty("args"))
                {
                    String type = (const char*)input["type"];
                    JSONVar args = input["args"];
                    if(type == "get" && args.hasOwnProperty("id"))
                    {
                        int id = getInt(args["id"]);
                        FuniMath::Vecteur pot = global.bot.getPole(id);
                        //construction de la réponse
                        JSONVar output;
                        JSONVar outputArgs;
                        outputArgs["id"] = id;
                        outputArgs["pos_x"] = pot.x;
                        outputArgs["pos_y"] = pot.y;
                        outputArgs["pos_z"] = pot.z;

                        output["comm"] = "pot";
                        output["type"] = "ack";
                        output["args"] = outputArgs;

                        //encoie de la réponse
                        sendJson(output);
                        
                    }
                    else if(type == "set" && args.hasOwnProperty("id") && args.hasOwnProperty("pos_x")
                        && args.hasOwnProperty("pos_y") && args.hasOwnProperty("pos_z"))
                    {
                        int id = getInt(args["id"]);
                        double x = getDouble( args["pos_x"]);
                        double y = getDouble( args["pos_y"]);
                        double z = getDouble( args["pos_z"]);

                        if(global.bot.getNbrPole() <= id ) //pole inexistant
                            global.bot.addPole(FuniMath::Vecteur(x,y,z),FuniMath::Vecteur(0,0,0));
                        else //pole existant
                            global.bot.setPole(id,FuniMath::Vecteur(x,y,z),FuniMath::Vecteur(0,0,0));
                        //envoie d'une réponse
                        input["type"] = "ack";
                        sendJson(input);
                    }
                }
            }
            else if (comm == "dep")
            {
                if (input.hasOwnProperty("type"))
                {
                    String type = (const char*)input["type"];
                    JSONVar args = input["args"];
                    if(type == "set" && args.hasOwnProperty("mode"))
                    {
                        String mode = (const char*)args["mode"];
                        if (mode == "stop") 
                        {
                            global.regime = 0; //arret
                            input["type"] = "ack";
                            sendJson(input);
                        }
                        else if (args.hasOwnProperty("axe_x") && args.hasOwnProperty("axe_y") && args.hasOwnProperty("axe_z"))
                        {
                            double x = getDouble( args["axe_x"]);
                            double y = getDouble( args["axe_y"]);
                            double z = getDouble( args["axe_z"]);
                            global.objectif = FuniMath::Vecteur(x,y,z);

                            if(mode == "start")
                            {
                                global.regime = 1; //déplacement dans la direction de objectif
                                input["type"] = "ack";
                                sendJson(input);
                            }
                            else if(mode == "distance")
                            {
                                FuniMath::Vecteur position = global.bot.getPosition();
                                global.objectif = global.objectif + position;
                                global.regime = 1; //déplacement jusqu'à la position de objectif
                                input["type"] = "ack";
                                sendJson(input);
                            }
                        }
                        
                    }
                }
            }
            else if (comm == "pos")
            {
                if (input.hasOwnProperty("type"))
                {
                    String type = (const char*)input["type"];
                    JSONVar args = input["args"];
                    if(type == "get")
                    {
                        JSONVar output;
                        JSONVar outputArgs;
                        FuniMath::Vecteur position = global.bot.getPosition();

                        outputArgs["pos_x"] = position.x;
                        outputArgs["pos_y"] = position.y;
                        outputArgs["pos_z"] = position.z;

                        output["comm"] = "pos";
                        output["type"] = "ack";
                        output["args"] = outputArgs;
                        sendJson(output);
                    }
                    if(type == "set" && args.hasOwnProperty("pos_x") && args.hasOwnProperty("pos_y") && args.hasOwnProperty("pos_z"))
                    {
                        double x = getDouble( args["pos_x"]);
                        double y = getDouble( args["pos_y"]);
                        double z = getDouble( args["pos_z"]);
                        global.objectif = FuniMath::Vecteur(x,y,z);
                        global.regime = 2; //déplacement jusqu'à la position global.objectif
                        //reponse
                        input["type"] = "ack";
                        sendJson(input);
                    }
                }
                
            }
            else if (comm == "err")
            {
                input["type"] = "ack";
                sendJson(input);
            }
            else if (comm == "cal")
            {
                if (input.hasOwnProperty("type")&&input.hasOwnProperty("args"))
                {
                    String type = (const char*)input["type"];
                    JSONVar args = input["args"];
                    if(type == "set" && args.hasOwnProperty("mode"))
                    {
                        String mode = (const char*)args["mode"];
                        if(mode == "cable" && args.hasOwnProperty("id") && args.hasOwnProperty("long"))
                        {
                            int id = getInt(args["id"]);
                            double longueur = getDouble(args["long"]);
                            global.bot.setLongueurCable(id,longueur);
                            input["type"] = "ack";
                            input["args"]["id"] = id;
                            input["args"]["longueur"] = global.bot.getLongueurCable(id);
                            sendJson(input);
                        }
                    }
                }
            }
        }
    }

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
    moteurLoop();
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
    global.bot.addPole(FuniMath::Vecteur(0,0,0),FuniMath::Vecteur(0,0,0));
    global.bot.addPole(FuniMath::Vecteur(0,0,0),FuniMath::Vecteur(0,0,0));
    global.bot.addPole(FuniMath::Vecteur(0,0,0),FuniMath::Vecteur(0,0,0));
    
    //enregistrement du temps
    long temps = millis();
    global.lastCommunication = temps;
    global.lastMoteur = temps;
    global.lastControle = temps;
    global.lastEncodeur = temps;

    moteurSetup();
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
    //Fonction de contrôle
    if (temps - global.lastControle >= periodeControle)
    {
        controle();
        global.lastControle = temps;
    }
    //Fonction des encodeurs
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
    }
}