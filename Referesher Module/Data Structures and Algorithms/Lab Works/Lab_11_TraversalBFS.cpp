#include <iostream>
#include <vector>
using namespace std;

int noNodes;

// Define the Queue class
class Queue {
private:
    int size;
    int front;
    int rear;
    vector<int> arr;

public:
    Queue(int size) : size(size), front(-1), rear(-1), arr(size) {}

    bool isFull() const {
        return rear == size - 1;
    }

    bool isEmpty() const {
        return front == rear;
    }

    void enQueue(int val) {
        if (isFull()) {
            cout << "\nQueue is Overflow !!!\n";
        } else {
            arr[++rear] = val;
        }
    }

    int deQueue() {
        if (isEmpty()) {
            cout << "\nQueue is Empty !!!";
            return -1; // Using -1 to indicate empty queue
        } else {
            return arr[++front];
        }
    }
};


void traversalBFS(const vector<vector<int>>& graph, int startVertex) {
    Queue gQueue(noNodes);
    vector<int> visited(noNodes, 0);

    visited[startVertex] = 1;
    gQueue.enQueue(startVertex);

    while (!gQueue.isEmpty()) {
        int node = gQueue.deQueue();
        cout << node << " "; // Output the node

        for (int j = 0; j < noNodes; j++) {
            if (graph[node][j] == 1 && visited[j] == 0) {
                visited[j] = 1;
                gQueue.enQueue(j);
            }
        }
    }
    cout << endl;
}

vector<vector<int>> genAdjacencyMatrix() {
    cout << "Number of vertices: ";
    cin >> noNodes;

    vector<vector<int>> graph(noNodes, vector<int>(noNodes, 0));

    cout << "Enter your edges in format: u v:\n";
    int u, v;
    while (true) {
        cin >> u >> v;
        if (u == -1 && v == -1) break;
        if (u >= 0 && u < noNodes && v >= 0 && v < noNodes) {
            graph[u][v] = 1;
            graph[v][u] = 1; // For undirected graph, also set the reverse edge
        } else {
            cout << "Invalid edge. Please enter again.\n";
        }
    }

    return graph;
}

int main() {

    vector<vector<int>> graph = genAdjacencyMatrix();

    cout << "Adjacency Matrix:\n";
    for (int i = 0; i < noNodes; i++) {
        for (int j = 0; j < noNodes; j++) {
            cout << graph[i][j] << " ";
        }
        cout << endl;
    }

    cout << "BFS traversal starting from vertex 0:\n";
    traversalBFS(graph, 0);

    return 0;
}
