import sys
import random
import itertools
import numpy

# Erdos-Renyi (or Random) Network generator
# You can pass to the script the number of nodes and the probability of linking two nodes. Optionally to generate
# several network with same settings you can pass in the number of networks.
#   i.e: ERNet.py 500 0.001 3
# Or if you type 'r' (from 'range') as first argument, you should then pass the number of nodes, a lower and upper bound
# of the probability, how many networks you want to be generated from that range and a boolean indicating whether
# you want to include the upper bound (capitalized). The probabilities will then be linearly spaced across the bounds.
#   i.e: ERNet.py r 500 0.2 0.5 10 False
if __name__ == "__main__":
    # args parsing
    args = sys.argv[1:]
    assert len(args) != 0, "Not enough arguments"
    if args[0] == 'r':
        assert len(args) == 6, "Wrong number of arguments"
        N = int(args[1])
        probs = [i for i in numpy.linspace(float(args[2]), float(args[3]), int(args[4]), endpoint=(args[5] == 'True'))]
        args = [None] * (len(probs) * 2)  # create a placeholder list, needed below
        args[::2] = [N] * (len(probs))
        args[1::2] = probs
    else:
        assert len(args) == 2 or len(args) == 3, "Wrong number of arguments (N, p [, n])"
        if len(args) == 3:
            args = [args[:2]] * int(args[2])
        else:
            args = [[args[0], args[1]]]

    for i, graph in enumerate(args):
        N = int(graph[0])
        p = float(graph[1])
        edges = []

        # generation
        for (a, b) in itertools.combinations(range(N), 2):
            if random.random() <= p:
                edges.append((a, b))

        # outputting
        with open('nodes' + str(i) + 'N' + str(N) + 'p' + str(p) + '.csv', 'w') as fnodes:
            fnodes.write('Id\n')
            fnodes.writelines(str(i) + '\n' for i in range(N))

        with open('edges' + str(i) + 'N' + str(N) + 'p' + str(p) + '.csv', 'w') as fedges:
            fedges.write('Source;Target;Weight;Type\n')
            fedges.writelines(str(edge[0]) + ';' + str(edge[1]) + ';1;Undirected\n' for edge in edges)
