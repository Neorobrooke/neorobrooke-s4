#include "Funibot.h"
#include <iostream>


int main()
{
    Funibot bot;
<<<<<<< HEAD
    bot.addPole(FuniMath::Vecteur(0, 0, 0), FuniMath::Vecteur(0, 0, 0));
    bot.addPole(FuniMath::Vecteur(5, 0, 8.66), FuniMath::Vecteur(0, 0, 0));
    bot.addPole(FuniMath::Vecteur(10, 0, 4), FuniMath::Vecteur(0, 0, 0));
    bot.setLongueurCable(0, 7);
    bot.setLongueurCable(1, 5);
    bot.setLongueurCable(2, 10);
    bot.test();
    //ne fonctionne pas
    std::cout << "\n\nexemple qui ne fonctionne pas, pas la meme hauteur pour chaque pole\n";
    bot.setPole(0, FuniMath::Vecteur(0, -1, 0), FuniMath::Vecteur(0, 0, 0));
=======
    bot.addPole(FuniMath::vecteur(100, 100, 100), FuniMath::vecteur(0, 0, 0));
    bot.addPole(FuniMath::vecteur(0, 102, 0), FuniMath::vecteur(0, 0, 0));
    bot.addPole(FuniMath::vecteur(0, 98, 104), FuniMath::vecteur(0, 0, 0));
    bot.setLongueurCable(0, 102);
    bot.setLongueurCable(1, 102);
    bot.setLongueurCable(2, 20);
>>>>>>> e3eac6a4ecfec756dc6f7dbd80ab1c5b76e3ffe9
    bot.test();
}
