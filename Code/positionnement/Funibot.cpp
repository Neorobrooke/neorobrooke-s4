#include "Funibot.h"
#include <iostream>

//#define systemeArduino


FuniMath::Vecteur FuniMath::operator*(const double u, const FuniMath::Vecteur v)
{
	return FuniMath::Vecteur(v.x * u, v.y * u, v.z * u);
}

// Racine carr�e � l'aide de la m�thode de Raphson-Newton
double FuniMath::sqrt(double u, double precision)
{
	double est = u / 2;
	while (abs((est * est) - u) > precision)
	{
		est -= (est * est - u) / (2 * est);
	}
	return est;
}

std::ostream& operator<<(std::ostream& ios, FuniMath::Vecteur& vect)
{
	ios << "(" << vect.x << "; " << vect.y << ";" << vect.z << ")";
	return ios;
}

Funibot::Funibot()
	: nbrPole(0)
{
	for (unsigned char i = 0; i < FuniConst::NBR_POLES; i++)
	{
		cable[i] = 0;
	}
}

void Funibot::addPole(FuniMath::Vecteur positionPole, FuniMath::Vecteur positionAccroche)
{
	// D�passement du nombre de p�les maximum
	if (nbrPole == FuniConst::NBR_POLES)
	{
		GestionErreurs::erreur erreur;
		erreur.id = 1;
		#ifdef systemeArduino
			erreur.moment = millis();
		#endif
		erreurs.addBack(erreur);
		return;
	}

	pole[nbrPole] = positionPole;
	accroche[nbrPole] = positionAccroche;
	nbrPole++;
}

void Funibot::setPole(unsigned char index, FuniMath::Vecteur positionPole, FuniMath::Vecteur positionAccroche)
{
	// Acc�s � un p�le inexistant
	if (index >= nbrPole)
	{
		GestionErreurs::erreur erreur;
		erreur.id = 2;
		#ifdef systemeArduino
			erreur.moment = millis();
		#endif
		erreurs.addBack(erreur);
		return;
	}

	pole[index] = positionPole;
	accroche[index] = positionAccroche;
}

void Funibot::setLongueurCable(unsigned char index, double longueur)
{
	// Acc�s � un c�ble inexistant
	if (index >= nbrPole)
	{
		GestionErreurs::erreur erreur;
		erreur.id = 3;
		#ifdef systemeArduino
			erreur.moment = millis();
		#endif
		erreurs.addBack(erreur);
		return;
	}

	cable[index] = longueur;
}

FuniMath::Vecteur Funibot::getPosition()
{
	// Plus de deux c�bles
	if (nbrPole > 2)
	{
		// V�rifiactions
		for (int i = 0; i < nbrPole; ++i)
			for (int j = i + 1; j < nbrPole; ++j)
			{
				double distij = (pole[i] - accroche[i] - pole[j] + accroche[j]).norme_carree();

				// C�bles trop courts
				if (sqrt(distij) > (cable[i] + cable[j]) * (cable[i] + cable[j]))
				{
					GestionErreurs::erreur erreur;
					erreur.id = 8;
					#ifdef systemeArduino
						erreur.moment = millis();
					#endif
					erreurs.addBack(erreur);
					return FuniMath::Vecteur();
				}
			}

		// Correction en fonction de la position des accroches
		FuniMath::Vecteur C1 = pole[0] - accroche[0];
		FuniMath::Vecteur C2 = pole[1] - accroche[1];
		FuniMath::Vecteur C3 = pole[2] - accroche[2];

		// Direction d'un p�le � l'autre
		FuniMath::Vecteur Dirr1 = C2 - C1;
		FuniMath::Vecteur Dirr2 = C3 - C1;

		// Distance d'une p�le � l'autre
		double dist1 = Dirr1.norme();
		double dist2 = Dirr2.norme();

		// Vecteurs de direction unitaire
		FuniMath::Vecteur Dirr1u = Dirr1 / dist1;
		FuniMath::Vecteur Dirr2u = Dirr2 / dist2;

		//test si m�me direction
		if ((Dirr1u - Dirr2u).norme_carree() < 0.0001)
		{
			GestionErreurs::erreur erreur;
			erreur.id = 9;
			#ifdef systemeArduino
				erreur.moment = millis();
			#endif
			erreurs.addBack(erreur);
			return FuniMath::Vecteur();
		}

		// Longueur du premier c�ble au carr� (utilis�e � plusieurs reprises)
		double r1Carr = cable[0] * cable[0];

		// Recherche des centres de jonctions tels que c1 + ki*Dirri = centre de jonction entre C1 et C(i+1)
		double k1 = (r1Carr - (cable[1] * cable[1]) + (dist1 * dist1)) / (2 * dist1);
		double k2 = (r1Carr - (cable[2] * cable[2]) + (dist2 * dist2)) / (2 * dist2);

		// Cr�ation de base orthonorm�es dans le plan (c1,c2,c3) ayant c1 comme centre
		FuniMath::Vecteur base1 = Dirr1u;
		FuniMath::Vecteur base2 = Dirr2u - Dirr1u * Dirr1u.produitScalaire(Dirr2u);
		base2 = base2 / base2.norme();
		FuniMath::Vecteur base3 = base1.produitVectoriel(base2);
		base3 = base3 / base3.norme();

		if (base3.y > 0)
		{
			base3 = base3 * -1;
		}

		// Position dans le referentiel base1, base2

		// Projection du vecteur k1*Dirr1u sur les bases 1 et 2
		// Dirr1u �tant la base1, la r�ponse est �vidente
		double b1Pos = k1;

		// Projection du vecteur k2*Dirr2u sur les bases 1 et 2
		double compb1 = Dirr2u.produitScalaire(base1) * k2;
		double compb2 = Dirr2u.produitScalaire(base2) * k2;

		// Cr�ation d'une droite perpendiculaire au vecteur k2*Dirr2u passant par le point k2*Dirr2u
		double a, b;
		a = -compb1 / compb2;
		b = compb2 - a * compb1;

		// Jonction entre les deux perpendiculaires
		double b2Pos = a * b1Pos + b;

		// Recherche de la composante dans la base3 � l'aide de l'�quation de la sph�re C1
		double b3Pos2 = r1Carr - (b1Pos * b1Pos) - (b2Pos * b2Pos);

		// Racine neative
		if (b3Pos2 < 0)
		{
			GestionErreurs::erreur erreur;
			erreur.id = 10;
			erreur.majeur = false;
			#ifdef systemeArduino
				erreur.moment = millis();
			#endif
			erreurs.addBack(erreur);

			b3Pos2 = 0;
		}

		double b3Pos = sqrt(b3Pos2);


		// Conversion des positions dans le r�f�rentiel normal
		FuniMath::Vecteur jointure = base1 * b1Pos + base2 * b2Pos + base3 * b3Pos;

		// D�centrage de C1
		return jointure + C1;


	}
	// Deux c�bles
	else if (nbrPole == 2)
	{
		// Calculs p�les relatifs
		FuniMath::Vecteur C1 = pole[0] - accroche[0];
		FuniMath::Vecteur C2 = pole[1] - accroche[1];
		FuniMath::Vecteur Dirr = C2 - C1;
		double dist = Dirr.norme();

		// C�bles trop courts
		if (dist > (cable[0] + cable[1]))
		{
			GestionErreurs::erreur erreur;
			erreur.id = 5;
			#ifdef systemeArduino
				erreur.moment = millis();
			#endif
			erreurs.addBack(erreur);
			return FuniMath::Vecteur();
		}
		if ((dist * dist + cable[1] * cable[1]) < (cable[0] * cable[0]))
		{
			GestionErreurs::erreur erreur;
			erreur.id = 6;
			erreur.majeur = false;
			#ifdef systemeArduino
				erreur.moment = millis();
			#endif
			erreurs.addBack(erreur);
		}
		if ((dist * dist + cable[0] * cable[0]) < (cable[1] * cable[1]))
		{
			GestionErreurs::erreur erreur;
			erreur.id = 7;
			#ifdef systemeArduino
				erreur.moment = millis();
			#endif
			erreurs.addBack(erreur);
		}

		// Recherche des centres de jonctions tels que c1 + k*Dirr = centre de jonction entre C1 et C2
		double k = ((cable[0]) * (cable[0]) - (cable[1] * cable[1]) + (dist * dist)) / (2 * dist);
		FuniMath::Vecteur centre = (Dirr * k / dist) + C1;

		// Recherche du d�calage d'un au rayon de la jonction
		if (C1.y == C2.y)
		{
			return FuniMath::Vecteur(centre.x, centre.y - FuniMath::sqrt(cable[0] * cable[0] - k * k), centre.z);
		}
		else
		{
			double a = (C2.x - C1.x) / (C1.y - C2.y);
			return centre - (FuniMath::Vecteur(1, a, 0) / FuniMath::Vecteur(1, a, 0).norme() * FuniMath::sqrt(cable[0] * cable[0] - k * k));
		}
	}
	// Un seul c�ble
	else if (nbrPole == 1)
	{
		return pole[0] - accroche[0] - FuniMath::Vecteur(0, cable[0], 0);
	}
	// Aucun c�ble pour les calculs
	else
	{
		GestionErreurs::erreur erreur;
		erreur.id = 4;
		#ifdef systemeArduino
			erreur.moment = millis();
		#endif
		erreurs.addBack(erreur);
		return FuniMath::Vecteur();
	}
}

void Funibot::test()
{
	// Multic�bles
	if (nbrPole > 1)
	{
		if (nbrPole == 2)
		{
			std::cout << "Fonctionnement 2D\n\n";
		}
		else
		{
			std::cout << "Fonctionnement 3D\n\n";
		}

		std::cout << "Position des p�les:\n";
		for (int i = 0; i < nbrPole; i++)
		{
			std::cout << pole[i] << "\n";
		}

		std::cout << "\nPosition des accroches:\n";
		for (int i = 0; i < nbrPole; i++)
		{
			std::cout << accroche[i] << "\n";
		}

		std::cout << "\nLongueurs des c�bles:\n";
		for (int i = 0; i < nbrPole; i++)
		{
			std::cout << cable[i] << "\n";
		}

		FuniMath::Vecteur pos = getPosition();
		std::cout << "\n\nPosition calcul�e: " << pos;

		std::cout << "\nLongueurs des c�bles calcul�es:\n";
		for (int i = 0; i < nbrPole; i++)
		{
			std::cout << (pos + accroche[i] - pole[i]).norme() << "\n";
		}
	}
	// Un seul c�ble
	else if (nbrPole == 1)
	{
		std::cout << "Fonctionnement 1D\n\n";
		std::cout << "Position du p�le: " << pole[0];
		std::cout << "\nPosition de l'accroche:" << accroche[0];
		std::cout << "\nTaille du c�ble: " << cable[0];

		FuniMath::Vecteur pos = getPosition();
		std::cout << "\n\nPosition calcul�e: " << pos;
		std::cout << "\nTaille c�ble calcul�e : " << (pos + accroche[0] - pole[0]).norme() << "\n";
	}
	// Aucun c�ble pour les calculs
	else
	{
		throw 1;
	}
}

double* Funibot::deplacementDirectionnel(FuniMath::Vecteur dir, double pasTemps, double vitesse, double* vitesseCable)
{
	//Position cible
	FuniMath::Vecteur position = getPosition();									//prise de la position actuelle
	if (!erreurs.empty())														//gestion des erreurs
	{
		bool erreurMajeur = false;
		{
			for (unsigned char i = 0; i < erreurs.size(); i++)
			{
				if (erreurs[i].majeur)
				{
					erreurMajeur = true;
					break;
				}
			}
		}
		if (erreurMajeur)
		{
			GestionErreurs::erreur erreur;
			erreur.id = 11;
			#ifdef systemeArduino
				erreur.moment = millis();
			#endif
			erreurs.addBack(erreur);
			return vitesseCable;
		}
		else
		{
			GestionErreurs::erreur erreur;
			erreur.id = 12;
			erreur.majeur = false;
			#ifdef systemeArduino
				erreur.moment = millis();
			#endif
			erreurs.addBack(erreur);
			return vitesseCable;
		}
	}
	dir = dir / dir.norme();													//direction unitaire
	FuniMath::Vecteur positionCible = position + (dir * pasTemps * vitesse);	//calcul de la position cible

	//Vitesse des cables
	for (unsigned char i = 0; i < FuniConst::NBR_POLES; i++)
	{
		const double nCable ((positionCible + accroche[i] - pole[i]).norme());		//longueur de cable cible
		vitesseCable[i] = (nCable - cable[i]) / pasTemps;							//vitesse du cable
	}

	return vitesseCable;
}

double* Funibot::deplacementPosition(FuniMath::Vecteur pos, double pasTemps, double vitesse, double* vitesseCable)
{
	//Position cible
	FuniMath::Vecteur position = getPosition();									//prise de la position actuelle
	if (!erreurs.empty())														//gestion des erreurs
	{
		bool erreurMajeur = false;
		{
			for (unsigned char i = 0; i < erreurs.size(); i++)
			{
				if (erreurs[i].majeur)
				{
					erreurMajeur = true;
					break;
				}
			}
		}
		if (erreurMajeur)
		{
			GestionErreurs::erreur erreur;
			erreur.id = 13;
			#ifdef systemeArduino
				erreur.moment = millis();
			#endif
			erreurs.addBack(erreur);
			return vitesseCable;
		}
		else
		{
			GestionErreurs::erreur erreur;
			erreur.id = 14;
			erreur.majeur = false;
			#ifdef systemeArduino
				erreur.moment = millis();
			#endif
			erreurs.addBack(erreur);
			return vitesseCable;
		}
	}


	FuniMath::Vecteur dir = pos - position;										//direction du d�placement
	dir = dir / dir.norme();													//direction unitaire
	FuniMath::Vecteur positionCible = position + (dir * pasTemps * vitesse);	//calcul de la position cible

	//test cible d�pass�
	if ((position - positionCible).norme_carree() > (position - pos).norme_carree())	//si la cible est plus loin que la position d�sir�e,
		positionCible = pos;															//on remplace la cible par la position d�sir�e

	//Vitesse des cables
	for (unsigned char i = 0; i < FuniConst::NBR_POLES; i++)
	{
		const double nCable((positionCible + accroche[i] - pole[i]).norme());		//longueur de cable cible
		vitesseCable[i] = (nCable - cable[i]) / pasTemps;							//vitesse du cable
	}

	return vitesseCable;
}

FuniMath::Vecteur Funibot::getPole(unsigned char index)
{
	if (index >= nbrPole)
	{
		GestionErreurs::erreur erreur;
		erreur.id = 15;
		#ifdef systemeArduino
			erreur.moment = millis();
		#endif
		erreurs.addBack(erreur);
		return FuniMath::Vecteur();
	}
	return pole[index];
}
FuniMath::Vecteur Funibot::getAccroche(unsigned char index)
{
	if (index >= nbrPole)
	{
		GestionErreurs::erreur erreur;
		erreur.id = 16;
		#ifdef systemeArduino
			erreur.moment = millis();
		#endif
		erreurs.addBack(erreur);
		return FuniMath::Vecteur();
	}
	return pole[index];
}
FuniMath::Vecteur Funibot::getLongueurCable(unsigned char index)
{
	if (index >= nbrPole)
	{
		GestionErreurs::erreur erreur;
		erreur.id = 17;
		#ifdef systemeArduino
			erreur.moment = millis();
		#endif
		erreurs.addBack(erreur);
		return 0;
	}
	return cable[index];
}

FuniMath::Vecteur Funibot::getPoleRelatif(unsigned char index)
{
	if (index >= nbrPole)
	{
		GestionErreurs::erreur erreur;
		erreur.id = 18;
		#ifdef systemeArduino
			erreur.moment = millis();
		#endif
		erreurs.addBack(erreur);
		return FuniMath::Vecteur();
	}
	return pole[index] - accroche[index];
}