#include "Funibot.h"
#include <iostream>


FuniMath::Vecteur FuniMath::operator*(const double u, const FuniMath::Vecteur v)
{
	return FuniMath::Vecteur(v.x * u, v.y * u, v.z * u);
}

// Racine carrée à l'aide de la méthode de Raphson-Newton
double FuniMath::sqrt(double u, double precision)
{
	double est = u / 2;
	while (abs((est * est) - u) > precision)
	{
		est -= (est * est - u) / (2 * est);
	}
	return est;
}

std::ostream& operator << (std::ostream& ios, FuniMath::Vecteur& vect)
{
	ios << "(" << vect.x << "; " << vect.y << ";" << vect.z << ")";
	return ios;
}

Funibot::Funibot():nbrPole(0)
{
	for (unsigned char i = 0; i < FuniConst::NBR_POLES; i++)
	{
		cable[i] = 0;
	}
}

void Funibot::addPole(FuniMath::Vecteur positionPole, FuniMath::Vecteur positionAccroche)
{
	if (nbrPole == FuniConst::NBR_POLES)throw 1; //dépassement du nombre de pole maximum
	pole[nbrPole] = positionPole;
	accroche[nbrPole] = positionAccroche;
	nbrPole++;
}

void Funibot::setPole(unsigned char index, FuniMath::Vecteur positionPole, FuniMath::Vecteur positionAccroche)
{
	if (index >= nbrPole)throw 1; //accès à un pole inexistant
	pole[index] = positionPole;
	accroche[index] = positionAccroche;

}

void Funibot::setLongueurCable(unsigned char index, double longueur)
{
	if (index >= nbrPole)throw 1; //accès à un cable inexistant
	cable[index] = longueur;
}

FuniMath::Vecteur Funibot::getPosition()
{
	//plus de deux cables
	if (nbrPole > 2)
	{
		//vérifiactions
		for (int i = 0; i < nbrPole; i++)
			for (int j = i+1; j < nbrPole; j++)
			{
<<<<<<< HEAD
				double distij = (pole[i] - accroche[i] - pole[j] + accroche[j]).norme_carree();
				if (sqrt(distij) > (cable[i] + cable[j])) throw 2; //cables trop court
			}

		// points
		FuniMath::Vecteur C1 = pole[0] - accroche[0];
		FuniMath::Vecteur C2 = pole[1] - accroche[1];
		FuniMath::Vecteur C3 = pole[2] - accroche[2];
=======
				double distij = (pole[i] - accroche[i] - pole[j] + accroche[j]).norm2();
				if (sqrt(distij) > (cable[i] + cable[j]) * (cable[i] + cable[j])) throw 2; //cables trop court
			}

		// correction en fonction de la position des accroches
		FuniMath::vecteur C1 = pole[0] - accroche[0];
		FuniMath::vecteur C2 = pole[1] - accroche[1];
		FuniMath::vecteur C3 = pole[2] - accroche[2];
>>>>>>> e3eac6a4ecfec756dc6f7dbd80ab1c5b76e3ffe9

		//v�rification d'erreur d'allignement des p�le
		if (C1.z == C2.z && C1.z == C3.z) throw 5; //allignement en z
		if (C1.x == C2.x && C1.x == C3.x) throw 5; //allignement en x

<<<<<<< HEAD
		//centres de jonction
		FuniMath::Vecteur Dirr1 = C2 - C1;
		FuniMath::Vecteur Dirr2 = C3 - C1;

		double dist1 = Dirr1.norme();
		double dist2 = Dirr2.norme();
=======
		//direction d'un pole � l'autre
		FuniMath::vecteur Dirr1 = C2 - C1;
		FuniMath::vecteur Dirr2 = C3 - C1;

		//distance d'une pole � l'autre
		double dist1 = Dirr1.norm();
		double dist2 = Dirr2.norm();
>>>>>>> e3eac6a4ecfec756dc6f7dbd80ab1c5b76e3ffe9

		//vecteurs de direction unitaire
		FuniMath::vecteur Dirr1u = Dirr1/dist1;
		FuniMath::vecteur Dirr2u = Dirr2/dist2;

		//longueur du prmeier cable au carr� (utilis� � plusieurs reprises)
		double r1Carr = cable[0]* cable[0];

		//recherches des centre de jonctions tels que c1 + ki*Dirri = centre de jonction entre C1 et C(i+1)
		double k1 = (r1Carr - (cable[1] * cable[1]) + (dist1 * dist1)) / (2 * dist1);
		double k2 = (r1Carr - (cable[2] * cable[2]) + (dist2 * dist2)) / (2 * dist2);

<<<<<<< HEAD
		FuniMath::Vecteur centre1 = (Dirr1 * k1 / dist1) + C1;
		FuniMath::Vecteur centre2 = (Dirr2 * k2 / dist2) + C1;
=======
		//creation de base orthonorm� dans le plan c1,c2,c3 ayant c1 comme centre
		FuniMath::vecteur base1 = Dirr1u;
		FuniMath::vecteur base2 = Dirr2u - Dirr1u * Dirr1u.produitScalaire(Dirr2u);
		base2 = base2 / base2.norm();
		FuniMath::vecteur base3 = base1.produitVectoriel(base2);
		base3 = base3 / base3.norm();
		if (base3.y > 0)base3 = base3 * -1;
>>>>>>> e3eac6a4ecfec756dc6f7dbd80ab1c5b76e3ffe9

		//position dans le referentiel base1, base2

		//projection du vecteur k1*Dirr1u sur la base1 et 2
		//Dirr1u �tant la base1, la r�ponse est �vidente
		double b1Pos = k1;

		

<<<<<<< HEAD
		//résolution finale
		double posX;
		double posZ;
=======
		//projection du vecteur k2*Dirr2u sur la base1 et 2
		double compb1 = Dirr2u.produitScalaire(base1) * k2;
		double compb2 = Dirr2u.produitScalaire(base2) * k2;
>>>>>>> e3eac6a4ecfec756dc6f7dbd80ab1c5b76e3ffe9

		//cr�ation d'une droite perpendiculaire au vecteur k2*Dirr2u passant par le point k2*Dirr2u
		double a, b;
		a = -compb1 / compb2;
		b = compb2 - a * compb1;

		//jonction entre les deux perpendiculaires
		double b2Pos = a * b1Pos + b;

		//recherche de la composante dans la base3 � l'aide de l'�quation de la sph�re C1
		double b3Pos2 = r1Carr - (b1Pos * b1Pos) - (b2Pos * b2Pos);
		if (b3Pos2 < 0) throw 5; //racine neative
		double b3Pos = sqrt(b3Pos2);

<<<<<<< HEAD
		double posYCarr = r1Carr - posX * posX - posZ * posZ;
		if (posYCarr < 0)throw 6;//racine négative
		double posY = C1.y - sqrt(posYCarr);
		return FuniMath::Vecteur(posX, posY, posZ);
=======

		//conversion des position dans le r�f�rentiel normal
		FuniMath::vecteur jointure =  base1 * b1Pos +  base2 * b2Pos + base3 * b3Pos;

		// decentrage de C1
		return jointure + C1;
>>>>>>> e3eac6a4ecfec756dc6f7dbd80ab1c5b76e3ffe9


	}
	//deux cables
	else if (nbrPole == 2)
	{
		// calculs pole relatif
		FuniMath::Vecteur C1 = pole[0] - accroche[0];
		FuniMath::Vecteur C2 = pole[1] - accroche[1];
		FuniMath::Vecteur Dirr = C2 - C1;
		double dist = Dirr.norme();

		if (dist > (cable[0] + cable[1])) throw 2; //cables trop court
		if ((dist * dist + cable[1] * cable[1]) < (cable[0] * cable[0]))throw 3; //cable 0 trop long
		if ((dist * dist + cable[0] * cable[0]) < (cable[1] * cable[1]))throw 4; //cable 1 trop long

		//recherches des centre de jonctions tels que c1 + k*Dirr = centre de jonction entre C1 et C2
		double k = ((cable[0]) * (cable[0]) - (cable[1] * cable[1]) + (dist * dist)) / (2*dist);
		FuniMath::Vecteur centre = (Dirr * k / dist) + C1;
		
		//recherche du d�calage d'un au rayon de la jonction
		if (C1.y == C2.y)
		{
			return FuniMath::Vecteur(centre.x,centre.y-FuniMath::sqrt(cable[0]*cable[0] - k*k),centre.z);
		}
		else
		{
			double a = (C2.x - C1.x) / (C1.y - C2.y);
			return centre - ( FuniMath::Vecteur(1, a, 0)/ FuniMath::Vecteur(1, a, 0).norme() * FuniMath::sqrt(cable[0] * cable[0] - k * k));
		}
	}
	//un seul cable
	else if (nbrPole == 1)
	{
		return pole[0] - accroche[0] - FuniMath::Vecteur(0, cable[0], 0);
	}
	else throw 1; // aucun cable pour les calculs
}

void Funibot::test()
{
	//multicable
	if (nbrPole > 1)
	{
		if (nbrPole == 2)std::cout << "fonctionnement 2D\n\n";
		else std::cout << "fonctionnement 3D\n\n";
		
		std::cout << "position des poles:\n";
		for (int i = 0; i < nbrPole; i++)std::cout << pole[i] << "\n";
		std::cout << "\nposition des accroches:\n";
		for (int i = 0; i < nbrPole; i++)std::cout << accroche[i] << "\n";
		std::cout << "\nlongueurs des cables:\n";
		for (int i = 0; i < nbrPole; i++)std::cout << cable[i] << "\n";

		FuniMath::Vecteur pos = getPosition();
		std::cout << "\n\nPosition calculee : " << pos;
		std::cout << "\nlongueurs des cables calculees:\n";
		for (int i = 0; i < nbrPole; i++)std::cout << (pos + accroche[i] - pole[i]).norme() << "\n";
	}
	//un seul cable
	else if (nbrPole == 1)
	{
		std::cout << "fonctionnement 1D\n\n";
		std::cout << "position du pole : " << pole[0];
		std::cout << "\nposition de l'accroche :" << accroche[0];
		std::cout << "\ntaille du cable : " << cable[0];
		FuniMath::Vecteur pos = getPosition();
		std::cout << "\n\nPosition calculee : " << pos;
		std::cout << "\ntaille cable calculee : " << (pos + accroche[0] - pole[0]).norme() << "\n";
	}
	else throw 1; // aucun cable pour les calculs
}