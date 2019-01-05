#ifndef __list__
#define __list__

#include "node.hpp"

using namespace std;

class List {
	
	public:
		List();
		Node * head;
		Node * tail;
		void enqueue(Node *);
		Node * dequeue();
		void push(Node *);
		Node * pop();
		void orderInsert(Node *);
		void print();
};

#endif

