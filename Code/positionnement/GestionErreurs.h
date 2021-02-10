#pragma once

#ifdef ARDUINO
#define TIMESTAMP_ERREUR(x) x.moment = millis() 
#else
#define TIMESTAMP_ERREUR(x) x.moment = 0
#endif

namespace GestionErreurs
{
	const unsigned char TAILLE_PILE = 32;

	struct erreur
	{
		bool majeur = true;
		unsigned char id = 0;
		unsigned long moment = 0;
	};

	class PileErreurs
	{
	protected:
		unsigned char curseurDebut;
		unsigned char curseurFin;
		erreur listeErreurs[TAILLE_PILE];
	public:

		PileErreurs();					//constructeur
		void addBack(erreur newErreur); //ajoute un erreur à la liste
		erreur takeFront();				//prend l'erreur le plus ancien de de la pile et la retire de la pile
		unsigned char size();			//retourne le nombre d'erreur dans la pile
		bool empty();			//plus rapide que size() != 0 pour savoir s'il y a un erreur ou non
		erreur operator[] (unsigned char i);


	};
}