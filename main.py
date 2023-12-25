#need to improve effective
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
    #global canvas  # Declare canvas as a global variable
    # Destroy the previous canvas and figure if they exist
    if hasattr(create_graph, 'canvas'):
        create_graph.canvas.get_tk_widget().destroy()
        plt.close(create_graph.fig)

    # Parse the entered graph input to create a directed graph
    edges = [tuple(map(int, edge.strip().split('-'))) for edge in graph_input.split(',')]
    if graph_type_var.get() != 'Graph':
        G = nx.DiGraph()
    else:
        G = nx.Graph()
    print('###debug' + graph_type_var.get())
    G.add_edges_from(edges)

    # Create a new figure
    create_graph.fig, ax = plt.subplots()

    # Draw the initial graph
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='skyblue',
            node_size=500, edge_color='gray', ax=ax)

    frame = tk.Frame(root)
    frame.grid(row=0, column=0, sticky=tk.NSEW)

    # Create a Tkinter canvas
    canvas = FigureCanvasTkAgg(create_graph.fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Add a navigation toolbar
    toolbar = NavigationToolbar2Tk(canvas, frame)
    toolbar.update()
    toolbar.pack(side=tk.BOTTOM, fill=tk.BOTH)
    # Function to update node and edge colors based on BFS algorithmic steps
    def update_bfs_algorithm(frame):
        nonlocal G, pos  # Add canvas to nonlocal variables

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
                    node_size=500, edge_color=edge_colors, ax=create_graph.fig.axes[0])  # Use the ax attribute directly

            canvas.draw()
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

            canvas.draw()
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
root.title("Graph Visualization")
root.geometry("1000x700")

# Create a button frame on the right side
button_frame = tk.Frame(root)
button_frame.grid(row=0, column=1, padx=50, sticky=tk.NSEW)

# Configure grid weights to make the graph expandable
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

button_frame.columnconfigure(0, weight=1)
button_frame.columnconfigure(1, weight=1)

# Create a new frame within button_frame
columns_frame = tk.Frame(button_frame)
columns_frame.pack()

# Create frames for the two columns
column1_frame = tk.Frame(columns_frame)
column1_frame.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)

column2_frame = tk.Frame(columns_frame)
column2_frame.grid(row=0, column=1, padx=10, pady=10, sticky=tk.NSEW)

# Widgets for column 1

graph_type_var = tk.StringVar(value="Graph")

graph_type_radio1 = tk.Radiobutton(
    column1_frame, text="Undirected", variable=graph_type_var, value="Graph")
graph_type_radio1.pack(pady=5)



# Widgets for column 2
graph_type_radio2 = tk.Radiobutton(
    column2_frame, text="Directed", variable=graph_type_var, value="DiGraph")
graph_type_radio2.pack(pady=5)



# Ô nhập đồ thị
graph_entry = tk.Text(button_frame, height=15, width=20)
graph_entry.insert(tk.END, "1-2, 1-3, 2-4, 2-5, 3-6, 3-7, 4-8, 4-9")

graph_entry.pack(pady=5)

#create_graph_button = tk.Button(
#    button_frame, text="Create Graph", command=create_graph)
#create_graph_button.pack(pady=10)

run_DFS_button = tk.Button(
    button_frame, text="Run DFS", command=lambda: create_graph(graph_entry.get("1.0", "end"), 'dfs'))
run_DFS_button.pack(pady=10)

run_BFS_button = tk.Button(
    button_frame, text="Run BFS", command=lambda: create_graph(graph_entry.get("1.0", "end"), 'bfs'))
run_BFS_button.pack(pady=10)

# Entry box for graph input

# Create a button to visualize BFS algorithm


# Start the Tkinter event loop
root.mainloop()
