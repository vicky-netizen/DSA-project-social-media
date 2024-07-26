class User:
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

class Edge:
    def __init__(self, start, end):
        self.start = start
        self.end = end

class Graph:
    def __init__(self):
        self.vertices = []
        self.adj_list = {}
        self.edges = []

    def add_node(self, vertex):
        if vertex not in self.vertices:
            self.vertices.append(vertex)
            self.adj_list[vertex] = []

    def remove_node(self, vertex_id):
        for vertex in self.vertices:
            if vertex.user_id == vertex_id:
                self.vertices.remove(vertex)
                del self.adj_list[vertex]
                break  

        for key, edges in self.adj_list.items():
            self.adj_list[key] = [edge for edge in edges if edge.end.user_id != vertex_id]

    def add_edge(self, start, end):
        if start in self.vertices and end in self.vertices:
            new_edge = Edge(start, end)
            self.edges.append(new_edge)
            self.adj_list[start].append(new_edge)

    def remove_edge(self, start_id, end_id):
        for edge in self.edges:
            if edge.start.user_id == start_id and edge.end.user_id == end_id:
                self.edges.remove(edge)
                self.adj_list[edge.start].remove(edge)
                break

    def bfs(self, start_vertex):
        visited = set()
        queue = [start_vertex]
        result = []
        while queue:
            vertex = queue.pop(0)
            if vertex not in visited:
                result.append(vertex)
                visited.add(vertex)
                queue.extend(edge.end for edge in self.adj_list[vertex] if edge.end not in visited)
        return result

    def dfs(self, start_vertex):
        visited = set()
        stack = [start_vertex]
        result = []
        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                result.append(vertex)
                visited.add(vertex)
                stack.extend(edge.end for edge in self.adj_list[vertex] if edge.end not in visited)
        return result
    
    def graph_size(self):
        return len(self.adj_list)

# Example usage:
graph = Graph()
user1 = User("Alice", 1)
user2 = User("Bob", 2)
user3 = User("Charlie", 3)
graph.add_node(user1)
graph.add_node(user2)
graph.add_node(user3)
graph.add_edge(user1, user2)
graph.add_edge(user1, user3)
graph.add_edge(user2, user3)


bfs_result = graph.bfs(user1)
print("BFS traversal:", [user.name for user in bfs_result])


dfs_result = graph.dfs(user1)
print("DFS traversal:", [user.name for user in dfs_result])