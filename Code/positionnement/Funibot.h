#pragma once

namespace FuniConst
{
    const unsigned char NBRPOLE = 4;
}

namespace FuniMath
{
    //valeur absolue
    double abs(double u);

    //racine carrée à l'aide de la méthode Raphson-Newton
    double sqrt(double u, double precision = 0.001);

    //vecteur
    class vecteur
    {
    public:
        double x, y, z;
        vecteur(double _x = 0, double _y = 0, double _z = 0) :x(_x), y(_y), z(_z) {}
        double norm() { return sqrt(x * x + y * y + z * z); }
        double norm2() { return x * x + y * y + z * z; }
        vecteur operator + (const vecteur u) const { return vecteur(x + u.x, y + u.y, z + u.z); }
        vecteur operator - (const vecteur u) const { return vecteur(x - u.x, y - u.y, z - u.z); }
        vecteur operator * (const double u)  const { return vecteur(x * u, y * u, z * u); }
        vecteur operator / (const double u)  const { return vecteur(x / u, y / u, z / u); }
    };
    vecteur operator * (const double u, const vecteur v);

}


class Funibot
{
protected:
    unsigned char nbrPole;
    FuniMath::vecteur pole[FuniConst::NBRPOLE];
    FuniMath::vecteur accroche[FuniConst::NBRPOLE];
    double cable[FuniConst::NBRPOLE];

public:
    Funibot();
    void addPole(FuniMath::vecteur positionPole, FuniMath::vecteur positionAccroche);
    void setPole(unsigned char index, FuniMath::vecteur positionPole, FuniMath::vecteur positionAccroche);
    void setLongueurCable(unsigned char index, double longueur);
    void test();

    FuniMath::vecteur getPosition();


};