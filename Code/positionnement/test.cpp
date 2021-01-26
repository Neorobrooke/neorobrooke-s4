#include "Funibot.h"


int main()
{
    Funibot bot;
    bot.addPole(FuniMath::vecteur(10, 0, 0), FuniMath::vecteur(0, 0, 0));
    bot.addPole(FuniMath::vecteur(0, 0, 0), FuniMath::vecteur(0, 0, 0));
    bot.setLongueurCable(0, 10);
    bot.setLongueurCable(1, 5);
    bot.test();
}
