import os
import xml.etree.ElementTree as ET
import itertools
import collections

# wrong author names and its correction
fixed_names = {'wrong name': 'good name',
               }

nodes = set()  # authors
edges = []  # articles

# get directories
departments = next(os.walk('./xml'))[1]
prof_departments = {}

for department in departments:
    for xml_file in os.listdir(os.path.join('./xml', department)):
        if xml_file.endswith('.xml'):
            tree = ET.parse(os.path.join('./xml', department, xml_file))
            root = tree.getroot()

            for entry in root.findall('r'):
                article = entry[0]
                article_authors = set(fixed_names.get(au.text, au.text) for au in article.findall('author'))

                # connect authors
                edges.append(list(itertools.combinations(article_authors, 2)))
                nodes |= article_authors

            # save author department
            current_author = root.get('name')
            prof_departments[fixed_names.get(current_author, current_author)] = department

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
    fnodes.write('Id;Label;InFaculty;Department\n')
    fnodes.writelines(str(i) + ';' + node + ';' + str(node in prof_departments) + ';' + prof_departments.get(node, '') + '\n'
                      for i, node in enumerate(nodes))

with open('edges.csv', 'w', encoding='utf-8') as fedges:
    fedges.write('Source;Target;Weight;Type\n')
    fedges.writelines(str(nodes.index(edge[0])) + ';' + str(nodes.index(edge[1])) + ';' + str(counter[edge]) + ';Undirected\n'
                      for edge in edges)
