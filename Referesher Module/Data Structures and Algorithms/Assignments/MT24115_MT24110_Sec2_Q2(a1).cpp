#include <iostream>
using namespace std;

int rear = -1, front = 0;
int queueSize;

bool isEmpty() {
    return front > rear;
}

bool isFull() {
    return rear == queueSize - 1;
}

void enQueue(int *queue, int data) {
    if (isFull()) {
        cout << "Queue is full...\n";
        return;
    }
    queue[++rear] = data;
}

int deQueue(int *queue) {
    if (isEmpty()) {
        cout << "Queue is empty.\n";
        return -1;
    }
    return queue[front++];
}

void displayFront(int *queue) {
    if (isEmpty()) {
        cout << "Queue is empty.\n";
        return;
    }
    cout << "Front index: " << front << " | Value: " << queue[front] << "\n";
}

void displayRear(int *queue) {
    if (isEmpty()) {
        cout << "Queue is empty.\n";
        return;
    }
    cout << "Rear index: " << rear << " | Value: " << queue[rear] << "\n";
}

void displayQueue(int *queue) {
    if (isEmpty()) {
        cout << "Queue is empty.\n";
        return;
    }
    for (int i = front; i <= rear; i++)
        cout << "| " << queue[i] << " | ";
    cout << "\n";
}

int main() {
    int *queue, dec, value;
    char ch = 'n';
    cout << "Enter maximum size of queue: ";
    cin >> queueSize;
    queue = new int[queueSize];

    while (true) {
        cout << "\nPerformable Operations:\n";
        cout << "1. EnQueue\n2. DeQueue\n3. DisplayFront\n4. DisplayRear\n5. Exit\n";
        cout << "Enter your decision: ";
        cin >> dec;
        switch (dec) {
            case 1:
                cout << "Enter value to EnQueue: ";
                cin >> value;
                enQueue(queue, value);
                break;
            case 2:
                value = deQueue(queue);
                if (value != -1)
                    cout << "Dequeued value: " << value << "\n";
                break;
            case 3:
                displayFront(queue);
                break;
            case 4:
                displayRear(queue);
                break;
            case 5:
                delete[] queue;
                return 0;
            default:
                cout << "Invalid choice...\n";
        }
        cout << "******* Queue Status *******\n";
        displayQueue(queue);
    }

    return 0;
}
