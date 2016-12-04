import sys
import itertools

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
        nodes = [i for i in range(m0)]
        edges = [i for i in itertools.combinations(range(m0), 2)]#make set
        degrees = [m0 - 1] * m0

        for step in range(t):
            probabilities = [degree / sum(degrees) for degree in degrees]
            indices = [i for i, v in enumerate(probabilities) if v >= sorted(probabilities)[-m]][:m]

            nodes.append(nodes[-1] + 1)
            new_edges = zip([nodes[-1]] * m, [nodes[i] for i in indices])
            edges.extend(tuple(sorted(i)) for i in new_edges)
            degrees.append(m)
            for i in indices:
                degrees[i] += 1
