Programming Assignment

The goal of this program is to implement an IEEE floating point parser for an arbitrary number of bit settings.  Your program will take 3 arguments.  The first argument is the number of fraction bits (n) between 2 and 10 to be used in the representation.  The second argument is the number of exponent bits (k) between 3 and 5 to be used in the representation.  Finally, the third argument is the hexadecimal representation of the number you want to parse assuming the settings given in the first two arguments. 

	sign (1 bit)	
	exp (# of bits specified in argv[2])
	frac (# of bits specified in argv[1])

The program will then print out the floating point value associated with the given bit pattern.  For example, consider the program execution "fp_parse 4 4 a8".  The format of the corresponding representation is shown below. 
	sign (1 bit)	
	exp (4 bits)
	frac (4 bits)

Given the input "a8", the program should parse the hex digits into corresponding bit fields.  Thus, separating out "a8" gives you 0 1010 1000 for the 3 fields.  (Note that we 0-pad the most-significant bits as needed).  From this, the exp field is 10 (in decimal) and the frac field is 1⁄2.  With a Bias of 7, the resultingvalue M*2E will be M = 1+1⁄2 = 3⁄2 , E = 10 - 7 = 3.  Thus, the output will be 12.0.

mashimaro % fp_parse
Usage: fp_parse <# of frac_bits> <# of exp_bits> <hex_to_convert>

mashimaro % fp_parse 11 4 33f
Illegal number of fraction bits (11).  Should be between 2 and 10

mashimaro % fp_parse 4 8 33f
Illegal number of exponent bits (8).  Should be between 3 and 5

mashimaro % fp_parse 4 4 1af
-15.500000

mashimaro % fp_parse 4 4 af
15.500000

mashimaro % fp_parse 3 3 3c
NaN

mashimaro % fp_parse 3 3 38
+inf

mashimaro % fp_parse 3 3 78
-inf

mashimaro % fp_parse 3 3 26
3.500000

mashimaro % fp_parse 3 3 18
1.000000

mashimaro % fp_parse 3 3 3f
NaN

mashimaro % fp_parse 3 3 37
15.000000
