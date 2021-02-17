#include "testFunibot.h"
#include <random>

const int MAXINFO = 32;

std::ostream& operator<< (std::ostream& os, FuniTest::rapport rap)
{
	os << "Test: " << rap.nom << "\n";
	if (rap.reussite)
	{
		os << "réussite du test\n";
	}
	else
	{
		os << "échec du test\n";
	}
	os << rap.info;
	os << "\n";
	return os;
}

double rand(double min, double max)
{
	double delta = max - min;
	return ((double)std::rand() / (double)RAND_MAX) * delta + min;
}

Funibot testBot()
{
	std::srand(102545);
	Funibot bot;

	//ajout des poles
	bot.addPole(FuniMath::Vecteur(rand(-2,2),rand(-2,2)+100,rand(-2,2)), FuniMath::Vecteur(rand(-2, 2), rand(-2, 2), rand(-2, 2)));
	bot.addPole(FuniMath::Vecteur(rand(-2, 2)+100, rand(-2, 2)+100, rand(-2, 2)), FuniMath::Vecteur(rand(-2, 2), rand(-2, 2), rand(-2, 2)));
	bot.addPole(FuniMath::Vecteur(rand(-2, 2), rand(-2, 2)+100, rand(-2, 2)+100), FuniMath::Vecteur(rand(-2, 2), rand(-2, 2), rand(-2, 2)));
	bot.addPole(FuniMath::Vecteur(rand(-2, 2)+100, rand(-2, 2)+100, rand(-2, 2)+100), FuniMath::Vecteur(rand(-2, 2), rand(-2, 2), rand(-2, 2)));


	return bot;
}



FuniTest::rapport FuniTest::abs()
{
	int info = 0;
	rapport out;
	out.nom = "abs()";
	for (double i = 0; i < 1000; i += 0.01)
	{
		double absi = FuniMath::abs(i);
		if (i - absi > 0.001 || i - absi < -0.001)
		{
			out.reussite = false;
			out.info += "abs(" + std::to_string(i) + ") != " + std::to_string(i) + "\n";
			info++;
			if (info > MAXINFO)
				return out;
		}

	}

	for (double i = 0; i > -1000; i -= 0.01)
	{
		double absi = FuniMath::abs(i);
		if (i + absi > 0.001 || i + absi < -0.001)
		{
			out.reussite = false;
			out.info += "abs(" + std::to_string(i) + ") == " + std::to_string(absi) + " != " + std::to_string(-i) + "\n";
			info++;
			if (info > MAXINFO)
				return out;
		}

	}

	return out;
}
FuniTest::rapport FuniTest::sqrt()
{
	int info = 0;
	rapport out;
	out.nom = "sqrt()";
	for (double i = 0; i < 1000; i += 0.1)
	{
		double i_carre = i * i;
		double sqrt_i_carre = FuniMath::sqrt(i_carre, 0.0001);

		if (sqrt_i_carre - i > 0.001 || sqrt_i_carre - i < -0.001)
		{
			out.reussite = false;
			out.info += "sqrt(" + std::to_string(i_carre) + ") == " +std::to_string(sqrt_i_carre)+ " != " + std::to_string(i) + "\n";
			info++;
			if (info > MAXINFO)
				return out;
		}
	}
	for (double i = 0; i > -1000; i -= 0.1)
	{
		double i_carre = i * i;
		double sqrt_i_carre = FuniMath::sqrt(i_carre, 0.0001);

		if (sqrt_i_carre + i > 0.001 || sqrt_i_carre + i < -0.001)
		{
			out.reussite = false;
			out.info += "sqrt("+ std::to_string(i) +"^2) == sqrt(" + std::to_string(i_carre) + ") == " + std::to_string(sqrt_i_carre) + " != " + std::to_string(-i) + "\n";
			info++;
			if (info > MAXINFO)
				return out;
		}
	}
	return out;
}

FuniTest::rapport FuniTest::getPosition()
{
	int info = 0;
	rapport out;
	out.nom = "getPosition()";

	Funibot bot = testBot();
	for (double i = 3; i < 97; i+= 4.5)
	{
		for (double j = 0; j < 97; j += 4.5)
		{
			for (double k = 3; k < 97; k += 4.5)
			{
				FuniMath::Vecteur position(i,j,k);
				double cable[4];
				for (int w = 0; w < 4; w++)
				{
					cable[w] = (position - bot.getPoleRelatif(w)).norme();
					bot.setLongueurCable(w, cable[w]);
				}
				FuniMath::Vecteur positionCalcul = bot.getPosition();

				if ((position - positionCalcul).norme_carree() > 0.0000001)
				{
					out.reussite = false;
					out.info += "(" + std::to_string(i) + ", " + std::to_string(j) + ", " + std::to_string(k) + ") != " +
						"(" + std::to_string(positionCalcul.x) + ", " + std::to_string(positionCalcul.y) + ", " + std::to_string(positionCalcul.z) + ")\n";
					info++;
					if (info > MAXINFO)
						return out;
				}

				while (!bot.erreurs.empty())
				{
					out.reussite = false;
					out.info += "erreur id: " + std::to_string(bot.erreurs.takeFront().id) + "\n";
					info++;
					if (info > MAXINFO)
						return out;
				}





			}
		}
	}

	return out;
}


FuniTest::rapport FuniTest::deplacementDirectionnel()
{
	int info = 0;
	rapport out;
	out.nom = "deplacementDirectionnel()";

	Funibot bot = testBot();

	const int nbrPosition = 3;
	const int nbrDirr = 5;
	const double positionTest[nbrPosition] = { 3, 50, 97 };
	const double dirrTest[nbrDirr] = { -1,-0.5,0,0.5,1 };

	double vitesse = 5;
	double pas = 0.1;

	for(int iDirr = 0; iDirr < nbrDirr; iDirr ++)
		for (int jDirr = 0; jDirr < nbrDirr; jDirr++)
			for (int kDirr = 0; kDirr < nbrDirr; kDirr++)
			{
				//vecteur de déplacement
				FuniMath::Vecteur dirr(dirrTest[iDirr], dirrTest[jDirr], dirrTest[kDirr]);
				FuniMath::Vecteur dirrU = dirr / dirr.norme();

				for (int i = 0; i < nbrPosition; i++)
					for (int j = 0; j < nbrPosition; j++)
						for (int k = 0; k < nbrPosition; k++)
						{
							//position départ
							FuniMath::Vecteur depart(positionTest[i], positionTest[j], positionTest[k]);
							//suivie de position
							FuniMath::Vecteur position = depart;
							FuniMath::Vecteur oldPosition = position;
							//mise en place de la longueur des cables
							double cable[4];
							for (int w = 0; w < 4; w++)
							{
								cable[w] = (position - bot.getPoleRelatif(w)).norme();
								bot.setLongueurCable(w, cable[w]);
							}

							//itération du mouvement
							FuniMath::Vecteur estimation = position + dirrU * vitesse * pas; //estimation de la prochaine position
							while (estimation.x < 97 && estimation.x > 3
								&& estimation.y < 97 && estimation.y > 3
								&& estimation.z < 97 && estimation.z > 3)
							{
								//mise à jour des cables
								double vitesseCable[4];
								bot.deplacementDirectionnel(dirr, pas, vitesse, vitesseCable);
								for (int w = 0; w < 4; w++)
								{
									cable[w] += vitesseCable[w] * pas;
									bot.setLongueurCable(w, cable[w]);
								}

								//mise à jours de la position
								oldPosition = position;
								position = bot.getPosition();

								//test de validité
								FuniMath::Vecteur erreur = (position - (oldPosition + dirrU * vitesse * pas)); //erreur de dirrection

								if (erreur.norme_carree() > 0.00001) //erreur de dirrection trop grande
								{
									double fact = erreur.norme_carree();
									out.reussite = false;
									out.info += "déplacement de (" + std::to_string(oldPosition.x) + ", " + std::to_string(oldPosition.y) + ", " + std::to_string(oldPosition.z) + ") vers\n(" +
										std::to_string(dirrU.x * vitesse * pas) + ", " + std::to_string(dirrU.y * vitesse * pas) + ", " + std::to_string(dirrU.z * vitesse * pas) + ") donne\n(" +
										std::to_string(position.x) + ", " + std::to_string(position.y) + ", " + std::to_string(position.z) + ")\n";
									info++;
									if (info > MAXINFO)
										return out;
								}

								while (!bot.erreurs.empty()) //erreur survenue dans le code
								{
									out.reussite = false;
									out.info += "erreur id: " + std::to_string(bot.erreurs.takeFront().id) + "\n";
									info++;
									if (info > MAXINFO)
										return out;
								}

								//reestimation
								estimation = position + dirrU * vitesse * pas;
							}
						}
			}

	

	return out;
}
FuniTest::rapport FuniTest::deplacementPosition()
{
	int info = 0;
	rapport out;
	out.nom = "deplacementPosition()";

	Funibot bot = testBot();

	const int nbrPosition = 5;
	const double positionTest[nbrPosition] = { 3, 26.5, 50, 76.5, 97 };
	
	double vitesse = 5;
	double pas = 0.1;

	for(int debuti = 0; debuti < nbrPosition; debuti++)
		for (int debutj = 0; debutj < nbrPosition; debutj++)
			for (int debutk = 0; debutk < nbrPosition; debutk++)
			{
				FuniMath::Vecteur debut(positionTest[debuti], positionTest[debutj], positionTest[debutk]);
				for (int fini = 0; fini < nbrPosition; fini++)
					for (int finj = 0; finj < nbrPosition; finj++)
						for (int fink = 0; fink < nbrPosition; fink++)
						{
							FuniMath::Vecteur fin(positionTest[fini], positionTest[finj], positionTest[fink]);
							
							//mise en place de la longueur des cables
							double cable[4];
							for (int w = 0; w < 4; w++)
							{
								cable[w] = (debut - bot.getPoleRelatif(w)).norme();
								bot.setLongueurCable(w, cable[w]);
							}
							//estimation de temps
							double estimTemps = (fin - debut).norme() / vitesse;

							//nbr d'itération
							int nbrItt = ((estimTemps / pas) * 1.01) + 1;

							for (int itt = 0; itt <= nbrItt; itt++)
							{
								//déplacement
								double vitesseCable[4];
								bot.deplacementPosition(fin, pas, vitesse, vitesseCable);
								for (int w = 0; w < 4; w++)
								{
									cable[w] += vitesseCable[w] * pas;
									bot.setLongueurCable(w, cable[w]);
								}

								//gestion des erreur
								if (!bot.erreurs.empty())
								{
									out.reussite = false;
									out.info += "erreur dans l'ittération " + std::to_string(itt) + "du déplacement entre\n(" +
										std::to_string(debut.x) + ", " + std::to_string(debut.y) + ", " + std::to_string(debut.z) + ") et\n("+
										std::to_string(fin.x) + ", " + std::to_string(fin.y) + ", " + std::to_string(fin.z) + ")\n";
								}
								while (!bot.erreurs.empty()) //erreur survenue dans le code
								{
									out.info += "erreur id: " + std::to_string(bot.erreurs.takeFront().id) + "\n";
									info++;
									if (info > MAXINFO)
										return out;
								}

							}

							//test de position à la fin du déplacement
							FuniMath::Vecteur positionFin = bot.getPosition();
							if ((positionFin - fin).norme_carree() > 0.00001)
							{
								out.reussite = false;
								out.info += "déplacement de " + std::to_string(debut.x) + ", " + std::to_string(debut.y) + ", " + std::to_string(debut.z) + ") à\n(" +
									std::to_string(positionFin.x) + ", " + std::to_string(positionFin.y) + ", " + std::to_string(positionFin.z) + ") au lieu de\n("+
									std::to_string(fin.x) + ", " + std::to_string(fin.y) + ", " + std::to_string(fin.z) + ")\n";
							}
						}
			}

	return out;
}