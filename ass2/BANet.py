import sys
import itertools
import numpy as np

# Scale-free (Barabasi-Albert) Network generator
# You can pass to the script the number of links of an incoming node and the number of steps.
# Optionally you can pass in the number of networks to generate several ones with same settings.
#   i.e: BANet.py 3 20 3
if __name__ == "__main__":
    # args parsing
    args = sys.argv[1:]
    assert len(args) != 0, "Not enough arguments"
    assert len(args) == 2 or len(args) == 3, "Wrong number of arguments (m, t [, n])"
    m = int(args[0])
    t = int(args[1])
    num_nets = 1
    if len(args) == 3:
        num_nets = int(args[2])

    # generation
    m0 = m + 1
    total_num_nodes = m0 + t
    nodes = np.arange(total_num_nodes)  # preallocate for efficiency
    for net_i in range(num_nets):
        current_num_nodes = m0
        # create initial complete graph
        edges = set([i for i in itertools.combinations(range(m0), 2)])
        degrees = np.zeros(total_num_nodes)  # preallocate for efficiency
        degrees[:m0] = m0 - 1

        for step in range(t):
            # choose nodes to connect with
            probabilities = degrees / degrees.sum()
            choices = np.random.choice(nodes[:current_num_nodes], m, replace=False, p=probabilities[:current_num_nodes])  # nodes == indices (choices)

            # update nodes, edges and degrees of each node
            edges |= set([tuple(sorted((nodes[current_num_nodes], nodes[choice]))) for choice in choices])

            degrees[current_num_nodes] = m
            degrees[choices] += 1

            current_num_nodes += 1

        # outputting
        with open('nodes' + str(net_i) + 'm' + str(m) + 't' + str(t) + '.csv', 'w') as fnodes:
            fnodes.write('Id\n')
            fnodes.writelines(str(i) + '\n' for i in nodes)

        with open('edges' + str(net_i) + 'm' + str(m) + 't' + str(t) + '.csv', 'w') as fedges:
            fedges.write('Source;Target;Weight;Type\n')
            fedges.writelines(str(edge[0]) + ';' + str(edge[1]) + ';1;Undirected\n' for edge in edges)
