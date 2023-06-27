# Path Finding Visualization

This is a path visualization tool that demonstrates four popular pathfinding algorithms: A*, Dijkstra, Depth-First Search (DFS), and Breadth-First Search (BFS). The tool allows you to create a grid, place obstacles, and find the shortest path between two points using different algorithms.

## Features 
+ Grid-based interface for easy visualization
+ Click and drag to create obstacles
+ Start and end nodes can be placed anywhere on the grid
+ Visual representation of the algorithms' search process
+ Step-by-step animation of the algorithm execution
+ Information about path distance and algorithm running/visualization time

## Algorithms
In this visualizer, the white cells represent walkable areas of the map and black cells represent obstacles. These can be added as wished. 
The neighbours of a node are the nodes directly up, down, left or right of the node. 

### A*
This algorithm identifies the shortest path from the starting node (A) to the end node (B). 
1. The algorithm begins at the starting node. 
2. Calculates $g(n)$, $h(n)$ and $f(n)$ for each neighbour node.   
    + $g(n)$ - distance between the starting node and node n
    + $h(n)$ - heuristic function that estimates the cost of the chepest path between node n and the end node
    + $f(n) = g(n) + h(n)$
3. The algorithm chooses the node with the lowest value of $f(n)$
4. In case of a tie, the algorithm chooses the node closer to the end node. 
5. Repeat the process until you find the end node or there is no more walkable cells. 

### Dijkstra
1. The algorithm begins at the starting node. 
2. Attribute a distance of infinity to all the nodes except the initial one (attribute a distance of 0 to this node)
3. Select the neighbours of this node
4. update their distances with a +1 from the original node
5. consider the current node as visited after considering every neighbour. 
6. Select the neighbour with the lowest value until you find the end node or there is no more walkable cells. 

### Depth-First Search (DFS)
Algorithm to transverse a tree or graph. 
This project implements the iterative version of DFS. 
1. We use a stack to keep tracks of the nodes to visit
2. while teh stack is not empty the last node in it is poped
3. we iterate over the neighbours
4. if the neighbours were not visited, we add them to the stack. 

### Breadth-First Search (BFS)
Algorithm to transverse a tree or graph. It is useful to find the shortest path on a unweighted graph. It differs from DFS because it first explores the nodes close by and only after exploring all of these, moves to the next level.
1. We use a queue to keep track of the nodes to visit.
2. The neighbours of the current node are added to the queue.
3. We visit the next element of the queue and add its neighbours to the queue.
4. We repeat until we find the end or we run out of neighbours to explore.

## Prerequisites
Before running the program, make sure you have the following installed:

Python 3.x: [Download Python](https://www.python.org/downloads/)
Pygame library: Run the following command to install Pygame, version 2.2.0.

```
pip install pygame==2.2.0
```

## Getting Started 
1. Clone the repository or download the source code
2. Navigate to the project directory
3. Run the path_finding.py file
4. Follow the instructions on the app
