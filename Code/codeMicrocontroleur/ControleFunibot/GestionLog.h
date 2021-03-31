#pragma once
#define log_size 1024

class GestionLog
{
    public:
    static char log[log_size];
    static short curseur;

    static void clear();
    static void printlog(const char* message);
    static void printlnlog(const char* message);
};

short GestionLog::curseur(0);
char GestionLog::log[log_size] = {'\0'};
