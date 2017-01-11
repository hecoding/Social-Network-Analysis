import os

for xml_file in os.listdir('.'):
    if xml_file.endswith('.xml'):
        print(xml_file)
