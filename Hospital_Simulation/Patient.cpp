#include "Patient.hpp"

Patient::Patient() {
	next = NULL;
}

void Patient::print() {
	// Prints the patient name, priority, and symptom.
	cout << "Patient name: " << pName << endl;
	cout << "Patient priority: " << pPriority << endl;
	cout << "Patient symptom: " << pSymptom << endl;

}
