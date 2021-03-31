#include "GestionLog.h"

void GestionLog::clear()
{
    curseur = 0;
    for (short i = 0 ; i < log_size; i++)
        log[i] = '\0';
}
void GestionLog::printlog(const char* message)
{
    short curseur_mess = 0;
    while (message[curseur_mess] != '\n' && curseur < log_size-1)
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
        log[curseur] = '\n';  
        curseur ++; 
    }
    log[curseur] = '\0';  
}