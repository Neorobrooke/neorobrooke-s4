#include "Funibot.h"
#include "iostream"

FuniMath::vecteur operator * (const double u, const FuniMath::vecteur v) { return FuniMath::vecteur(v.x * u, v.y * u, v.z * u); }

//valeur absolue
double FuniMath::abs(double u)
{
	if (u >= 0) return u;
	else return -u;
}

//racine carrée à l'aide de la méthode Raphson-Newton
double FuniMath::sqrt(double u, double precision)
{
	double est = u / 2;
	while (abs((est * est) - u) > precision)
	{
		est -= (est * est - u) / (2 * est);
	}
	return est;
}

std::ostream& operator << (std::ostream& ios, FuniMath::vecteur& vect)
{
	ios << "(" << vect.x << "; " << vect.y << ";" << vect.z << ")";
	return ios;
}

Funibot::Funibot():nbrPole(0)
{
	for (unsigned char i = 0; i < FuniConst::NBRPOLE; i++)
	{
		cable[i] = 0;
	}
}

void Funibot::addPole(FuniMath::vecteur positionPole, FuniMath::vecteur positionAccroche)
{
	if (nbrPole == FuniConst::NBRPOLE)throw 1; //dépassement du nombre de pole maximum
	pole[nbrPole] = positionPole;
	accroche[nbrPole] = positionAccroche;
	nbrPole++;
}

void Funibot::setPole(unsigned char index, FuniMath::vecteur positionPole, FuniMath::vecteur positionAccroche)
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

FuniMath::vecteur Funibot::getPosition()
{
	//plus de deux cables
	if (nbrPole > 2)
	{
		//vérifiactions
		for (int i = 0; i < nbrPole; i++)
			for (int j = i+1; j < nbrPole; j++)
			{
				double distij = (pole[i] - accroche[i] - pole[j] + accroche[j]).norm2();
				if (sqrt(distij) > (cable[i] + cable[j])) throw 2; //cables trop court
			}

		// points
		FuniMath::vecteur C1 = pole[0] - accroche[0];
		FuniMath::vecteur C2 = pole[1] - accroche[1];
		FuniMath::vecteur C3 = pole[2] - accroche[2];

		if (C1.z == C2.z && C1.z == C3.z) throw 5; //allignement en z
		if (C1.x == C2.x && C1.x == C3.x) throw 5; //allignement en x

		//centres de jonction
		FuniMath::vecteur Dirr1 = C2 - C1;
		FuniMath::vecteur Dirr2 = C3 - C1;

		double dist1 = Dirr1.norm();
		double dist2 = Dirr2.norm();


		double r1Carr = cable[0]* cable[0];
		double k1 = (r1Carr - (cable[1] * cable[1]) + (dist1 * dist1)) / (2 * dist1);
		double k2 = (r1Carr - (cable[2] * cable[2]) + (dist2 * dist2)) / (2 * dist2);

		FuniMath::vecteur centre1 = (Dirr1 * k1 / dist1) + C1;
		FuniMath::vecteur centre2 = (Dirr2 * k2 / dist2) + C1;

		//fabrication de droites
		double a1,a2,b1,b2;
		bool xPos1 = false, xPos2 = false;

		if (C1.z == C2.z)
		{
			a1 = centre1.x;
			xPos1 = true;
		}
		else
		{
			a1 = -Dirr1.x / Dirr1.z;
			b1 = centre1.z - a1 * centre1.x;
		}

		if (C1.z == C3.z)
		{
			a2 = centre2.x;
			xPos2 = true;
		}
		else
		{
			a2 = -Dirr2.x / Dirr2.z;
			b2 = centre2.z - a2 * centre2.x;
		}

		//résolution finale
		double posX;
		double posZ;

		if (xPos1)
		{
			posX = a1;
			posZ = a2 * posX + b2;
		}
		else if (xPos2)
		{
			posX = a2;
			posZ = a1 * posX + b1;
		}
		else
		{
			posX = (b2 - b1) / (a1 - a2);
			posZ = a1 * posX + b1;
		}

		double posYCarr = r1Carr - posX * posX - posZ * posZ;
		if (posYCarr < 0)throw 6;//racine négative
		double posY = C1.y - sqrt(posYCarr);
		return FuniMath::vecteur(posX, posY, posZ);


	}
	//deux cables
	else if (nbrPole == 2)
	{
		// calculs pole relatif
		FuniMath::vecteur C1 = pole[0] - accroche[0];
		FuniMath::vecteur C2 = pole[1] - accroche[1];
		FuniMath::vecteur Dirr = C2 - C1;
		double dist = Dirr.norm();

		if (dist > (cable[0] + cable[1])) throw 2; //cables trop court
		if ((dist * dist + cable[1] * cable[1]) < (cable[0] * cable[0]))throw 3; //cable 0 trop long
		if ((dist * dist + cable[0] * cable[0]) < (cable[1] * cable[1]))throw 4; //cable 1 trop long


		double k = ((cable[0]) * (cable[0]) - (cable[1] * cable[1]) + (dist * dist)) / (2*dist);
		FuniMath::vecteur centre = (Dirr * k / dist) + C1;
		
		if (C1.y == C2.y)
		{
			return FuniMath::vecteur(centre.x,centre.y-FuniMath::sqrt(cable[0]*cable[0] - k*k),centre.z);
		}
		else
		{
			double a = (C2.x - C1.x) / (C1.y - C2.y);
			return centre - ( FuniMath::vecteur(1, a, 0)/ FuniMath::vecteur(1, a, 0).norm() * FuniMath::sqrt(cable[0] * cable[0] - k * k));
		}
	}
	//un seul cable
	else if (nbrPole == 1)
	{
		return pole[0] - accroche[0] - FuniMath::vecteur(0, cable[0], 0);
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

		FuniMath::vecteur pos = getPosition();
		std::cout << "\n\nPosition calculee : " << pos;
		std::cout << "\nlongueurs des cables calculees:\n";
		for (int i = 0; i < nbrPole; i++)std::cout << (pos + accroche[i] - pole[i]).norm() << "\n";
	}
	//un seul cable
	else if (nbrPole == 1)
	{
		std::cout << "fonctionnement 1D\n\n";
		std::cout << "position du pole : " << pole[0];
		std::cout << "\nposition de l'accroche :" << accroche[0];
		std::cout << "\ntaille du cable : " << cable[0];
		FuniMath::vecteur pos = getPosition();
		std::cout << "\n\nPosition calculee : " << pos;
		std::cout << "\ntaille cable calculee : " << (pos + accroche[0] - pole[0]).norm() << "\n";
	}
	else throw 1; // aucun cable pour les calculs
}