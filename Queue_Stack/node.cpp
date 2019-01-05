#include <iostream>
#include "node.hpp"
using namespace std;

Node::Node() {
	next = NULL;
	value2 = '\0';
	priority = 0;
}

void Node::print() {
	cout << "String value: " << value << endl;
	cout << "Char value: " << value2 << endl;
	cout << "Int value: " << priority << endl;
}
