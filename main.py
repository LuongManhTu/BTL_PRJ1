import random
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib
from collections import deque
matplotlib.use('Agg')


# Create a graph
G = nx.Graph()
pos = nx.spring_layout(G)


####################     FUNCTIONS     #######################


# Vô hướng, có hướng
def undigraph():
    global G
    G = nx.Graph(G)
    create_graph()


def digraph():
    global G
    G = nx.DiGraph(G)
    create_graph()

# Xử lý add_vertex


def add_vertex():
    v = add_vertex_text.get("1.0", tk.END).strip()
    if v != "":
        global pos
        if len(G.nodes) == 0:
            new_node = int(v)
            pos[new_node] = (0, 0)
            G.add_node(new_node)
        else:
            new_node = int(v)
            G.add_node(new_node)
            if len(G.nodes) > 1:
                fixed_nodes = list(G.nodes())[:-1]
                fixed_positions = [pos[node] for node in fixed_nodes]
                new_node_pos = nx.spring_layout(
                    G, pos=dict(zip(fixed_nodes, fixed_positions)), fixed=fixed_nodes, k=10**-10)
                pos.update(new_node_pos)
        add_vertex_text.delete("1.0", tk.END)
        create_graph()


# Xử lý del_vertex
def remove_vertex():
    v = remove_vertex_text.get("1.0", tk.END).strip()
    if v != "":
        global pos
        node = int(v)
        if G.has_node(node):
            G.remove_node(node)
            if node in pos:
                del pos[node]
            create_graph()
        remove_vertex_text.delete("1.0", tk.END)


# Xử lý add_edge
def add_edge():
    edge = add_edge_text.get("1.0", tk.END).strip()
    if edge:
        nodes = edge.split("-")
        if len(nodes) == 2:
            node1, node2 = nodes
            G.add_edge(int(node1), int(node2))
            global pos
            fixed_nodes = list(G.nodes())[:-1]
            fixed_positions = [pos.get(node, (0, 0)) for node in fixed_nodes]
            fixed_pos = dict(zip(fixed_nodes, fixed_positions))
            pos.update(fixed_pos)
            new_node_pos = nx.spring_layout(
                G, pos=pos, fixed=fixed_nodes, k=10**0)
            pos.update(new_node_pos)
            create_graph()
        add_edge_text.delete("1.0", tk.END)


# Xử lý del_edge
def remove_edge():
    edge = remove_edge_text.get("1.0", tk.END).strip()
    if edge:
        nodes = edge.split("-")
        if len(nodes) == 2:
            node1, node2 = nodes
            if G.has_edge(int(node1), int(node2)):
                G.remove_edge(int(node1), int(node2))
                create_graph()
        remove_edge_text.delete("1.0", tk.END)


# Tạo Graph
def create_graph():

    # Create a new figure
    print(list(G.nodes))

    plt.clf()
    fig = plt.figure()

    # Draw the graph
    nx.draw(G, pos, with_labels=True, node_color='skyblue',
            node_size=500, edge_color='gray', edge_cmap=plt.cm.get_cmap('Blues'), edge_vmin=0, edge_vmax=1, connectionstyle="arc3, rad=0.1")

    # Create a Tkinter frame as a container for the canvas and toolbar
    frame = tk.Frame(root)
    frame.grid(row=0, column=0, sticky=tk.NSEW)

    # Create a Tkinter canvas
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Add a navigation toolbar
    toolbar = NavigationToolbar2Tk(canvas, frame)
    toolbar.update()
    toolbar.pack(side=tk.BOTTOM, fill=tk.BOTH)


# DFS
def DFS():
    global pos  # Update the position variable
    # Create a new figure
    fig = plt.figure()

    # Draw the graph
    nx.draw(G, pos, with_labels=True, node_color='skyblue',
            node_size=500, edge_color='gray', edge_cmap=plt.cm.get_cmap('Blues'), edge_vmin=0, edge_vmax=1,
            connectionstyle="arc3, rad=0.1")

    # Create a Tkinter frame as a container for the canvas and toolbar
    frame = tk.Frame(root)
    frame.grid(row=0, column=0, sticky=tk.NSEW)

    # Create a Tkinter canvas
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Add a navigation toolbar
    toolbar = NavigationToolbar2Tk(canvas, frame)
    toolbar.update()
    toolbar.pack(side=tk.BOTTOM, fill=tk.BOTH)

    # Function to update node and edge colors
    def update_colors(frame):
        for node in G.nodes:
            node_color = random.choice(['red', 'blue', 'green'])
            G.nodes[node]['color'] = node_color
        for edge in G.edges:
            edge_color = random.choice(['red', 'blue', 'green'])
            G.edges[edge]['color'] = edge_color
        nx.draw(G, pos, with_labels=True, node_color=[G.nodes[n]['color'] for n in G.nodes],
                node_size=500, edge_color=[G.edges[e]['color'] for e in G.edges],
                edge_cmap=plt.cm.get_cmap('Blues'), edge_vmin=0, edge_vmax=1,
                connectionstyle="arc3, rad=0.1")  # Add curved edges

    # Update colors every second
    anim = FuncAnimation(fig, update_colors, interval=1000,
                         cache_frame_data=False)

    # Start the animation
    anim._start()

    # Set the edge color in the initial graph drawing
    for edge in G.edges:
        G.edges[edge]['color'] = 'gray'


# BFS
def BFS():

    if not (G.nodes):
        print("No node")

    global pos

    _, ax = plt.subplots()
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
        edge_colors = ['black' if edge in nx.bfs_edges(
            G, source=list(G.nodes)[0]) else 'gray' for edge in G.edges]

        # Draw the updated graph
        nx.draw(G, pos, with_labels=True, node_color=node_colors,
                node_size=500, edge_color=edge_colors, ax=ax)

        create_graph.canvas.draw()
        root.update()

        # Update canvas for animation
        plt.pause(1)

        # Enqueue neighbors of the current node for the next iteration
        bfs_queue.extend(neighbor for neighbor in G.neighbors(
            current_node) if neighbor not in visited)


####################     GUI     #######################


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
    column1_frame, text="Undirected Graph", variable=graph_type_var, value="Graph", command=undigraph)
graph_type_radio1.pack(pady=5)

add_vertex_text = tk.Text(column1_frame, height=1, width=5)
add_vertex_text.pack(pady=5)

add_vertex_button = tk.Button(
    column1_frame, text="Add vertex", command=add_vertex)
add_vertex_button.pack(pady=5)

add_edge_text = tk.Text(column1_frame, height=1, width=5)
add_edge_text.pack(pady=5)

add_edge_button = tk.Button(column1_frame, text="Add edge", command=add_edge)
add_edge_button.pack(pady=5)

# Widgets for column 2
graph_type_radio2 = tk.Radiobutton(
    column2_frame, text="Directed Graph", variable=graph_type_var, value="DiGraph", command=digraph)
graph_type_radio2.pack(pady=5)

remove_vertex_text = tk.Text(column2_frame, height=1, width=5)
remove_vertex_text.pack(pady=5)

remove_vertex_button = tk.Button(
    column2_frame, text="Remove vertex", command=remove_vertex)
remove_vertex_button.pack(pady=5)

remove_edge_text = tk.Text(column2_frame, height=1, width=5)
remove_edge_text.pack(pady=5)

remove_edge_button = tk.Button(
    column2_frame, text="Remove edge", command=remove_edge)
remove_edge_button.pack(pady=5)

# Ô nhập đồ thị
input_text = tk.Text(button_frame, height=15, width=20)
input_text.pack(pady=5)

create_graph_button = tk.Button(
    button_frame, text="Create Graph", command=create_graph)
create_graph_button.pack(pady=10)

run_DFS_button = tk.Button(
    button_frame, text="Run DFS", command=DFS)
run_DFS_button.pack(pady=10)

run_BFS_button = tk.Button(
    button_frame, text="Run BFS", command=BFS)
run_BFS_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
