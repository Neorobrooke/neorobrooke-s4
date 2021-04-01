#include "GestionLog.h"

void dtoc(double val, char* buffer, int prec = 2, double max = 100000)
{
    int pos = 0;
    int temps_d = 0;
    double base = max;
    while (temps_d <= prec)
    {
        if (val > base)
        {
            int mult = (int)floor(val/base);
            switch (mult)
            {
            case 1:
                buffer[pos] = '1';
                val -= base;
                break;
            case 2:
                buffer[pos] = '2';
                val -= base * 2;
                break;
            case 3:
                buffer[pos] = '3';
                val -= base * 3;
                break;
            case 4:
                buffer[pos] = '4';
                val -= base * 4;
                break;
            case 5:
                buffer[pos] = '5';
                val -= base * 5;
                break;
            case 6:
                buffer[pos] = '6';
                val -= base * 6;
                break;
            case 7:
                buffer[pos] = '7';
                val -= base * 7;
                break;
            case 8:
                buffer[pos] = '8';
                val -= base * 8;
                break;
            default:
                buffer[pos] = '9';
                val -= base * 9;
                break;
            }
            pos++;
        }
        else if (pos != 0)
        {
            buffer[pos] = '0';
            pos ++;
        }
        base /= 10;
        if (base < 0.9)
        {
            if (temps_d == 0)
            {
                if(pos == 0)
                {
                    buffer[pos] = '0';
                    pos ++;
                }
                buffer[pos] = ',';
                pos ++;
            }
            temps_d ++;
        }
    }
    buffer[pos] = 0;

    
    
}
void GestionLog::clear()
{
    curseur = 0;
    for (short i = 0 ; i < log_size; i++)
        log[i] = '\0';
}
void GestionLog::printlog(const char* message)
{
    short curseur_mess = 0;
    while (message[curseur_mess] != '\0' && curseur < log_size-1)
    {
        log[curseur] = message[curseur_mess];
        curseur ++;
        curseur_mess ++;
    }
    log[curseur] = '\0';     
}
void GestionLog::printlnlog(const char* message)
{
    short curseur_mess = 0;
    while (message[curseur_mess] != '\0' && curseur < log_size-1)
    {
        log[curseur] = message[curseur_mess];
        curseur ++;
        curseur_mess ++;
    }
    if(curseur < log_size-1)
    {
        log[curseur] = 13;  
        curseur ++; 
    }
    log[curseur] = '\0';  
}
void GestionLog::printlog(double val)
{
    char buffer[32];
    dtoc(val,buffer);
    printlog(buffer);
}

void GestionLog::printlnlog(double val)
{
    char buffer[32];
    dtoc(val,buffer);
    printlnlog(buffer);
}

void GestionLog::printlog(String message)
{
    printlog(message.c_str());  
}
void GestionLog::printlnlog(String message)
{
    printlnlog(message.c_str());  
}