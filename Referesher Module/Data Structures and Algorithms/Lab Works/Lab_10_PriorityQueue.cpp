#include <iostream>
#include <vector>
using namespace std;

struct Element {
    int data;
    int priority;
};

struct PriorityQueue {
    vector<Element> elements;
    int capacity;
    int curSize;

    PriorityQueue(int cap) {
        capacity = cap;
        curSize = 0;
        elements.resize(capacity + 1);  // Using 1-based indexing for convenience
    }
};

void swapLarge(Element &a, Element &b) {
    Element temp = a;
    a = b;
    b = temp;
}

void maxHeapify(PriorityQueue* queue, int index) {
    int largest = index;
    int left = 2 * index;
    int right = 2 * index + 1;

    if (left <= queue->curSize && queue->elements[left].priority > queue->elements[largest].priority) 
        largest = left;
    if (right <= queue->curSize && queue->elements[right].priority > queue->elements[largest].priority) 
        largest = right;

    if (largest != index) {
        swapLarge(queue->elements[largest], queue->elements[index]);
        maxHeapify(queue, largest);
    }
}

void insertElements(PriorityQueue* queue, int data, int priority) {
    if (queue->curSize >= queue->capacity) {
        cout << "Priority queue overflow" << endl;
        return;
    }

    queue->curSize++;
    int index = queue->curSize;
    queue->elements[index] = {data, priority};

    while (index > 1 && queue->elements[index / 2].priority < queue->elements[index].priority) {
        swapLarge(queue->elements[index], queue->elements[index / 2]);
        index = index / 2;
    }
}

Element peakMax(PriorityQueue* queue) {
    if (queue->curSize <= 0) {
        cout << "Priority queue underflow" << endl;
        return {-1, -1};
    }

    if (queue->curSize == 1) {
        queue->curSize--;
        return queue->elements[1];
    }

    Element root = queue->elements[1];
    queue->elements[1] = queue->elements[queue->curSize];
    queue->curSize--;
    maxHeapify(queue, 1);

    return root;
}

void printQueue(PriorityQueue* queue) {
    if (queue->curSize == 0){
        cout << "\nQueue is empty...\n";
        return;
    }

    for (int i = 1; i <= queue->curSize; i++) {
        cout << "Data: " << queue->elements[i].data << ", Priority: " << queue->elements[i].priority << " \n";
    }
    cout << endl;
}

int main() {
    PriorityQueue* queue = new PriorityQueue(10);
    int choice, data, priority;

    while (true) {
        cout << "Menu:\n";
        cout << "1. Insert an element\n";
        cout << "2. Delete the highest priority element\n";
        cout << "3. Print the elements of the priority queue\n";
        cout << "4. Exit\n";
        cout << "Enter your choice: ";
        cin >> choice;

        switch (choice) {
            case 1:
                cout << "Enter data: ";
                cin >> data;
                cout << "Enter priority: ";
                cin >> priority;
                insertElements(queue, data, priority);
                break;
            case 2: {
                Element max = peakMax(queue);
                if (max.data != -1) {
                    cout << "Deleted element with data: " << max.data << " and priority: " << max.priority << endl;
                }
            }   
                break;
            case 3:
                printQueue(queue);
                break;
            case 4:
                cout << "Exiting..." << endl;
                delete queue;
                return 0;
            default:
                cout << "Invalid choice, please try again." << endl;
        }
    }

    return 0;
}