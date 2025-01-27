#include <iostream>
using namespace std;

int top = -1, stackSize;

bool isEmpty() { return top < 0; }
bool isFull() { return top == stackSize - 1; }

void push(int *stack, int data) {
    if (isFull()) {
        cout << "Stack is full.\n";
        return;
    }
    stack[++top] = data;
}

int pop(int *stack) {
    if (isEmpty()) {
        cout << "Stack is empty.\n";
        return -1;
    }
    return stack[top--];
}

int peek(int *stack) {
    if (isEmpty()) {
        cout << "Stack is empty.\n";
        return -1;
    }
    return stack[top];
}


int* nextGreaterElements(int nums[], int n) {
    int* stack = new int[n];

    int* result = new int[n];
    for (int i = 0; i < n; i++) result[i] = -1;

    // First Approach
    // for (int i = 0; i < 2 * n; i++) {
    //     while (!isEmpty() && nums[peek(stack)] < nums[i % n])
    //         result[pop(stack)] = nums[i % n];

    //     if (i < n) push(stack, i);
    // }

    // Second Approach
    int j;
    for (int i = 0; i < n; i++) {
        j = 0;
        while(j < n){
            while (!isEmpty() && nums[peek(stack)] < nums[j % n]) {
                result[pop(stack)] = nums[j % n];
                if (j % n == i) break;
                j++;
            }
            if (j < n) push(stack, j);
            j++;
        }
    }

    delete[] stack;
    return result;
}

int main() {
    int nums[] = {1, 2, 1};
    stackSize = sizeof(nums) / sizeof(nums[0]);

    int* result = nextGreaterElements(nums, stackSize);

    cout << "Resulting array: ";
    for (int i = 0; i < stackSize; i++)
        cout << result[i] << " ";
    cout << endl;

    delete[] result;
    return 0;
}
