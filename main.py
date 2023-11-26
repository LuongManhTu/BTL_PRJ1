import random
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib
matplotlib.use('Agg')


def create_graph():
    # Create a graph
    G = nx.Graph()
    G.add_edges_from([(1, 2), (1, 3), (2, 3), (3, 4),
                     (4, 5), (4, 6), (5, 6), (2, 7)])

    # Create a new figure
    fig = plt.figure()

    # Draw the graph
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='skyblue',
            node_size=500, edge_color='gray')

    # Create a Tkinter canvas
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Add a navigation toolbar
    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Function to update node colors
    def update_colors(frame):
        for node in G.nodes:
            node_color = random.choice(['red', 'blue', 'green'])
            G.nodes[node]['color'] = node_color
        nx.draw(G, pos, with_labels=True, node_color=[G.nodes[n]['color'] for n in G.nodes],
                node_size=500, edge_color='gray')

    # Update colors every second
    anim = FuncAnimation(fig, update_colors, interval=1000,
                         cache_frame_data=False)

    # Set up node click event handling
    def on_node_click(event):
        if event.artist.get_picker() is not None:
            node_index = event.ind[0]
            node = list(G.nodes)[node_index]
            print("Clicked node:", node)

    fig.canvas.mpl_connect('pick_event', on_node_click)

    # Start the animation
    anim._start()


# Create the main Tkinter window
root = tk.Tk()
root.title("Graph Visualization")

# Set the size of the root window
root.geometry("800x600")

# Create a button to draw the graph
create_graph_button = tk.Button(
    root, text="Create Graph", command=create_graph)
create_graph_button.pack()

# Start the Tkinter event loop
root.mainloop()
