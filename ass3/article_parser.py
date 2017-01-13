import os
import xml.etree.ElementTree as ET
import itertools
import collections

# wrong author names and its correction
fixed_names = {'Eduardo Huedo Cuesta': 'Eduardo Huedo',
               'Victoria Lopez': 'Victoria López',
               'Juan C. Fabero': 'Juan Carlos Fabero Jiménez',
               'Juan Carlos Fabero': 'Juan Carlos Fabero Jiménez',
               'Sara Roman': 'Sara Román Navarro',
               'J. Manuel Velasco': 'José Manuel Velasco',
               'J. J. Ruz Ortiz': 'José Jaime Ruz',
               'David de Frutos Escrig': 'David de Frutos-Escrig',
               'Antonio Gavilanes-Franco': 'Antonio Gavilanes',
               'Miguel Palomino Tarjuelo': 'Miguel Palomino',
               'Susana Bautista-Blasco': 'Susana Bautista',
               'Carlos Leon': 'Carlos León'
               }

nodes = set()  # authors
edges = []  # articles

for xml_file in os.listdir('./xml'):
    if xml_file.endswith('.xml'):
        filename = xml_file
        tree = ET.parse('./xml/' + filename)
        root = tree.getroot()

        for entry in root.findall('r'):
            article = entry[0]
            article_authors = set(fixed_names.get(au.text, au.text) for au in article.findall('author'))

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
with open('nodes.csv', 'w', encoding='utf-8') as fnodes:
    fnodes.write('Id;Label\n')
    fnodes.writelines(str(i) + ';' + node + '\n' for i, node in enumerate(nodes))

with open('edges.csv', 'w', encoding='utf-8') as fedges:
    fedges.write('Source;Target;Weight;Type\n')
    fedges.writelines(str(nodes.index(edge[0])) + ';' + str(nodes.index(edge[1])) + ';' + str(counter[edge]) + ';Undirected\n'
                      for edge in edges)
