#include "GestionErreurs.h"
using namespace GestionErreurs;


PileErreurs::PileErreurs() 
	: curseurDebut(0), curseurFin(0)
{}

void PileErreurs::addBack(erreur newErreur)
{
	if (curseurDebut == curseurFin)							//si taille max dépassé
		curseurDebut = (curseurDebut + 1) % TAILLE_PILE;	//décalage du curseur de début

	listeErreurs[curseurFin] = newErreur;					//ajout de l'erreur
	curseurFin = (curseurFin + 1) % TAILLE_PILE;			//décalage du curseur de fin
}
erreur PileErreurs::takeFront()
{
	if (curseurDebut == curseurFin) //si aucune erreur
		return erreur();			//retourne une erreur vide (id = 0)
	
	unsigned char PositionPremiereErreur = curseurDebut;	//enregistrement de la position de la première erreure
	curseurDebut = (curseurDebut + 1) % TAILLE_PILE;		//décalage du curseur de début

	return listeErreurs[PositionPremiereErreur];			//retour de la première erreur
}

unsigned char PileErreurs::size()
{
	if (curseurDebut < curseurFin)
		return curseurFin - curseurDebut;
	return (TAILLE_PILE - curseurDebut) + curseurFin;
}

bool PileErreurs::empty()
{
	return (curseurDebut == curseurFin);
}

erreur PileErreurs::operator[] (unsigned char i)
{
	return listeErreurs[(curseurDebut + i) % TAILLE_PILE];
}