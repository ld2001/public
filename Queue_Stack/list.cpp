#include "list.hpp"
#include "node.hpp"

List::List () {
	head = NULL;
	tail = NULL;
}
// For enqueue, dequeue, push, and pop, a node must be passed through., 
void List::enqueue (Node * a) {
	if(head == NULL) {
		head = a;
		tail = a;
	} else {
		tail->next = a;
		tail = a;
	}
}

Node * List::dequeue() {
	if(head == NULL) {
		cout << "No head" << endl;
	} else {
		Node * temp = new Node;
		temp = head;
		head = head->next;
		return temp;
	}
}

void List::push (Node * a) {
	if(head == NULL) {
		head = a;
	} else {
		a->next = head;
		head = a;
	}
}

Node * List::pop() {
	if(head == NULL) {
		cout << "No head" << endl;
	} else {
		Node * temp = new Node;
		temp = head;
		head = head->next;
		return temp;
	}
}

void List::print() {
// Change node.cpp print functions to print different items
	Node * current = head;
	while (current != NULL) {
		current->print();
		current = current->next;
	}
}

void List::orderInsert(Node * a) {
// Change the "values" below in order to change the ordering variable. Currently is least to greatest. Flip the sign from greatest to least. (< to >, and <= to >=)

	if(head == NULL) {
		head = a;
		tail = a;
	} else if (head->value > a->value) {
		a->next = head;
		head = a;
	} else {
		Node * current = head;
		while(current->next != NULL && current->next->value <= a->value) {
			current = current->next;
		}
		a->next = current->next;
		current->next = a;
	}
}



