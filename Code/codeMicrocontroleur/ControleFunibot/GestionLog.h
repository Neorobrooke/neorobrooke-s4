#pragma once
#include <avr/dtostrf.h>
#define log_size 1024

class GestionLog
{
    public:
    static char log[log_size];
    static short curseur;

    static void clear();
    static void printlog(const char* message);
    static void printlnlog(const char* message);
    static void printlog(double val);
    static void printlnlog(double val);
    static void printlog(String message);
    static void printlnlog(String message);
};

short GestionLog::curseur(0);
char GestionLog::log[log_size] = {'\0'};
