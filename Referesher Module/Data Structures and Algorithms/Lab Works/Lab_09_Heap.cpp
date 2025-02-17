#include <iostream>
#include <vector>
using namespace std;

struct Heap {
    int data;
    Heap *heapLeft, *heapRight;
};

Heap* genHeapNode(int value) {
    Heap* cNode = new Heap;
    cNode->data = value;
    cNode->heapLeft = nullptr;
    cNode->heapRight = nullptr;
    return cNode;
}

// Swapping value of node by using reference operator variable;
void swap(int &a, int &b) {
    int temp = a;
    a = b;
    b = temp;
}

void heapify(Heap* root) {
    if (root == nullptr) return;
    
    Heap* largest = root;
    if (root->heapLeft != nullptr && root->heapLeft->data > largest->data) {
        largest = root->heapLeft;
    }
    if (root->heapRight != nullptr && root->heapRight->data > largest->data) {
        largest = root->heapRight;
    }
    if (largest != root) {
        swap(root->data, largest->data);
        heapify(largest);
    }
}

Heap* insertHeapNode(Heap* root, int value) {
    Heap* cNode = genHeapNode(value);

    if (root == nullptr) {
        return cNode;
    }

    if (!root->heapLeft) {
        root->heapLeft = cNode;
    } else if (!root->heapRight) {
        root->heapRight = cNode;
    } else {
        if (!root->heapLeft->heapLeft || !root->heapLeft->heapRight) {
            insertHeapNode(root->heapLeft, value);
        } else {
            insertHeapNode(root->heapRight, value);
        }
    }
    heapify(root);
    return root;
}

Heap* getLastNode(Heap* root, Heap** parentNode) {
    if (root->heapLeft == nullptr && root->heapRight == nullptr) return root;

    if (root->heapLeft != nullptr && root->heapRight == nullptr) {
        *parentNode = root;
        return root->heapLeft;
    }
    
    if (root->heapRight != nullptr) {
        *parentNode = root;
        return root->heapRight;
    }
    
    Heap* leftResult = getLastNode(root->heapLeft, parentNode);
    if (leftResult != nullptr) return leftResult;
    
    return getLastNode(root->heapRight, parentNode);
}

Heap* deleteHeapMaxNode(Heap* root) {
    if (root == nullptr) return nullptr;

    if (root->heapLeft == nullptr && root->heapRight == nullptr) {
        delete root;
        return nullptr;
    }

    Heap* parentNode = nullptr;
    Heap* lastNode = getLastNode(root, &parentNode);

    if (parentNode->heapLeft == lastNode) {
        parentNode->heapLeft = nullptr;
    } else {
        parentNode->heapRight = nullptr;
    }

    root->data = lastNode->data;
    delete lastNode;

    heapify(root);
    return root;
}


// Here we using BFS means level to level printing 
void levelWiseTraversal(Heap* root) {
    if (root == nullptr) return;

    vector<Heap*> liveLevel;
    liveLevel.push_back(root);

    while (!liveLevel.empty()) {
        vector<Heap*> nextLevel;
        for (Heap* tNode : liveLevel) {
            cout << tNode->data << " ";
            if (tNode->heapLeft != nullptr) {
                nextLevel.push_back(tNode->heapLeft);
            }
            if (tNode->heapRight != nullptr) {
                nextLevel.push_back(tNode->heapRight);
            }
        }
        liveLevel = nextLevel;
    }
}

int main() {
    Heap* root = nullptr;
    int choice;

    while (true) {
        cout << "\n\nHere perform Heap Data Structure Operations: \n";
        cout << "1. Insert Element\n2. Delete Max Node\n3. Exit\n";
        cout << "Enter your choice here: ";
        cin >> choice;
        switch (choice) {
        case 1:
            int value;
            cout << "Enter the value you want to insert: ";
            cin >> value;
            root = insertHeapNode(root, value);
            break;

        case 2:
            root = deleteHeapMaxNode(root);
            break;

        case 3:
            cout << "\nExit...\n";
            return 0;
        
        default:
            cout << "\nInvalid choice. Please, try again...\n";
            break;
        }
        cout << "\n";
        levelWiseTraversal(root);
        cout << "\n";
    }

    return 0;
}