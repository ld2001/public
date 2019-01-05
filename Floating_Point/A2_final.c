// Assignment 2 for New Beginnings
// Luke Ding 2018

#include <stdio.h>
#include <math.h>

// Functional prototype for run_frac.
void run_frac (int, int, int, int, int, int, int, int, int);


// Main function is a floating point calculator, taking the number of exp components, frac components, and hex values and calculating the equivalent value in decimal.
int main (int argc, char* argv[]) {

	// Pulls values from Args 1, 2, 3, and assigns to frac, exp, and hexValue
	int frac;
	int exp;
	int hexValue;
	sscanf(argv[1],"%d", &frac);
	sscanf(argv[2],"%d", &exp);
	sscanf(argv[3],"%x", &hexValue);
	
	// cleanedFrac, cleaned exp, and sign are masked values. However, they have not been rightshifted.
	int cleanedFrac = ((int)pow (2, frac) - 1 ) & hexValue;
	int cleanedExp = ((int)(pow(2,exp) - 1) << frac) & hexValue;
	int sign = ((int)(pow(2, frac + exp))) & hexValue;
	int bias = ((int)pow(2, (exp -1))-1);
	int E = ((cleanedExp >> frac) - bias);
	int DE = (1 - bias);

	printf("sign is %d \n", sign);
	printf("cleanExp is %d \n", cleanedExp);
	printf("cleanFrac is %d \n", cleanedFrac);
	printf("Bias is %d \n", bias);
	printf("E is %d \n", E);
	printf("DE is %d \n", DE);

	run_frac(frac, exp, hexValue, cleanedFrac, cleanedExp, sign, bias, E, DE);
}

void run_frac (int frac, int exp, int hexValue, int cleanedFrac, int cleanedExp, int sign, int bias, int E, int DE) { 
	
	// Checks if frac and exp are within guidelines. Calculator works for any array of floating point values. Just change frac and exp limits below.
	if(frac < 2 || frac > 10) {
		printf("Range of fraction must be [2,10]");
	} else if (exp < 3 || exp > 5) {
		printf("Range of exp must be [3,5]");
	} else {

	if((cleanedExp >> frac) == pow(2, exp) - 1) {
		if(cleanedFrac == 0) {
			if(sign == 0) {
				printf("Positive Infinity\n");
			} else {
				printf("Negative Infinity\n");
			}
		
		} else {
				printf("Not a number\n");
		}
	} 
	
	 else if ((cleanedExp >> frac) == 0) {
	// denormalized number (exp all 0s)
		int digits;
		double fractions;
		double total;
			
		//calculates the positive digits (0, since it is denormalized)
		digits = 0;
		//calculates the fractions
		fractions =  (cleanedFrac) / (pow(2, (-1*DE + frac)));
		printf("fractions: %.5f\n",fractions);
		total = digits + fractions;

		if(sign == 0) {
			printf("Decimal equivalent: %E\n", total);
		} else {
			total *= -1;
			printf("Decimal equivlaent: %E\n", total);
		       }

	} else {
		int digits;
		double fractions;
		double total;
			
		//calculates the positive digits
		digits = (cleanedFrac >> (frac - E)) + (int)pow(2,(E));
		//calculates the fractions
		fractions =  (((int)pow(2, frac - E) - 1) & cleanedFrac) / (pow(2, frac - E));
		printf("fractions: %.5f\n",fractions);
		total = digits + fractions;

		if(sign == 0) {
			printf("Decimal equivalent: %.20f\n", total);
		} else {
			total *= -1;
			printf("Decimal equivalent: %.20f\n", total);
			}
		}	
	}

}
