#pragma once

namespace FuniConst
{
	const unsigned char NBR_POLES = 4;
}

namespace FuniMath
{
	// Valeur absolue d'un double
	inline double abs(double u) { return (u >= 0) ? u : -u; }

	// Racine carrée à l'aide de la méthode de Raphson-Newton
	double sqrt(double u, double precision = 0.001);

	//vecteur
	class Vecteur
	{
	public:
		double x, y, z;

		Vecteur(double _x = 0, double _y = 0, double _z = 0)
			:	x(_x), y(_y), z(_z)
			{}
		
		inline double norme_carree() { return (x * x) + (y * y) + (z * z); }
		inline double norme() { return sqrt(norme_carree()); }
		
		inline Vecteur operator+(const Vecteur u) const { return Vecteur(x + u.x, y + u.y, z + u.z); }
		inline Vecteur operator-(const Vecteur u) const { return Vecteur(x - u.x, y - u.y, z - u.z); }
		inline Vecteur operator*(const double u) const { return Vecteur(x * u, y * u, z * u); }
		inline Vecteur operator/(const double u) const { return Vecteur(x / u, y / u, z / u); }
	};

	Vecteur operator*(const double u, const Vecteur v);
}

class Funibot
{
public:
	Funibot();
	void addPole(FuniMath::Vecteur positionPole, FuniMath::Vecteur positionAccroche);
	void setPole(unsigned char index, FuniMath::Vecteur positionPole, FuniMath::Vecteur positionAccroche);
	void setLongueurCable(unsigned char index, double longueur);
	void test();

	FuniMath::Vecteur getPosition();

protected:
	unsigned char nbrPole;
	FuniMath::Vecteur pole[FuniConst::NBR_POLES];
	FuniMath::Vecteur accroche[FuniConst::NBR_POLES];
	double cable[FuniConst::NBR_POLES];
};