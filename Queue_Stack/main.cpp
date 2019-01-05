#include <iostream>
#include <string>
#include <cmath>
#include <fstream>
#include "node.hpp"
#include "list.hpp"
#include "functions.hpp"

using namespace std;

int main () { 	

	List initial;

	char command = '\0';
		
	do {	
		cout << "Please enter the next command:  (Q)ueue, (D)equeue, P(U)sh, P(O)p, (P)rint, O(R)dered Insert, and E(X)it. Be aware, commands are case sensitive: " << endl;
		cin >> command;
		cin.ignore();
		if(command == 'Q') {
			Node * temp = new Node;
			cout << "Please enter a value: " << endl;
			getline(cin, temp->value);
			initial.enqueue(temp);
		}
		else if (command == 'D') initial.dequeue();
		else if (command == 'U') {
			Node * temp = new Node;
			cout << "Please enter a value: " << endl;
			getline(cin, temp->value);
			initial.push(temp);
		}
		else if (command == 'X');
		else if (command == 'O') initial.pop();
		else if (command == 'P') initial.print();
		else if (command == 'R') {
			Node * temp = new Node;
			cout << "Please enter a value: " << endl;
			getline(cin, temp->value);
			initial.orderInsert(temp);
		}
		else cout << "Please enter a valid command" << endl;
	} while (command != 'X'); 

}
