#include <iostream>
#include <vector>
#include <queue>
#include <stack>
#include <unordered_map>
#include <unordered_set>
using namespace std;

class TopologicalSort
{
    unordered_map<int, vector<int>> edges;   // Adjacency list
    unordered_map<int, int> inComDeg;        // In-degrees of vertices

public:
    void addEdges(int startVertex, int endVertex)
    {
        edges[startVertex].push_back(endVertex);
        inComDeg[endVertex]++;
        if (inComDeg.find(startVertex) == inComDeg.end())
            inComDeg[startVertex] = 0; // Initialize in-degree of start vertex if not already present
    }

    vector<int> topologicalSortUsingBFS();
    vector<int> topologicalSortUsingDFS();

private:
    void dfs(int vertex, unordered_set<int>& visitedNode, stack<int>& orderStack);
};

vector<int> TopologicalSort::topologicalSortUsingBFS()
{
    vector<int> orderTrack;
    queue<int> trackNode;

    // Enqueue nodes with in-degree 0
    for (const auto& [vertex, degree] : inComDeg)
    {
        if (degree == 0)
        {
            trackNode.push(vertex);
        }
    }

    while (!trackNode.empty())
    {
        int curVertex = trackNode.front();
        trackNode.pop();
        orderTrack.push_back(curVertex);

        // Process all outgoing edges from the current vertex
        for (int neighbor : edges[curVertex])
        {
            inComDeg[neighbor]--;
            if (inComDeg[neighbor] == 0)
            {
                trackNode.push(neighbor);
            }
        }
    }

    return orderTrack;
}

void TopologicalSort::dfs(int vertex, unordered_set<int>& visitedNode, stack<int>& orderStack)
{
    visitedNode.insert(vertex);

    // Visit all adjacent vertices
    for (int neighbor : edges[vertex])
    {
        if (visitedNode.find(neighbor) == visitedNode.end())
        {
            dfs(neighbor, visitedNode, orderStack);
        }
    }

    // Push the current vertex to stack which stores the result
    orderStack.push(vertex);
}

vector<int> TopologicalSort::topologicalSortUsingDFS()
{
    unordered_set<int> visitedNode;
    stack<int> orderStack;
    vector<int> orderTrack;

    // Perform DFS for each unvisited vertex
    for (const auto& [vertex, _] : edges)
    {
        if (visitedNode.find(vertex) == visitedNode.end())
        {
            dfs(vertex, visitedNode, orderStack);
        }
    }

    // Extract vertices from stack to result vector
    while (!orderStack.empty())
    {
        orderTrack.push_back(orderStack.top());
        orderStack.pop();
    }

    return orderTrack;
}

int main()
{
    TopologicalSort tSort;
    int noNodes, startVertex, endVertex;
    cout << "Enter number of vertices: ";
    cin >> noNodes;

    cout << "Enter the edges (at the end add (-1, -1) to finish edges): \n";
    while (true)
    {
        cin >> startVertex >> endVertex;
        if (startVertex == -1 && endVertex == -1)
            break;
        tSort.addEdges(startVertex, endVertex);
    }

    cout << "Topological Sort Using BFS: ";
    vector<int> tSortBFS = tSort.topologicalSortUsingBFS();
    for (int i : tSortBFS)
        cout << i << " ";

    cout << "\nTopological Sort Using DFS: ";
    vector<int> tSortDFS = tSort.topologicalSortUsingDFS();
    for (int i : tSortDFS)
        cout << i << " ";

    return 0;
}