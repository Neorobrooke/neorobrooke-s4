#include "Funibot.h"
#include <iostream>;


int main()
{
    //fonctionne
    std::cout << "exemple qui fonctionne meme hauteur pour chaque pole\n";
    Funibot bot;
    bot.addPole(FuniMath::vecteur(0, 0, 0), FuniMath::vecteur(0, 0, 0));
    bot.addPole(FuniMath::vecteur(5, 0, 8.66), FuniMath::vecteur(0, 0, 0));
    bot.addPole(FuniMath::vecteur(10, 0, 4), FuniMath::vecteur(0, 0, 0));
    bot.setLongueurCable(0, 7);
    bot.setLongueurCable(1, 5);
    bot.setLongueurCable(2, 10);
    bot.test();
    //ne fonctionne pas
    std::cout << "\n\nexemple qui ne fonctionne pas, pas la meme hauteur pour chaque pole\n";
    bot.setPole(0, FuniMath::vecteur(0, -1, 0), FuniMath::vecteur(0, 0, 0));
    bot.test();
}
