#pragma once

namespace GestionErreurs
{
	const unsigned char TAILLE_PILE = 32;

	struct Erreur
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
		Erreur listeErreurs[TAILLE_PILE];
	public:

		PileErreurs();					//constructeur
		void addBack(Erreur newErreur); //ajoute un erreur à la liste
		Erreur takeFront();				//prend l'erreur le plus ancien de de la pile et la retire de la pile
		unsigned char size();			//retourne le nombre d'erreur dans la pile
		bool empty();			//plus rapide que size() != 0 pour savoir s'il y a un erreur ou non
		Erreur operator[] (unsigned char i);


	};
}