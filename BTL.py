import numpy as np
import math
from ortools.graph.python import min_cost_flow
import networkx as nx
import matplotlib.pyplot as plt

# max node :50 
def main():
    num=int(input("Input number of nodes: "))
    origin=int(input("Input the origin: "))
    while origin>num:
        origin=int(input("Input the origin: "))
    destination=int(input("Input the destination: "))
    while destination>num:
        destination=int(input("Input the destination: "))
        
    smcf = min_cost_flow.SimpleMinCostFlow()
    
    start_nodes = np.random.randint(0,0,0)
    for i in range(0, num-1):
        if i+1 % math.sqrt(num) == 0:
            start_nodes = np.append(start_nodes, [i])
        elif i+1 < num-math.sqrt(num):
            start_nodes = np.append(start_nodes, [i, i])
        else:
            start_nodes = np.append(start_nodes, [i])
    print(start_nodes, len(start_nodes))
    end_nodes = np.random.randint(0,0,0)
    for i in range(0, num-1):
        if i+1 < num-int(math.sqrt(num)) and i+1 % int(math.sqrt(num)) != 0:
            end_nodes = np.append(end_nodes, [i+1 , i + int(math.sqrt(num))])
        elif i+1 % math.sqrt(num) == 0:
            end_nodes = np.append(end_nodes, [i + int(math.sqrt(num))])
        else:
            end_nodes = np.append(end_nodes, [i +1 ])
    print(end_nodes, len(end_nodes))
    
    G = nx.DiGraph()

# Add edges to the graph
    edges = list(zip(start_nodes, end_nodes))
    G.add_edges_from(edges)

    # Draw the graph
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_size=8, arrowsize=10)
    plt.show()

    capacities = np.random.randint( 100, 200, len(start_nodes))
    print(capacities, len(capacities))
    unit_costs = np.random.randint(1, 10, len(start_nodes))
    print(unit_costs, len(unit_costs))
    # Define an array of supplies at each node.
    supplies = [0]*num
    supplies[origin] = 200
    supplies[destination] = -200
    print(supplies)
    all_arcs = smcf.add_arcs_with_capacity_and_unit_cost(
        start_nodes, end_nodes, capacities, unit_costs
    )

    smcf.set_nodes_supplies(np.arange(0, len(supplies)), supplies)


    status = smcf.solve()
    # Tạo mảng NumPy trống
    array_of_tuples = np.array([])


# Thêm phần tử vào mảng
    if status != smcf.OPTIMAL:
        print("There was an issue with the min cost flow input.")
        print(f"Status: {status}")
        exit(1)
    print(f"Minimum cost: {smcf.optimal_cost()}")
    print("")
    print(" Arc    Flow / Capacity Cost")
    solution_flows = smcf.flows(all_arcs)
    costs = solution_flows * unit_costs
    for arc, flow, cost in zip(all_arcs, solution_flows, costs):
        if cost != 0:
            array_of_tuples=np.append(array_of_tuples,(int(smcf.tail(arc)), int(smcf.head(arc))))

            print(
                f"{smcf.tail(arc):1} -> {smcf.head(arc)}  {flow:3}  / {smcf.capacity(arc):3}       {cost}"
            )
    # Chuyển đổi thành mảng của các bộ số
    pair_array = [(array_of_tuples[i], array_of_tuples[i+1]) for i in range(0, len(array_of_tuples), 2)]
    new_edge_colors = ['red' if edge in pair_array else 'black' for edge in G.edges()]

    # Draw the graph with updated edge colors
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_size=8, arrowsize=10, edge_color=new_edge_colors)

    # Show the updated plot
    plt.show()
    # In ra mảng kết quả
    

main()