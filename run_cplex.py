"""
COSC364 flow assignment 
Created by Yuxi (Harry) Chen
01/05/24
"""
import subprocess
import time

def print_results(transit_nodes, vars_c, vars_d, execute_time):
    print("Execute_time:", execute_time)

    #PRINT THE HIGHEST C CAPACITY
    highest_capacity_c = vars_c[0]
    print("CAPACITY")
    for item in vars_c: 
        if item[1] > highest_capacity_c[1]:
            highest_capacity_c = item
            print(highest_capacity_c)

    #PRINT THE HIGHEST D CAPACITY
    highest_capacity_d = vars_d[0]
    for item in vars_d: 
        if item[1] > highest_capacity_d[1]:
            highest_capacity_d = item
            print(highest_capacity_d)

    #Calculate number of non-zero capacity links
    non_zero_links_d = len([value for (name, value) in vars_d if value != 0])
    non_zero_links_c = len([value for (name, value) in vars_c if value != 0])
    non_zero_links = non_zero_links_d+non_zero_links_c
    print("Number of non-zero links:", non_zero_links)

    # Print the load for each transit node
    for transit_node, load in sorted(transit_nodes.items()):
        print(f"Transit node {transit_node}: {load}")
    
def run_cplex(): 
    start_time = time.time()
    command =  ["cplex", "-c", "read", r"C:\Users\chenh\Documents\cosc364\737.lp", "optimize", "display solution variables -"]
    proccess = subprocess.Popen(command, stdout=subprocess.PIPE)
    results = proccess.stdout.read().splitlines()
    end_time = time.time()
    run_time = end_time - start_time
    data = [d.decode('utf-8') for d in results]

    #variables list for capacity and nodes
    vars_x = []
    vars_c = []
    vars_d = []
    transit_nodes = {}

    # Process the lines and extract variables
    for line in data:
        parts = line.split()
        if len(parts) == 2:
            name, value = parts
            try:
                value = float(value)
                if name.startswith('x'):
                    vars_x.append((name, value))
                elif name.startswith('c'):
                    vars_c.append((name, value))
                elif name.startswith('d'):
                    vars_d.append((name, value))
            except ValueError:
                #Skips the non-readable lines/useless lines from data
                continue
    
    #Calculate transit node load and append to dict
    for node, load in vars_x:
        # Extract the transit node K from str(xikj)
        transit_node = node[2]
        if transit_node in transit_nodes:
            transit_nodes[transit_node] += load
        else:
            transit_nodes[transit_node] = load

    return transit_nodes, vars_c, vars_d, run_time

def main():
    transit_nodes, vars_c,vars_d, run_time=run_cplex()
    print_results(transit_nodes, vars_c,vars_d, run_time)

if __name__ == "__main__":
    main()