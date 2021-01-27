#include "Funibot.h"
#include <iostream>;


int main()
{
    Funibot bot;
    bot.addPole(FuniMath::vecteur(100, 100, 100), FuniMath::vecteur(0, 0, 0));
    bot.addPole(FuniMath::vecteur(0, 102, 0), FuniMath::vecteur(0, 0, 0));
    bot.addPole(FuniMath::vecteur(0, 98, 104), FuniMath::vecteur(0, 0, 0));
    bot.setLongueurCable(0, 102);
    bot.setLongueurCable(1, 102);
    bot.setLongueurCable(2, 20);
    bot.test();
}
