import networkx as nx

def create_sample_graph():
    G = nx.Graph()

    # Nodes with content
    G.add_node(1, text="Machine Learning is a subset of Artificial Intelligence.")
    G.add_node(2, text="Deep Learning is a subset of Machine Learning.")
    G.add_node(3, text="Graph Neural Networks operate on graphs.")
    G.add_node(4, text="RAG stands for Retrieval-Augmented Generation.")
    G.add_node(5, text="Graph databases represent data as nodes and edges.")

    # Relationships
    G.add_edges_from([
        (1, 2), (2, 3), (3, 5), (4, 1), (4, 5)
    ])

    return G

def retrieve_relevant_nodes(G, query, top_k=2):
    # Basic retrieval by keyword matching (you can enhance this with embeddings)
    relevant_nodes = []
    for node, data in G.nodes(data=True):
        if query.lower() in data['text'].lower():
            relevant_nodes.append((node, data['text']))
    
    # Return top_k nodes, expand via neighbors if fewer nodes found
    if len(relevant_nodes) < top_k:
        expanded_nodes = []
        for node, _ in relevant_nodes:
            neighbors = list(G.neighbors(node))
            for neighbor in neighbors:
                expanded_nodes.append((neighbor, G.nodes[neighbor]['text']))
        relevant_nodes.extend(expanded_nodes)
    
    return relevant_nodes[:top_k]
