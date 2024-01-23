import random
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib
from collections import deque
matplotlib.use('Agg')


G = nx.Graph()
pos = None # Store nodes' positions
undirected = 1 # graph type: undirected
running = 0 # running == 1 -> a BFS or DFS animation is running -> no interuption
anim = None
windowSize = "1280x770"
animTimeStep = 2500 # animation time step


####################     FUNCTIONS     #######################


# Switch to undirected graph
def undigraph():
    global undirected
    undirected = 1

    global G
    DG = nx.Graph()
    DG.add_nodes_from(G.nodes)
    DG.add_edges_from(G.edges)
    G = DG

    output_text.delete('1.0', tk.END)

    # Clear plot
    plt.clf()
    fig = plt.figure()
    # Draw the graph
    nx.draw(G, pos, with_labels=True, node_color='skyblue',
            node_size=500, edge_color='lightgray', edge_cmap=plt.cm.get_cmap('Blues'), edge_vmin=0, edge_vmax=1, connectionstyle="arc3, rad=0.1")
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


# Switch to directed graph
def digraph():
    global undirected
    undirected = 0

    global G
    DG = nx.DiGraph()
    DG.add_nodes_from(G.nodes)
    # get list edges from input_text
    content = input_text.get("1.0", "end-1c")
    lines = content.split("\n")
    lines = lines[1:]
    edges = [tuple(map(int, line.strip().split())) for line in lines]
    DG.add_edges_from(edges)
    G = DG

    output_text.delete('1.0', tk.END)

    plt.clf()
    fig = plt.figure()
    # Draw the graph
    nx.draw(G, pos, with_labels=True, node_color='skyblue',
            node_size=500, edge_color='lightgray', edge_cmap=plt.cm.get_cmap('Blues'), edge_vmin=0, edge_vmax=1, connectionstyle="arc3, rad=0.1")
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


# Update num_vertext, num_edge in input_text
def replace_first_line():
    content = input_text.get("1.0", "end-1c")
    lines = content.split("\n")
    lines[0] = str(len(G.nodes)) + " " + str(len(G.edges))
    new_content = "\n".join(lines)
    input_text.delete("1.0", tk.END)
    input_text.insert(tk.END, new_content)


def add_vertex():
    v = add_vertex_text.get("1.0", tk.END).strip()
    if v != "":
        output_text.delete('1.0', tk.END)
        global pos
        # First node of G
        if len(G.nodes) == 0:
            new_node = int(v)
            pos = nx.spring_layout(G)
            # Asign position (0, 0) to new_node
            pos[new_node] = (0, 0)
            G.add_node(new_node)
        else:
            new_node = int(v)
            if not G.has_node(new_node):
                G.add_node(new_node)
                if len(G.nodes) > 1:
                    fixed_nodes = list(G.nodes())[:-1]
                    fixed_positions = [pos[node] for node in fixed_nodes]
                    new_node_pos = nx.spring_layout(
                        G, pos=dict(zip(fixed_nodes, fixed_positions)), fixed=fixed_nodes, k=10**-10)
                    pos.update(new_node_pos)
            else:
                messagebox.showinfo("Alert", "Vertex existed!")

        add_vertex_text.delete("1.0", tk.END)
        replace_first_line()

        # if input_text is not blank, only update the figure; else create a new graph
        if input_text.get("1.0", "end").strip() != '':
            plt.clf()
            fig = plt.figure()
            # Draw the graph
            nx.draw(G, pos, with_labels=True, node_color='skyblue',
                    node_size=500, edge_color='lightgray', edge_cmap=plt.cm.get_cmap('Blues'), edge_vmin=0, edge_vmax=1, connectionstyle="arc3, rad=0.1")
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
        else:
            create_graph()


def remove_vertex():
    v = remove_vertex_text.get("1.0", tk.END).strip()
    if v != "":
        output_text.delete('1.0', tk.END)
        global pos
        node = int(v)
        if G.has_node(node):
            G.remove_node(node)
            # Delete lines in input_text containing this node
            lines_to_delete = []
            line_number = 1
            current_line = input_text.get(
                f"{line_number}.0", f"{line_number}.end")
            while current_line:
                if line_number != 1 and str(node) in current_line:
                    lines_to_delete.append(line_number)
                line_number += 1
                current_line = input_text.get(
                    f"{line_number}.0", f"{line_number}.end")
            for line_num in reversed(lines_to_delete):
                input_text.delete(f"{line_num}.0", f"{line_num+1}.0")

            replace_first_line()

            plt.clf()
            fig = plt.figure()
            # Draw the graph
            nx.draw(G, pos, with_labels=True, node_color='skyblue',
                    node_size=500, edge_color='lightgray', edge_cmap=plt.cm.get_cmap('Blues'), edge_vmin=0, edge_vmax=1, connectionstyle="arc3, rad=0.1")
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
        else:
            messagebox.showinfo("Alert", "Vertex does not exist!")
    remove_vertex_text.delete("1.0", tk.END)


def add_edge():
    edge = add_edge_text.get("1.0", tk.END).strip()
    if edge:
        output_text.delete('1.0', tk.END)
        nodes = edge.split(" ")
        if len(nodes) == 2:
            node1, node2 = nodes
            if not G.has_edge(int(node1), int(node2)):
                global pos
                if len(G.nodes) == 0:
                    pos = nx.spring_layout(G)
                    pos[int(node1)] = (0, 0)
                G.add_edge(int(node1), int(node2))
                # Keep the nodes' positions
                fixed_nodes = list(G.nodes())[:-1]
                fixed_positions = [pos.get(node, (0, 0))
                                   for node in fixed_nodes]
                fixed_pos = dict(zip(fixed_nodes, fixed_positions))
                pos.update(fixed_pos)

                if int(node1) not in pos:
                    rand1 = random.choice([-2, -1, 1, 2])
                    rand2 = random.choice([-2, -1, 1, 2])
                    # Asign random position for node1 if not existed
                    pos[int(node1)] = (fixed_positions[-1]
                                       [0] + rand1, fixed_positions[-1][1] + rand2)
                if int(node2) not in pos:
                    rand1 = random.choice([-2, -1, 1, 2])
                    rand2 = random.choice([-2, -1, 1, 2])
                    # Asign random position for node2 if not existed
                    pos[int(node2)] = (fixed_positions[-1]
                                       [0] + rand1, fixed_positions[-1][1] + rand2)

                # Add new line to input_text
                new_line = f"\n{node1} {node2}"
                lines = input_text.get("1.0", "end-1c")
                if new_line not in lines:
                    input_text.insert(tk.END, new_line)

                add_edge_text.delete("1.0", tk.END)
                replace_first_line()

                plt.clf()
                fig = plt.figure()
                # Draw the graph
                nx.draw(G, pos, with_labels=True, node_color='skyblue',
                        node_size=500, edge_color='lightgray', edge_cmap=plt.cm.get_cmap('Blues'), edge_vmin=0, edge_vmax=1, connectionstyle="arc3, rad=0.1")
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
            else:
                messagebox.showinfo("Alert", "Edge existed!")
        else:
            messagebox.showinfo("Alert", "Wront input format!")
    add_edge_text.delete("1.0", tk.END)


def remove_edge():
    edge = remove_edge_text.get("1.0", tk.END).strip()
    if edge:
        output_text.delete('1.0', tk.END)
        nodes = edge.strip().split(" ")
        print(len(nodes))
        if len(nodes) == 2:
            node1, node2 = nodes
            if G.has_edge(int(node1), int(node2)):
                G.remove_edge(int(node1), int(node2))
                # Delete line in input_text containing this edge
                lines_to_delete = []
                line_number = 1
                current_line = input_text.get(
                    f"{line_number}.0", f"{line_number}.end")
                while current_line:
                    if edge in current_line:
                        lines_to_delete.append(line_number)
                    line_number += 1
                    current_line = input_text.get(
                        f"{line_number}.0", f"{line_number}.end")
                for line_num in reversed(lines_to_delete):
                    input_text.delete(f"{line_num}.0", f"{line_num+1}.0")

                replace_first_line()

                plt.clf()
                fig = plt.figure()
                # Draw the graph
                nx.draw(G, pos, with_labels=True, node_color='skyblue',
                        node_size=500, edge_color='lightgray', edge_cmap=plt.cm.get_cmap('Blues'), edge_vmin=0, edge_vmax=1, connectionstyle="arc3, rad=0.1")
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
            else:
                messagebox.showinfo("Alert", "Edge does not exist!")
        else:
            messagebox.showinfo("Alert", "Wrong input format!")
        remove_edge_text.delete("1.0", tk.END)


# Import graph from .txt file
def import_graph():
    file_path = filedialog.askopenfilename()
    if file_path:
        if len(G.nodes):
            global pos
            pos = None
            G.clear()
        with open(file_path, 'r') as file:
            content = file.read()
        input_text.delete('1.0', tk.END)
        input_text.insert(tk.END, content)


def create_graph():
    global G
    output_text.delete('1.0', tk.END)
    # If input_text is not blank, read and create graph from it
    if input_text.get("1.0", "end").strip() != '':
        if undirected == 1:
            G = nx.Graph()
        else:
            G = nx.DiGraph()
        data = input_text.get("1.0", "end")
        lines = data.strip().split("\n")
        for line in lines[1:]:
            u, v = map(int, line.split(" "))
            G.add_node(u)
            G.add_node(v)
            G.add_edge(u, v)
        global pos
        if not pos:    
            pos = nx.spring_layout(G)
    if len(G.nodes):
        plt.clf()
        fig = plt.figure()
        # Draw the graph
        nx.draw(G, pos, with_labels=True, node_color='skyblue',
                node_size=500, edge_color='lightgray', edge_cmap=plt.cm.get_cmap('Blues'), edge_vmin=0, edge_vmax=1, connectionstyle="arc3, rad=0.1")
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
    else:
        messagebox.showinfo("Alert", "Blank Graph!")
    
    
def delete_graph():
    global G, pos
    if len(G.nodes):
        pos = None
        G.clear()
        plt.clf()
        fig = plt.figure()
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
        
        input_text.delete('1.0', tk.END)
        output_text.delete('1.0', tk.END)
    else:
        messagebox.showinfo("Alert", "Blank Graph!")


def BFS():
    global pos, anim, running
    
    if len(G.nodes):
        sorted_nodes = sorted(G.nodes)
        start_index = sorted_nodes[0]
        end_index = sorted_nodes[len(sorted_nodes)-1]

        # if not input start_node, set start_node = start_index as default
        if starting_vertex_text.get("1.0", "end").strip() != '':
            if G.has_node(int(starting_vertex_text.get("1.0", "end").strip())):
                start_node = int(starting_vertex_text.get("1.0", "end").strip())
            else:
                messagebox.showinfo("Alert", "Start vertex does not exist!")
                starting_vertex_text.delete('1.0', tk.END)
                return
        else:
            start_node = start_index
            starting_vertex_text.insert(tk.END, start_index)
        if target_vertex_text.get("1.0", "end").strip() != '':
            if G.has_node(int(target_vertex_text.get("1.0", "end").strip())):
                target_node = int(target_vertex_text.get("1.0", "end").strip())
            else:
                messagebox.showinfo("Alert", "Target vertex does not exist!")
                target_vertex_text.delete('1.0', tk.END)
                return

        if not running:
            # BFS queue
            bfs_queue = deque()
            visited = set()
            running = 1

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

            # add start_node to queue
            bfs_queue.append(start_node)
            # Used to trace back path from target_node
            previous = {start_node: None}

            output_text.delete('1.0', tk.END)
            output_text.insert(tk.END, "--- Started BFS Traversal:\n")
            output_text.insert(
                tk.END, "    Initial queue: [" + str(start_node) + "]\n")
            trace = []
            
            if target_vertex_text.get("1.0", "end").strip() != '' and start_node == target_node:

                # BFS traversal completed
                line = "    Current node: " + \
                                    str(start_node) + " - Queue: []\n"
                output_text.insert(tk.END, line)
                output_text.insert(tk.END, "--- BFS traversal completed!\n")
                tracee = "- Visit order: " + str(start_node)

                output_text.insert(tk.END, tracee + "\n")
                running = 0
                
                nx.draw(G, pos, with_labels=True, node_color='skyblue',
                        node_size=500, edge_color='lightgray', edge_cmap=plt.cm.get_cmap('Blues'), edge_vmin=0, edge_vmax=1, connectionstyle="arc3, rad=0.1")

                return

            # Check if all neighbors are visited
            def visitedAllNeighbor(node):
                for neighbor in G.neighbors(node):
                    if neighbor not in visited:
                        return 0
                return 1

            # Run BFS
            def animateBFS(frame, canvas, animation):

                global running
                
                if bfs_queue:
                    
                    starting_vertex_text.config(state="disabled")
                    target_vertex_text.config(state="disabled")
                    

                    current_node = bfs_queue.popleft()
                    visited.add(current_node)
                    trace.append(current_node)
                    

                    # Set nodes' color
                    node_colors = ['yellow' if node == current_node 
                                else 'lightgreen' if (node in G.neighbors(current_node) and node not in visited and node not in bfs_queue) 
                                else 'lightgreen' if node in bfs_queue
                                else 'gray' if node in visited 
                                else 'skyblue' for node in G.nodes]
                    
                    node_edge_colors = ['black' if node == current_node
                                else 'lightgreen' if (node in G.neighbors(current_node) and node not in visited and node not in bfs_queue)
                                        else 'lightgreen' if node in bfs_queue
                                else 'gray' if node in visited
                                else 'skyblue' for node in G.nodes]

                    edge_colors = ['lightgray' for _ in G.edges]

                    # Clear the previous figure
                    plt.clf()

                    nx.draw(G, pos, with_labels=True, node_color=node_colors,
                            node_size=500, edge_color=edge_colors, edge_cmap=plt.cm.get_cmap('Blues'), edge_vmin=0,
                            edge_vmax=1, connectionstyle="arc3, rad=0.1", edgecolors=node_edge_colors)

                    # Update canvas for animation
                    canvas.draw()
                    root.update()

                    # if input target_node --> stop when current_node == target_node
                    if target_vertex_text.get("1.0", "end").strip() != '':
                        if current_node != target_node:
                            # global running
                            # if target_node cant be reach from current_node
                            if len(bfs_queue) == 0 and target_node not in visited and visitedAllNeighbor(current_node):
                                line = "    Current node: " + \
                                    str(current_node) + " - Queue: []\n"
                                output_text.insert(tk.END, line)
                                output_text.insert(
                                    tk.END, "--- Could not reach target node (" + str(target_node) + ")!\n")
                                anim.event_source.stop()  # Stop the animation
                                running = 0
                            else:
                                line = "    Current node: " + \
                                    str(current_node) + " - "
                                output_text.insert(tk.END, line)

                                # Enqueue neighbors of the current node for the next iteration
                                neighbors = sorted(list(G.neighbors(current_node)))
                                for neighbor in neighbors:
                                    if neighbor not in visited and neighbor not in bfs_queue:
                                        bfs_queue.append(neighbor)
                                        previous[neighbor] = current_node

                                queue = ""
                                for i in range(len(bfs_queue)-1):
                                    queue += str(bfs_queue[i]) + ","
                                queue += str(bfs_queue[len(bfs_queue)-1])
                                line = "Queue: [" + queue + "]\n"
                                output_text.insert(tk.END, line)
                        # reached target_node
                        else:
                            if starting_vertex_text.get("1.0", "end").strip() == "" and target_vertex_text.get("1.0", "end").strip() == "":
                                line = "    Current node: " + \
                                    str(current_node) + " - Queue: []\n"
                                output_text.insert(tk.END, line)
                            else:
                                line = "    Current node: " + \
                                    str(current_node) + "\n"
                                output_text.insert(tk.END, line)

                            output_text.insert(
                                tk.END, "--- BFS traversal completed!\n")
                            tracee = "- Visit order: "
                            for i in range(len(trace)-1):
                                tracee += str(trace[i]) + "->"
                            tracee += str(trace[len(trace)-1])
                            output_text.insert(tk.END, tracee + "\n")

                            path = []
                            current = target_node
                            while current is not None:
                                path.append(current)
                                current = previous[current]
                            path.reverse()

                            pathh = ""
                            for i in range(len(path)-1):
                                pathh += str(path[i]) + "->"
                            pathh += str(path[len(path)-1])
                            output_text.insert(
                                tk.END, "- Shortest path from start vertex (" + str(start_node) + ") to target vertex (" + str(target_node) + "): " + pathh)
                            
                            starting_vertex_text.config(state="normal")
                            target_vertex_text.config(state="normal")

                            anim.event_source.stop()  # Stop the animation
                            running = 0
                    # if not input target_node --> BFS traversy from start_node
                    else:
                        line = "    Current node: " + str(current_node) + " - "
                        output_text.insert(tk.END, line)

                        # Enqueue neighbors of the current node for the next iteration
                        neighbors = sorted(list(G.neighbors(current_node)))
                        for neighbor in neighbors:
                            if neighbor not in visited and neighbor not in bfs_queue:
                                bfs_queue.append(neighbor)
                                previous[neighbor] = current_node
                        queue = ""
                        for i in range(len(bfs_queue)-1):
                            queue += str(bfs_queue[i]) + ","
                        if len(bfs_queue) == 0:
                            queue = ""
                        else:
                            queue += str(bfs_queue[len(bfs_queue)-1])
                        line = "Queue: [" + queue + "]\n"
                        output_text.insert(tk.END, line)
                else:
                    # BFS traversal completed
                    output_text.insert(tk.END, "--- BFS traversal completed!\n")
                    tracee = "- Visit order: "
                    for i in range(len(trace)-1):
                        tracee += str(trace[i]) + "->"
                    tracee += str(trace[len(trace)-1])
                    output_text.insert(tk.END, tracee + "\n")
                    
                    starting_vertex_text.config(state="normal")
                    target_vertex_text.config(state="normal")
                    
                    anim.event_source.stop()  # Stop the animation
                    running = 0

            # Loop every 1.5 seconds to change animation
            anim = FuncAnimation(fig, animateBFS, fargs=(
                canvas, anim), interval=animTimeStep, cache_frame_data=False)

            # Start the animation
            anim._start()
    else:
        messagebox.showinfo("Alert", "Blank Graph!")


def DFS():
    global pos, anim, running

    if len(G.nodes):    
        sorted_nodes = sorted(G.nodes)
        start_index = sorted_nodes[0]
        end_index = sorted_nodes[len(sorted_nodes)-1]

        # if not input start_node, set start_node = start_index as default
        if starting_vertex_text.get("1.0", "end").strip() != '':
            if G.has_node(int(starting_vertex_text.get("1.0", "end").strip())):
                start_node = int(
                    starting_vertex_text.get("1.0", "end").strip())
            else:
                messagebox.showinfo("Alert", "Start vertex does not exist!")
                starting_vertex_text.delete('1.0', tk.END)
                return
        else:
            start_node = start_index
            starting_vertex_text.insert(tk.END, start_index)
        if target_vertex_text.get("1.0", "end").strip() != '':
            if G.has_node(int(target_vertex_text.get("1.0", "end").strip())):
                target_node = int(target_vertex_text.get("1.0", "end").strip())
            else:
                messagebox.showinfo("Alert", "Target vertex does not exist!")
                target_vertex_text.delete('1.0', tk.END)
                return

        # if no BFS or DFS traversy is running
        if not running:
            # DFS stack
            dfs_stack = []
            visited = set()
            running = 1

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

            # Perform DFS traversal
            dfs_stack.append(start_node)

            output_text.delete('1.0', tk.END)
            output_text.insert(tk.END, "--- Started DFS Traversal:\n")
            output_text.insert(
                tk.END, "    Initial stack: [" + str(start_node) + "]\n")
            trace = []
            
            if target_vertex_text.get("1.0", "end").strip() != '' and start_node == target_node:

                # BFS traversal completed
                line = "    Current node: " + \
                    str(start_node) + " - Stack: []\n"
                output_text.insert(tk.END, line)
                output_text.insert(tk.END, "--- DFS traversal completed!\n")
                tracee = "- Visit order: " + str(start_node)

                output_text.insert(tk.END, tracee + "\n")
                running = 0
                
                nx.draw(G, pos, with_labels=True, node_color='skyblue',
                        node_size=500, edge_color='lightgray', edge_cmap=plt.cm.get_cmap('Blues'), edge_vmin=0, edge_vmax=1, connectionstyle="arc3, rad=0.1")

                return

            # Check if all neighbors are visited
            def visitedAllNeighbor(node):
                for neighbor in G.neighbors(node):
                    if neighbor not in visited:
                        return 0
                return 1

            # Run DFS
            def animateDFS(frame, canvas, animation):

                # while stack is not empty
                if dfs_stack:
                    
                    starting_vertex_text.config(state="disabled")
                    target_vertex_text.config(state="disabled")

                    current_node = dfs_stack.pop()
                    visited.add(current_node)
                    trace.append(current_node)

                    # Set nodes' color
                    node_colors = ['yellow' if node == current_node
                                else 'lightgreen' if (node in G.neighbors(current_node) and node not in visited and node not in dfs_stack)
                                else 'lightgreen' if node in dfs_stack
                                else 'gray' if node in visited
                                else 'skyblue' for node in G.nodes]

                    node_edge_colors = ['black' if node == current_node
                                        else 'lightgreen' if (node in G.neighbors(current_node) and node not in visited and node not in dfs_stack)
                                        else 'lightgreen' if node in dfs_stack
                                        else 'gray' if node in visited
                                        else 'skyblue' for node in G.nodes]

                    edge_colors = ['lightgray' for _ in G.edges]

                    # Clear the previous figure
                    plt.clf()

                    nx.draw(G, pos, with_labels=True, node_color=node_colors,
                            node_size=500, edge_color=edge_colors, edge_cmap=plt.cm.get_cmap('Blues'), edge_vmin=0,
                            edge_vmax=1, connectionstyle="arc3, rad=0.1", edgecolors=node_edge_colors)

                    # Update canvas for animation
                    canvas.draw()
                    root.update()

                    # if input target_node --> stop when current_node == target_node
                    if target_vertex_text.get("1.0", "end").strip() != '':
                        if current_node != target_node:
                            global running
                            # if target_node cant be reach from current_node
                            if len(dfs_stack) == 0 and target_node not in visited and visitedAllNeighbor(current_node):
                                line = "    Current node: " + \
                                    str(current_node) + " - Stack: []\n"
                                output_text.insert(tk.END, line)
                                output_text.insert(
                                    tk.END, "--- Could not reach target node (" + str(target_node) + ")!\n")
                                anim.event_source.stop()  # Stop the animation
                                running = 0
                            else:
                                line = "    Current node: " + \
                                    str(current_node) + " - "
                                output_text.insert(tk.END, line)

                                # Enqueue neighbors of the current node for the next iteration
                                neighbors = sorted(list(G.neighbors(current_node)))
                                neighbors.reverse()
                                for neighbor in neighbors:
                                    if neighbor not in visited and neighbor not in dfs_stack:
                                        dfs_stack.append(neighbor)
                                stack = ""
                                for i in range(len(dfs_stack)-1):
                                    stack += str(dfs_stack[i]) + ","
                                stack += str(dfs_stack[len(dfs_stack)-1])
                                line = "Stack: [" + stack + "]\n"
                                output_text.insert(tk.END, line)
                        # reached target_node
                        else:
                            if starting_vertex_text.get("1.0", "end").strip() == "" and target_vertex_text.get("1.0", "end").strip() == "":
                                line = "    Current node: " + \
                                    str(current_node) + " - Stack: []\n"
                                output_text.insert(tk.END, line)
                            else:
                                line = "    Current node: " + \
                                    str(current_node) + "\n"
                                output_text.insert(tk.END, line)

                            output_text.insert(
                                tk.END, "--- DFS traversal completed!\n")
                            tracee = "- Visit order: "
                            for i in range(len(trace)-1):
                                tracee += str(trace[i]) + "->"
                            tracee += str(trace[len(trace)-1])
                            output_text.insert(tk.END, tracee + "\n")

                            pathDFS = []
                            traceRe = trace.copy()
                            traceRe.reverse()
                            pathDFS.append(traceRe[0])
                            
                            i = 0
                            if undirected:
                                while i < len(traceRe) - 1:
                                    if traceRe[i+1] in G.neighbors(traceRe[i]):
                                        pathDFS.append(traceRe[i+1])
                                        i += 1
                                    else:
                                        del traceRe[i+1]
                            else:
                                while i < len(traceRe) - 1:
                                    if traceRe[i] in G.successors(traceRe[i+1]):
                                        pathDFS.append(traceRe[i+1])
                                        i += 1
                                    else:
                                        del traceRe[i+1]
                            pathDFS.reverse()
                            pathh = ""
                            for i in range(len(pathDFS)-1):
                                pathh += str(pathDFS[i]) + "->"
                            pathh += str(pathDFS[len(pathDFS)-1])
                            output_text.insert(
                                tk.END, "- Path from start vertex (" + str(start_node) + ") to target vertex (" + str(target_node) + "): " + pathh)
                            
                            starting_vertex_text.config(state="normal")
                            target_vertex_text.config(state="normal")

                            anim.event_source.stop()  # Stop the animation
                            running = 0
                    # if not input target_node --> DFS traversy from start_node
                    else:
                        line = "    Current node: " + str(current_node) + " - "
                        output_text.insert(tk.END, line)

                        # Enqueue neighbors of the current node for the next iteration
                        neighbors = sorted(list(G.neighbors(current_node)))
                        neighbors.reverse()
                        for neighbor in neighbors:
                            if neighbor not in visited and neighbor not in dfs_stack:
                                dfs_stack.append(neighbor)
                        stack = ""
                        for i in range(len(dfs_stack)-1):
                            stack += str(dfs_stack[i]) + ","
                        if len(dfs_stack) == 0:
                            stack = ""
                        else:
                            stack += str(dfs_stack[len(dfs_stack)-1])
                        line = "Stack: [" + stack + "]\n"
                        output_text.insert(tk.END, line)
                # just in case start_node == target_node
                else:
                    # DFS traversal completed
                    output_text.insert(tk.END, "--- DFS traversal completed!\n")
                    tracee = "- Visit order: "
                    for i in range(len(trace)-1):
                        tracee += str(trace[i]) + "->"
                    tracee += str(trace[len(trace)-1])
                    output_text.insert(tk.END, tracee + "\n")
                    
                    starting_vertex_text.config(state="normal")
                    target_vertex_text.config(state="normal")

                    anim.event_source.stop()  # Stop the animation
                    running = 0

            # Loop every 1.5 seconds to change animation
            anim = FuncAnimation(fig, animateDFS, fargs=(
                canvas, anim), interval=animTimeStep, cache_frame_data=False)

            # Start the animation
            anim._start()
    else:
        messagebox.showinfo("Alert", "Blank Graph!")
        

####################     WIDGETS     #######################


# Create the main Tkinter window
root = tk.Tk()
root.title("Graph Visualization")
# root.attributes('-fullscreen', True)
root.geometry(windowSize)

# Create a button frame on the right side
button_frame = tk.Frame(root)
button_frame.grid(row=0, column=1, padx=30, sticky=tk.NSEW)

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
def disable_editing(event):
    return "break"
input_text = tk.Text(button_frame, height=10, width=20)
input_text.bind("<Key>", disable_editing)
input_text.pack(pady=5)

import_graph_button = tk.Button(
    button_frame, text="Import Graph", command=import_graph)
import_graph_button.pack(pady=10)

create_graph_button = tk.Button(
    button_frame, text="Create Graph", command=create_graph)
create_graph_button.pack(pady=10)

delete_graph_button = tk.Button(
    button_frame, text="Delete Graph", command=delete_graph)
delete_graph_button.pack(pady=10)

# Create a frame for the starting vertex label and text
starting_vertex_frame = tk.Frame(button_frame)
starting_vertex_frame.pack(pady=5)

# Add the label and text widget
starting_vertex_label = tk.Label(
    starting_vertex_frame, text="Start vertex:")
starting_vertex_label.pack(side=tk.LEFT, padx=5)

starting_vertex_text = tk.Text(starting_vertex_frame, height=1, width=5)
starting_vertex_text.pack(side=tk.LEFT, padx=5)

# Create a frame for the starting vertex label and text
target_vertex_frame = tk.Frame(button_frame)
target_vertex_frame.pack(pady=5)

# Add the label and text widget
target_vertex_label = tk.Label(
    target_vertex_frame, text="Target vertex:")
target_vertex_label.pack(side=tk.LEFT, padx=5)

target_vertex_text = tk.Text(target_vertex_frame, height=1, width=5)
target_vertex_text.pack(side=tk.LEFT, padx=5)

# Create a frame for the DFS and BFS buttons
dfs_bfs_frame = tk.Frame(button_frame)
dfs_bfs_frame.pack(pady=10)

# Add the DFS and BFS buttons
run_DFS_button = tk.Button(dfs_bfs_frame, text="Run DFS", command=DFS)
run_DFS_button.pack(side=tk.LEFT, padx=5)

run_BFS_button = tk.Button(dfs_bfs_frame, text="Run BFS", command=BFS)
run_BFS_button.pack(side=tk.LEFT, padx=5)

# Show trace
output_text = tk.Text(button_frame, height=8, width=42)
output_text.bind("<Key>", disable_editing)
output_text.pack(pady=5)

# Start the Tkinter event loop
root.mainloop()
