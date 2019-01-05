#ifndef __node__
#define __node__

#include <string>
#include <iostream>

using namespace std;

class Node {
	
	public:
		Node();
		string value;
		char value2;
		int priority;
		void print();
		Node * next;
};

#endif
