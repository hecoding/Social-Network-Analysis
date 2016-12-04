import csv
import itertools
import collections

nodes = set()
edges = []

with open('input.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        mailContacts = row['Addresses'].split(':')
        # clean mail addresses
        mailContacts = [s.replace(';', '') for s in mailContacts]
        mailContacts = [s.replace('"', '') for s in mailContacts]
        # combinations of all recipients (n!)
        edges.append(list(itertools.combinations(mailContacts, 2)))
        for mail in mailContacts:
            # repeated elements do not get into
            nodes.add(mail)

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
