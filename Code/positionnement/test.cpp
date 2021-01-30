#include "Funibot.h"
#include <iostream>


int main()
{
    Funibot bot;

    bot.addPole(FuniMath::Vecteur(100, 100, 100), FuniMath::Vecteur(0, 0, 0));
    bot.addPole(FuniMath::Vecteur(0, 102, 0), FuniMath::Vecteur(0, 0, 0));
    bot.addPole(FuniMath::Vecteur(0, 98, 104), FuniMath::Vecteur(0, 0, 0));
    bot.setLongueurCable(0, 102);
    bot.setLongueurCable(1, 102);
    bot.setLongueurCable(2, 20);

    bot.test();
}
