#ifndef __WaitingRoom__
#define __WaitingRoom__
#include "Patient.hpp"

class WaitingRoom {
	public:
		WaitingRoom();
		// Heads and tails are single arrays of pointers to the first patient of every priority level.
		Patient * heads[5];
		Patient * tails[5];
		void addPatient(Patient *);
		Patient * callPatient();
		void print();
};

#endif
