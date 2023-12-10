import random
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib
from collections import deque

matplotlib.use('Agg')

def create_graph(graph_input, alg_type):
    # Destroy the previous canvas and figure if they exist (prevent duplicate canvas)
    if hasattr(create_graph, 'canvas'):
        create_graph.canvas.get_tk_widget().destroy()
        plt.close(create_graph.fig)

    # Parse the entered graph input to create a directed graph
    edges = [tuple(map(int, edge.strip().split('-'))) for edge in graph_input.split(',')]
    G = nx.DiGraph()
    G.add_edges_from(edges)

    # Create a new figure
    create_graph.fig, ax = plt.subplots()

    # Draw the initial graph
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='skyblue',
            node_size=500, edge_color='gray', ax=ax)

    # Create a Tkinter canvas
    create_graph.canvas = FigureCanvasTkAgg(create_graph.fig, master=root)
    create_graph.canvas.draw()
    create_graph.canvas.get_tk_widget().pack()

    # Add a navigation toolbar if it doesn't exist
    if not hasattr(create_graph, 'toolbar'):
        create_graph.toolbar = NavigationToolbar2Tk(create_graph.canvas, root)
        create_graph.toolbar.update()
        create_graph.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Function to update node and edge colors based on BFS algorithmic steps
    def update_bfs_algorithm(frame):
        nonlocal G, pos

        # Perform BFS traversal
        bfs_queue = deque([list(G.nodes)[0]])
        visited = set()

        while bfs_queue:
            current_node = bfs_queue.popleft()
            visited.add(current_node)

            # Set node color for the current node
            node_colors = ['yellow' if node == current_node else 'gray' if node not in visited else 'lightgreen'
                           for node in G.nodes]

            # Set edge color for the visited edges
            edge_colors = ['black' if edge in nx.bfs_edges(G, source=list(G.nodes)[0]) else 'gray' for edge in G.edges]

            # Draw the updated graph
            nx.draw(G, pos, with_labels=True, node_color=node_colors,
                    node_size=500, edge_color=edge_colors, ax=ax)

            create_graph.canvas.draw()
            root.update()

            # Update canvas for animation
            plt.pause(1)

            # Enqueue neighbors of the current node for the next iteration
            bfs_queue.extend(neighbor for neighbor in G.neighbors(current_node) if neighbor not in visited)
    def update_dfs_algorithm(frame):
        nonlocal G, pos

        # Perform DFS traversal
        dfs_stack = [list(G.nodes)[0]]
        visited = set()

        while dfs_stack:
            current_node = dfs_stack.pop()
            visited.add(current_node)

            # Set node color for the current node
            node_colors = ['yellow' if node == current_node else 'gray' if node not in visited else 'lightgreen'
                           for node in G.nodes]

            # Set edge color for the visited edges
            edge_colors = ['black' if edge in nx.dfs_edges(G, source=list(G.nodes)[0]) else 'gray' for edge in G.edges]

            # Draw the updated graph
            nx.draw(G, pos, with_labels=True, node_color=node_colors,
                    node_size=500, edge_color=edge_colors, ax=ax)

            create_graph.canvas.draw()
            root.update()

            # Update canvas for animation
            plt.pause(1)

            # Push neighbors of the current node onto the stack for the next iteration
            dfs_stack.extend(neighbor for neighbor in G.neighbors(current_node) if neighbor not in visited)

    # Update BFS algorithmic steps every second
    if alg_type == 'bfs':
        anim = FuncAnimation(create_graph.fig, update_bfs_algorithm, interval=1000,
                            cache_frame_data=False)
    elif alg_type == 'dfs':
        anim = FuncAnimation(create_graph.fig, update_dfs_algorithm, interval=1000,
                            cache_frame_data=False)

    

    # Start the animation
    anim._start()

# Create the main Tkinter window
root = tk.Tk()
root.title("BFS Algorithm Visualization")

# Set the size of the root window
root.geometry("800x600")

# Entry box for graph input
graph_entry = tk.Entry(root, width=50)
graph_entry.insert(0, "1-2, 1-3, 2-4, 2-5, 3-6, 3-7, 4-8, 4-9")
graph_entry.pack()

# Create a button to visualize BFS algorithm
visualize_bfs_algorithm_button = tk.Button(
    root, text="Visualize BFS Algorithm", command=lambda: create_graph(graph_entry.get(), 'bfs'))
visualize_bfs_algorithm_button.pack()

visualize_dfs_algorithm_button = tk.Button(
    root, text="Visualize DFS Algorithm", command=lambda: create_graph(graph_entry.get(), 'dfs'))
visualize_dfs_algorithm_button.pack()
# Start the Tkinter event loop
root.mainloop()
