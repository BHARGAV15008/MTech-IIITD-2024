#include <iostream>
#include <cstdlib>
using namespace std;

struct BuildTree {
    int data;
    BuildTree* left;
    BuildTree* right;
};

void traversal(BuildTree* root) {
    if(root != NULL){
        cout << root->data << " ";
        traversal(root->left);
        traversal(root->right);
    }
    // cout << "null \n"; 
}

BuildTree* genTreeNode(int val) {
    BuildTree* cNode = (BuildTree*) malloc(sizeof(BuildTree));
    cNode->data = val;
    cNode->left = NULL;
    cNode->right = NULL;

    return cNode;
}

int findVal(int arr[], int val, int size) {
    for(int i = 0; i <= size; i++){
        if(arr[i] == val) return i;
    }
    return -1;
}

BuildTree* constructTree(BuildTree* root, int postOrder[], int inOrder[], int postSize, int inSize, int postFrom, int inFrom) {
    BuildTree* cNode = genTreeNode(postOrder[postSize]);
    int inPos = findVal(inOrder, postOrder[postSize], inSize);
    int postPos = findVal(postOrder, inOrder[inSize-1], postSize);
    if (postFrom > postSize || inFrom > inSize)
        return root;
    else{
        cNode->right = constructTree(cNode->right, postOrder, inOrder, postSize-1, inSize, postPos, inPos+1);
        cNode->left = constructTree(cNode->left, postOrder, inOrder, postPos-1, inPos-1, postFrom, inFrom);
        root = cNode;
    }
    return root;
    
}

int main (){
    int inOrder[10] = {9,3,15,20,7};
    int postOrder[10]  = {9,15,7,20,3};
    BuildTree* root = NULL;
    root = constructTree(root, postOrder, inOrder, 4, 4, 0, 0);
    traversal(root);
    
    return 0;
}