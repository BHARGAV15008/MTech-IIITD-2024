#include <iostream>
using namespace std;

int top = -1, stackSize;

bool isEmpty() { return top < 0; }
bool isFull() { return top == stackSize - 1; }

int pop(int *stack) {
    if (isEmpty()) {
        cout << "Stack is empty.\n";
        return -1;
    }
    return stack[top--];
}

void push(int *stack, int data) {
    if (isFull()) {
        cout << "Stack is full.\n";
        return;
    }
    stack[++top] = data;
}

void displayTop(int *stack) {
    if (isEmpty()) {
        cout << "Stack is empty.\n";
        return;
    }
    cout << "Top index: " << top << " | Value: " << stack[top] << "\n";
}

int peek(int *stack, int index) {
    if (index < 0 || index > top) {
        cout << "Invalid index.\n";
        return -1;
    }
    return stack[index];
}

void displayStack(int *stack) {
    if (isEmpty()) {
        cout << "Stack is empty.\n";
        return;
    }
    for (int i = 0; i <= top; i++)
        cout << "| " << stack[i] << " | ";
    cout << "\n";
}

int main() {
    int *stack, dec, value;
    char ch = 'n';
    cout << "Enter maximum stackSize of stack: ";
    cin >> stackSize;
    stack = new int[stackSize];

    while (true) {
        cout << "\nPerformable Operations:\n";
        cout << "1. Push\n2. Pop\n3. Top\n4. Peek\n5. Exit\n";
        cout << "Enter your decision: ";
        cin >> dec;
        switch (dec) {
            case 1:
                cout << "Enter value to push: ";
                cin >> value;
                push(stack, value);
                break;
            case 2:
                value = pop(stack);
                if (value != -1)
                    cout << "Popped value: " << value << "\n";
                break;
            case 3:
                displayTop(stack);
                break;
            case 4:
                cout << "Enter index to peek: ";
                int index;
                cin >> index;
                value = peek(stack, index);
                if (value != -1)
                    cout << "Peeked value: " << value << "\n";
                break;
            case 5:
                delete[] stack;
                return 0;
            default:
                cout << "Invalid choice...\n";
                return 0;
        }
        displayStack(stack);
    }

    return 0;
}
