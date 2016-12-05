import sys
import itertools
import numpy as np

# Scale-free (Barabasi-Albert) Network generator
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
    for net_i in range(num_nets):
        # create initial complete graph
        nodes = [i for i in range(m0)]  # for efficiency, so that we won't have to create a range later on each choice
        edges = set([i for i in itertools.combinations(range(m0), 2)])
        degrees = [m0 - 1] * m0

        for step in range(t):
            probabilities = [degree / sum(degrees) for degree in degrees]
            choices = np.random.choice(nodes, m, replace=False, p=probabilities)  # nodes == indices (choices)

            nodes.append(nodes[-1] + 1)
            edges |= set([tuple(sorted((nodes[-1], nodes[choice]))) for choice in choices])

            degrees.append(m)
            for i in choices:
                degrees[i] += 1

        # outputting
        with open('nodes' + str(net_i) + 'm' + str(m) + 't' + str(t) + '.csv', 'w') as fnodes:
            fnodes.write('Id\n')
            fnodes.writelines(str(i) + '\n' for i in nodes)

        with open('edges' + str(net_i) + 'm' + str(m) + 't' + str(t) + '.csv', 'w') as fedges:
            fedges.write('Source;Target;Weight;Type\n')
            fedges.writelines(str(edge[0]) + ';' + str(edge[1]) + ';1;Undirected\n' for edge in edges)
