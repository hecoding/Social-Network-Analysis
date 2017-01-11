import xml.etree.ElementTree as ET
import itertools
import collections

filename = 'Albert_Elvira.xml'
tree = ET.parse(filename)
root = tree.getroot()

nodes = set()  # authors
edges = []  # articles

for entry in root.findall('r'):
    article = entry[0]
    article_authors = set(au.text.encode('utf-8') for au in article.findall('author'))

    # connect authors
    edges.append(list(itertools.combinations(article_authors, 2)))
    nodes |= article_authors

# convert set to list to have an order to set weight on edges
nodes = list(nodes)
# flatten the list of edges and sort each one for consistency
edges = [tuple(sorted(edge)) for edgelist in edges for edge in edgelist]
# count every occurrence of an edge
counter = collections.Counter(edges)
# convert edge list to set to eliminate repeated elements because we don't longer need them
edges = set(edges)


# outputting
with open('nodes.csv', 'w') as fnodes:
    fnodes.write('Id;Label\n')
    fnodes.writelines(str(i) + ';' + node + '\n' for i, node in enumerate(nodes))

with open('edges.csv', 'w') as fedges:
    fedges.write('Source;Target;Weight;Type\n')
    fedges.writelines(str(nodes.index(edge[0])) + ';' + str(nodes.index(edge[1])) + ';' + str(counter[edge]) + ';Undirected\n'
                      for edge in edges)
