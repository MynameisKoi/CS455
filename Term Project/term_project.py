class Graph:
    def __init__(self, document, d=0):
        # Tokenize and down-case the words in the document
        self.words = document.lower().split()
        # Initialize empty dictionaries to store node and arc properties
        self.node_properties = {}
        self.arc_properties = {}

        # Calculate counts for nodes and arcs
        self.calculate_counts(d)
        # print(self.node_properties)
        # print(self.arc_properties)

    def calculate_counts(self, d):
        # Calculate counts for nodes
        for word in set(self.words):  # Use set to get unique words
            self.node_properties[word] = {'count': self.words.count(word)}

        # Calculate counts for arcs
        for i in range(len(self.words)):
            for j in range(i + 1, min(i + d + 2, len(self.words))):
                arc = (self.words[i], self.words[j])
                if arc in self.arc_properties:
                    self.arc_properties[arc] = self.arc_properties.get(arc, 0) + 1
                else:
                    self.arc_properties[arc] = 1

    def get_count(self, word):
        if word not in self.node_properties:
            raise ValueError(f"Node '{word}' not found in the graph.")
        return self.node_properties[word].get('count', 0)

    def BFS(self, s, node_count_thresh, arc_count_thresh):
        # Mark all the vertices as not visited
        visited = set()
        # Create a queue for BFS
        queue = []
        # Mark the source node as visited and enqueue it
        visited.add(s)
        queue.append(s)
        while queue:
            # Dequeue a vertex from queue and print it
            s = queue.pop(0)
            # Get all adjacent vertices of the dequeued vertex s. If a adjacent
            # has not been visited, then mark it visited and enqueue it
            for node in self.words:
                if node not in visited and self.get_count(node) >= node_count_thresh and self.arc_properties.get((s, node), 0) >= arc_count_thresh:
                    visited.add(node)
                    queue.append(node)
        return visited

    def get_shortest_path(self, v0):
        # Mark all the vertices as not visited
        visited = set()
        # Create a queue for BFS
        queue = []
        # Mark the source node as visited and enqueue it
        visited.add(v0)
        queue.append(v0)
        # Create a dictionary to store the shortest path
        shortest_path = {}
        shortest_path[v0] = [v0]
        while queue:
            # Dequeue a vertex from queue and print it
            s = queue.pop(0)
            # Get all adjacent vertices of the dequeued vertex s. If a adjacent
            # has not been visited, then mark it visited and enqueue it
            for node in self.words:
                if node not in visited and self.arc_properties.get((s, node), 0) > 0:
                    visited.add(node)
                    queue.append(node)
                    shortest_path[node] = shortest_path[s] + [node]
        return shortest_path



    def find_connected_components(self, node_count_thresh, arc_count_thresh):
        components = []
        visited = set()

        for node in self.words:
            if node not in visited and self.get_count(node) < node_count_thresh:
                component = self.BFS(node, node_count_thresh, arc_count_thresh)
                components.append(component)
                visited.update(component)

        return components


# Read content from the text file
file_path = "d:/VS CODE/Python/CS455/term_project_doc.txt"
with open(file_path, "r", encoding="utf-8") as file:
    document = file.read()

# Step 1: Find suitable node_count_thresh
common_words = ["the", "a", "of", "and", "in", "be", "it"]
graph = Graph(document)
counts = [graph.get_count(word) for word in common_words]
print("Counts of common words:\n\t{}".format("\n\t".join([f"{w}: {c}" for
        w, c in zip(common_words, counts)])))
node_count_thresh = min(counts)  # You can also use average instead of min
print(f"node_count_thresh: {node_count_thresh}")

# Step 2: Create two graphs with d=0 and d=10
d = 0
graph_d = Graph(document, d)
# Find connected components
connected_components = graph_d.find_connected_components(node_count_thresh, arc_count_thresh=6)
# put the result into a text file
with open("d:/VS CODE/Python/CS455/step2_d0.txt", "w", encoding="utf-8") as file:
    for component in connected_components:
        file.write(f"{component}\n")
    file.write(f"Number of connected components: {len(connected_components)}")
    print("Result is saved to 'step2_d0.txt'")

d = 10
graph_d = Graph(document, d)
# Find connected components
connected_components = graph_d.find_connected_components(node_count_thresh, arc_count_thresh=6)
# put the result into a text file
with open("d:/VS CODE/Python/CS455/step2_d10.txt", "w", encoding="utf-8") as file:
    for component in connected_components:
        file.write(f"{component}\n")
    file.write(f"Number of connected components: {len(connected_components)}")
    print("Result is saved to 'step2_d10.txt'")

# Step 3: Repeat step 2 with maximum node_count_thresh and arc_count_thresh
max_node_count_thresh = float('inf')
arc_count_thresh_0 = 0

graph_max_thresh = Graph(document, 0)
# Find connected components
connected_components_max_thresh = graph_max_thresh.find_connected_components(max_node_count_thresh, arc_count_thresh_0)
with open("d:/VS CODE/Python/CS455/step3.txt", "w", encoding="utf-8") as file:
    for component in connected_components_max_thresh:
        file.write(f"{component}\n")
    file.write(f"Number of connected components: {len(connected_components_max_thresh)}")
    print("Result is saved to 'step3.txt'")

# Step 4: BFS and get_shortest_path for small dataset D
dataset_D = [["sport", "rules"], ["european", "charter"], ["swimmers", "squats"], ["sport", "china"], ["ancient", "sports"], ["greeks", "olympic"]]

for pair in dataset_D:
    wi, wi_1 = pair
    graph_d0 = Graph(document, 0)
    # BFS and get_shortest_path
    visited_nodes = graph_d0.BFS(wi, node_count_thresh=float('inf'), arc_count_thresh=0)
    shortest_path = graph_d0.get_shortest_path(wi)
    # if not found shortest_path[wi_1], print as not found
    if wi_1 not in shortest_path:
        print(f"Shortest path from {wi} to {wi_1}: Not found")
    else:
        print(f"Shortest path from {wi} to {wi_1}: {shortest_path[wi_1]}")
