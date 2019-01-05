#ifndef __Patient__
#define __Patient__

#include <iostream>
#include <string>
using namespace std;

class Patient {
	public:
		Patient();
		string pName;
		int pPriority;
		string pSymptom;
		Patient * next;
		void print();
};

#endif
