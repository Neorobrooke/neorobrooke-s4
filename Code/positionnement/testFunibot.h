#pragma once

#include "Funibot.h"
#include <string>
#include <iostream>



namespace FuniTest
{
	struct rapport
	{
		bool reussite = true;
		std::string info = std::string();
		std::string nom = std::string();
	};

	//funimath
	rapport abs();
	rapport sqrt();
	//funibot
	rapport getPosition();
	rapport deplacementDirrectionnel();
	rapport deplacementPosition();

}

std::ostream& operator<< (std::ostream&, FuniTest::rapport);
