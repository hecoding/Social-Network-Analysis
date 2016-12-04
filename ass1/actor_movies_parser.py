import csv
import itertools
import collections

nodes = set()
edges = []

with open('actorMovies.csv') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        moviesRow = set(row['Movies'].replace('"', '').split('|'))
        # clean movie titles
        moviesRow.discard('')
        # connect movies
        edges.append(list(itertools.combinations(moviesRow, 2)))
        nodes |= moviesRow

# convert set to list to have an order to set weight on edges
nodes = list(nodes)
# flatten the list of edges and sort each one for consistency
edges = [tuple(sorted(edge)) for edgelist in edges for edge in edgelist]
# count every occurrence of an edge
counter = collections.Counter(edges)
# convert edge list to set to eliminate repeated elements because we don't longer need them
edges = set(edges)


with open('nodes.csv', 'w') as fnodes:
    fnodes.write('Id;Label\n')
    fnodes.writelines(str(i) + ';' + str(node) + '\n' for i, node in enumerate(nodes))

with open('edges.csv', 'w') as fedges:
    fedges.write('Source;Target;Weight;Type\n')
    fedges.writelines(str(nodes.index(edge[0])) + ';' + str(nodes.index(edge[1])) + ';' + str(counter[edge]) + ';Undirected\n'
                      for edge in edges)
