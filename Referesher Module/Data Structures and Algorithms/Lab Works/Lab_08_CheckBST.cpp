#include <iostream>
#include <cstdlib>
#include <cmath>
using namespace std;

struct CheckBST {
    int data;
    CheckBST* left;
    CheckBST* right;
};

CheckBST* genNode(int data) {
    CheckBST* cNode = (CheckBST*) malloc(sizeof(CheckBST));
    cNode->data = data;
    cNode->left = NULL;
    cNode->right = NULL;

    return cNode;
}

bool checkBST(CheckBST* root) {
    int data = root->data;
    if (root->left == NULL && root->right == NULL)
        return true;

    if (data < root->left->data || data > root->right->data)
        return false;
    else {
        bool ret = checkBST(root->left);
        if (ret == false)
            return ret;
        else
            return checkBST(root->right);
    }
    return false;
}

CheckBST* buildTree(int arr[], int i, int size) {
    if (isnan(arr[i]))
        return NULL;
    CheckBST* cNode = genNode(arr[i]);
    if(i <= size) {
        cNode->left = buildTree(arr, 2*i+1, size);
        cNode->right = buildTree(arr, 2*i+2, size);
        // cout << cNode->data << " ";
        return cNode;
    }
    return NULL;
}

int main (){
    int n;
    cout << "How many elements you want to enter: ";
    cin >> n;
    int arr[n];
    cout << "Enter your Elements: \n";
    for (int i = 0; i < n; i++)
        cin >> arr[i];
    CheckBST* root = buildTree(arr, 0, 2);

    cout << root->data << endl;
    cout << root->left->data << endl;
    cout << root->right->data << endl;
    if(checkBST(root))
        cout << "True";
    else
        cout << "False";
    
    
    return 0;
}