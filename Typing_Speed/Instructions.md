Typing speed game

You are to implement a game that tests a user's typing speed.  The game randomly chooses words from an array of strings containing "The", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog".   Each word must appear exactly once.  The program should output the time it takes for the user to correctly enter the entire array of words.  If the user incorrectly types a word, the program must prompt the user to retype the incorrect word.

Rules and requirements
	Random permutation of words should be generated via calls to srand() and rand()
	Seed srand() using the usec field from a call to gettimeofday().
	Each permutation of the words must be possible.
	Ensure that your random permutation is generated using a minimal number of rand() calls

