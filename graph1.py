import mysql.connector
import heapq

class Graph:
    def __init__(self, vertices):
        self.vertices = vertices
        self.adj_list = {i: [] for i in range(vertices)}
        self.edges = []

    def remove_node(self, vertex):
        self.edges = [x for x in self.edges if vertex not in x]
        self.adj_list[vertex] = []

    def add_edge(self, u, v, weight=1):
        self.adj_list[u].append(v)

        self.edges.append([u, v, weight])

    def remove_edge(self, u, v):
        self.edges = [x for x in self.edges if (u, v) != (x[0], x[1])]

    def bfs(self, start_vertex):
        l = []
        result = []
        visited = set()
        l.append(start_vertex)
        visited.add(start_vertex)
        while len(l) != 0:
            a = l.pop(0)
            result.append(a)
            for x in self.adj_list[a]:
                if x not in visited:
                    visited.add(x)
                    l.append(x)
        return result

    def dfs(self, start_vertex):
        result = []
        visited = set()

        def dept(s):
            if s not in visited:
                visited.add(s)
                result.append(s)
            for x in self.adj_list[s]:
                if x not in visited:
                    dept(x)

        dept(start_vertex)
        return result

    def kruskal(self):
        class UnionFind:
            def __init__(self, n):
                self.parent = list(range(n))
                self.rank = [0] * n

            def find(self, u):
                if self.parent[u] != u:
                    self.parent[u] = self.find(self.parent[u])
                return self.parent[u]

            def union(self, u, v):
                root_u = self.find(u)
                root_v = self.find(v)
                if root_u != root_v:
                    if self.rank[root_u] < self.rank[root_v]:
                        self.parent[root_u] = root_v
                    elif self.rank[root_u] > self.rank[root_v]:
                        self.parent[root_v] = root_u
                    else:
                        self.parent[root_v] = root_u
                        self.rank[root_u] += 1
                return root_u != root_v

        self.edges.sort(key=lambda x: x[2])
        uf = UnionFind(self.vertices)
        mst = []
        mst_cost = 0
        for edge in self.edges:
            u, v, w = edge
            if uf.union(u, v):
                mst.append(edge)
                mst_cost += w
        return mst

    def prim(self):
        if self.vertices == 0:
            return []
        mst = []
        mst_cost = 0
        min_heap = []
        visited = set()
        start_vertex = 0
        for v in self.adj_list[start_vertex]:
            heapq.heappush(min_heap, (1, start_vertex, v))
        visited.add(start_vertex)
        while min_heap and len(visited) < self.vertices:
            weight, u, v = heapq.heappop(min_heap)
            if v not in visited:
                visited.add(v)
                mst.append([u, v, weight])
                mst_cost += weight
                for neighbor in self.adj_list[v]:
                    if neighbor not in visited:
                        heapq.heappush(min_heap, (1, v, neighbor))
        return mst

    def dijkstra(self, start_vertex):
        distances = {i: float('inf') for i in range(self.vertices)}
        distances[start_vertex] = 0
        min_heap = [(0, start_vertex)]
        while min_heap:
            current_distance, current_vertex = heapq.heappop(min_heap)
            if current_distance > distances[current_vertex]:
                continue
            for neighbor in self.adj_list[current_vertex]:
                new_distance = current_distance + 1  # Adjust for specific edge weights
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    heapq.heappush(min_heap, (new_distance, neighbor))
        return distances

    def graph_size(self):
        pass

    def get_neighbors(self, vertex):
        if vertex in self.adj_list:
            return self.adj_list[vertex]
        else:
            return []

    def print_graph(self):
        for vertex, neighbors in self.adj_list.items():
            print(f"Vertex {vertex}: {neighbors}")
        print(f"Edges: {self.edges}")



def construct_graph_from_mysql(cursor):
    graph = Graph(20)  # Initialize an empty graph
    cursor.execute("SELECT friend_id, follower_id FROM friendfollower")
    for row in cursor.fetchall():
        friend, follower = row

        graph.add_edge(friend, follower)  # Assuming friend and follower are vertex IDs
    return graph

def testGraph():

    conn = mysql.connector.connect(host='localhost',user='root',password='vicky310105',database='vicky')
    if conn is None:
        return
    
    cursor = conn.cursor()

    graph = construct_graph_from_mysql(cursor)

    while True:
        command = input().strip()
        if command == "End":
            break
        operation = command.split()
        cmd_type = operation[0]

        if cmd_type == "AddEdge":
            u, v, w = int(operation[1]), int(operation[2]), int(operation[3])
            graph.add_edge(u, v, w)
            print(f"Edge added between {u} and {v} with weight {w}")
        
        elif cmd_type == "RemoveEdge":
            u, v = int(operation[1]), int(operation[2])
            graph.remove_edge(u, v)
            print(f"Edge removed between {u} and {v}")

        elif cmd_type == "RemoveNode":
            vertex = int(operation[1])
            graph.remove_node(vertex)
            print(f"Node {vertex} removed")

        elif cmd_type == "BFS":
            start_vertex = int(operation[1])
            result = graph.bfs(start_vertex)
            print(f"BFS from vertex {start_vertex}: {result}")

        elif cmd_type == "DFS":
            start_vertex = int(operation[1])
            result = graph.dfs(start_vertex)
            print(f"DFS from vertex {start_vertex}: {result}")

        elif cmd_type == "MST":
            algo = operation[1]
            if algo == "Kruskal":
                result = graph.kruskal()
                print(f"MST (Kruskal's): {result}")
            elif algo == "Prim":
                result = graph.prim()
                print(f"MST (Prim's): {result}")

        elif cmd_type == "ShortestPath":
            start_vertex = int(operation[1])
            result = graph.dijkstra(start_vertex)
            print(f"Shortest paths from vertex {start_vertex}: {result}")
            
                
        elif cmd_type == "Print":
            graph.print_graph()
    cursor.close()
    conn.close()

def main():
    testGraph()

if __name__ == "__main__":
    main()
