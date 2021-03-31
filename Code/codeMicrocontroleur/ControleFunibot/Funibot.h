#pragma once
#undef abs
#undef sqrt

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

	bool inTriangleXY(const Vecteur A, const Vecteur B, const Vecteur C, const Vecteur P); //retourne vrai si P est dans le triangle A,B,C
	bool inConvexXY(const Vecteur* Cotes, const int nbrCotes, const Vecteur P); //retourne vrai si P est dans le polynome convexe formé par les cotes
}

class Funibot
{
public:
	Funibot();
	GestionErreurs::PileErreurs erreurs;
	void addPole(FuniMath::Vecteur positionPole, FuniMath::Vecteur positionAccroche);
	void setPole(unsigned char index, FuniMath::Vecteur positionPole, FuniMath::Vecteur positionAccroche);
	void setLongueurCable(unsigned char index, double longueur);

	unsigned char getNbrPole(){return nbrPole;}
	FuniMath::Vecteur getPole(unsigned char index);
	FuniMath::Vecteur getAccroche(unsigned char index);
	double getLongueurCable(unsigned char index);
	FuniMath::Vecteur getPoleRelatif(unsigned char index); //Pole - accroche

	FuniMath::Vecteur getPosition();
	double* deplacementDirectionnel(FuniMath::Vecteur dir, double pasTemps, double vitesse, double* vitesseCable);
	double* deplacementPosition(FuniMath::Vecteur pos, double pasTemps, double vitesse, double* vitesseCable);

	void setupSafeZone(double securite_cote = 0, double securite_toit = 200);
	bool isSafe(FuniMath::Vecteur P);
	void setSol(double val_sol);
	double getSol();



protected:
	unsigned char nbrPole;
	FuniMath::Vecteur pole[FuniConst::NBR_POLES];
	FuniMath::Vecteur accroche[FuniConst::NBR_POLES];
	double cable[FuniConst::NBR_POLES];

	FuniMath::Vecteur safeCorner[FuniConst::NBR_POLES];
	double toit;
	double sol;
	bool hasSol;
};