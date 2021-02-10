#pragma once

#include"GestionErreurs.h"

namespace FuniConst
{
	const unsigned char NBR_POLES = 4;
}

namespace FuniMath
{
	// Valeur absolue d'un double
	inline double abs(double vec) { return (vec >= 0) ? vec : -vec; }

	// Racine carrée à l'aide de la méthode de Raphson-Newton
	double sqrt(double vec, double precision = 0.0001);

	//vecteur
	class Vecteur
	{
	public:
		double x, y, z;

		Vecteur(double _x = 0, double _y = 0, double _z = 0)
			: x(_x), y(_y), z(_z)
		{}

		inline double norme_carree() { return (x * x) + (y * y) + (z * z); }
		inline double norme() { return FuniMath::sqrt(norme_carree()); }
		inline double produitScalaire(const Vecteur vec) const { return x * vec.x + y * vec.y + z * vec.z; }
		inline Vecteur produitVectoriel(const Vecteur vec) const { return Vecteur(y * vec.z - vec.y * z, z * vec.x - vec.z * x, x * vec.y - vec.x * y); }

		inline Vecteur operator+(const Vecteur vec) const { return Vecteur(x + vec.x, y + vec.y, z + vec.z); }
		inline Vecteur operator-(const Vecteur vec) const { return Vecteur(x - vec.x, y - vec.y, z - vec.z); }
		inline Vecteur operator*(const double vec) const { return Vecteur(x * vec, y * vec, z * vec); }
		inline Vecteur operator/(const double vec) const { return Vecteur(x / vec, y / vec, z / vec); }
	};

	Vecteur operator*(const double vec, const Vecteur v);
}

class Funibot
{
public:
	Funibot();
	GestionErreurs::PileErreurs erreurs;
	void addPole(FuniMath::Vecteur positionPole, FuniMath::Vecteur positionAccroche);
	void setPole(unsigned char index, FuniMath::Vecteur positionPole, FuniMath::Vecteur positionAccroche);
	void setLongueurCable(unsigned char index, double longueur);
	void test();

	FuniMath::Vecteur getPole(unsigned char index);
	FuniMath::Vecteur getAccroche(unsigned char index);
	FuniMath::Vecteur getLongueurCable(unsigned char index);
	FuniMath::Vecteur getPoleRelatif(unsigned char index); //Pole - accroche

	FuniMath::Vecteur getPosition();
	double* deplacementDirectionnel(FuniMath::Vecteur dir, double pasTemps, double vitesse, double* vitesseCable);
	double* deplacementPosition(FuniMath::Vecteur pos, double pasTemps, double vitesse, double* vitesseCable);



protected:
	unsigned char nbrPole;
	FuniMath::Vecteur pole[FuniConst::NBR_POLES];
	FuniMath::Vecteur accroche[FuniConst::NBR_POLES];
	double cable[FuniConst::NBR_POLES];
};