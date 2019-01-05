#include "WaitingRoom.hpp"
#include <iostream>
#include <string>

WaitingRoom::WaitingRoom() { // Initial constructor
	for( int i = 0; i < 5; i++) {
	heads[i] = NULL;
	tails[i] = NULL;
	}
}

void WaitingRoom::addPatient(Patient * p) {
	int priority = p->pPriority;
	// Patient priorities are between 0-4
	if(priority > 4 || priority < 0) {
		cout << "addPatient error: invalid priority" << endl;
	} else {
		// If priority level is empty, P becomes head and tail.
		if(heads[priority] == NULL) {
			heads[priority] = p;
			tails[priority] = p;
		} else {
		// Else, attach node to tail.
			tails[priority]->next = p;
			tails[priority] = p;	
		}
	}
}

Patient * WaitingRoom::callPatient() {
	for(int i = 0; i < 5; i++) {
		// If level is empty, move to next level
		if(heads[i] == NULL) {
			continue;
		} else {
			Patient * temp;
			temp = heads[i];
			heads[i] = heads[i]->next;
			return temp;
		}
		
	} return NULL;
}

void WaitingRoom::print() {
	for(int i = 0; i < 5; i++) {
		// Cycle through all levels and print
		Patient * current = heads[i];
		if(heads[i] == NULL) {
			continue;
		}
		
		while(current != NULL)
		{
			current->print();
			if(current->next == NULL) {
				break;
			} else {
				current = current->next;
			}
		}
	}
}


