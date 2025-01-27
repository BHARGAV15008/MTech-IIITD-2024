#include <iostream>
#include <vector>
using namespace std;

struct WeightedGraphAdjacencyList {
    int weight;
    int node;
    WeightedGraphAdjacencyList* link;
};

class UnionFind {
public:
    UnionFind(int size) {
        parent.resize(size);
        rank.resize(size, 0);
        for (int i = 0; i < size; i++) {
            parent[i] = i;
        }
    }

    int find(int u) {
        if (u != parent[u]) {
            parent[u] = find(parent[u]); // Path compression
        }
        return parent[u];
    }

    void unite(int u, int v) {
        int rootU = find(u);
        int rootV = find(v);
        if (rootU != rootV) {
            if (rank[rootU] > rank[rootV]) {
                parent[rootV] = rootU;
            } else if (rank[rootU] < rank[rootV]) {
                parent[rootU] = rootV;
            } else {
                parent[rootV] = rootU;
                rank[rootU]++;
            }
        }
    }

private:
    vector<int> parent;
    vector<int> rank;
};


WeightedGraphAdjacencyList* createGraphNode(int weight, int node) {
    WeightedGraphAdjacencyList* cGNode = new WeightedGraphAdjacencyList();
    cGNode->weight = weight;
    cGNode->node = node;
    cGNode->link = nullptr;
    return cGNode;
}

void addEdge(WeightedGraphAdjacencyList* graph[], int start, int end, int weight) {
    WeightedGraphAdjacencyList* node = createGraphNode(weight, end);
    node->link = graph[start]->link;
    graph[start]->link = node;
    
    // Add the edge in both directions for an undirected graph
    node = createGraphNode(weight, start);
    node->link = graph[end]->link;
    graph[end]->link = node;
}

vector<pair<int, pair<int, int>>> getEdges(WeightedGraphAdjacencyList* graph[], int noNodes) {
    vector<pair<int, pair<int, int>>> edges;
    for (int i = 0; i < noNodes; i++) {
        WeightedGraphAdjacencyList* temp = graph[i]->link;
        while (temp != nullptr) {
            if (temp->node > i) { // Avoid duplicate edges
                edges.push_back({temp->weight, {i, temp->node}});
            }
            temp = temp->link;
        }
    }
    return edges;
}


void bubbleSort(vector<pair<int, pair<int, int>>>& edges) {
    int n = edges.size();
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (edges[j].first > edges[j + 1].first) {
                swap(edges[j], edges[j + 1]);
            }
        }
    }
}

int kruskalAlgorithm(WeightedGraphAdjacencyList* graph[], int noNodes) {
    vector<pair<int, pair<int, int>>> edges = getEdges(graph, noNodes);
    bubbleSort(edges); // Sort edges by weight

    UnionFind uf(noNodes);
    int mstWeight = 0;

    for (auto& edge : edges) {
        int weight = edge.first;
        int u = edge.second.first;
        int v = edge.second.second;

        if (uf.find(u) != uf.find(v)) {
            uf.unite(u, v);
            mstWeight += weight;
        }
    }

    return mstWeight;
}


int main() {
    int noNodes;
    cout << "Number of vertices: ";
    cin >> noNodes;

    WeightedGraphAdjacencyList* graph[noNodes];
    for (int i = 0; i < noNodes; i++) {
        graph[i] = createGraphNode(0, i);
    }

    cout << "Enter edges (startVertex, endVertex, weight) (Make sure after last edge you enter (-1, -1, -1)): \n";
    int startVertext, endVertex, weight;
    while (cin >> startVertext >> endVertex >> weight) {
        if (startVertext == -1 && endVertex == -1 && weight == -1) break;
        addEdge(graph, startVertext, endVertex, weight);
    }

    int totalWeight = kruskalAlgorithm(graph, noNodes);
    cout << "Total weight of MST: " << totalWeight << endl;

    return 0;
}
