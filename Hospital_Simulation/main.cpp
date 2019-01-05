#include <iostream>
#include <string>
#include "WaitingRoom.hpp"
#include "Patient.hpp"
#include <unistd.h>

using namespace std;

int main () {
	cout << "Computer starting..............." << endl;
	usleep(3000000);

	WaitingRoom wr;

	char command = '\0';

	do { 	// Asks user if they want to continue inputting patients
		cout << "Please enter the capital letter 'O' if you have no more patients. Enter any other character if you have patients. Do not enter more than one character." << endl;
		cin >> command;
		cin.ignore();
		if(command == 'O') break;

		Patient * temp = new Patient;

		cout << "Please enter the patient's name:" << endl;
		getline(cin,temp->pName);
		cout << "Please enter the patient's symptom." << endl;
		getline(cin,temp->pSymptom);
		cout << "Please enter the patient's priority number" << endl;
		cin >> temp->pPriority;
		wr.addPatient(temp);

		} while (command != 'O'); 

	do {	// Requests patient to either call a patient and remove from list, print hte waiting room, or exit program..
		cout << "Please enter the next command: (C)all patient, (P)rint waiting room, e(X)it. Be aware, commands are case sensitive: " << endl;
		cin >> command;
		cin.ignore();
		if (command == 'C')  wr.callPatient()->print();
		else if (command == 'P') wr.print();
		else if (command == 'X');
		else cout << "Please enter a valid command" << endl;
		}while (command != 'X'); 
	
}
