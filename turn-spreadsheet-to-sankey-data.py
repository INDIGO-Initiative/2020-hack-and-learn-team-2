import csv

#----------------------- INPUT
# Download the team spreadsheet, save it as a CSV called "sankey.csv"


#----------------------- Get Raw data
data = []
with open('sankey.csv') as csvfile:
     reader = csv.reader(csvfile)
     # Skip header row
     next(reader)
     # get data
     for row in reader:
        if row[0].strip() and row[6].strip() and row[19].strip() and row[19].strip().startswith('GOAL'):
            item = {
                'project_id': row[0].strip(),
                'outcome_id': row[6].strip(),
                'primary_goal': row[19].strip().split(':')[0][5:],
                'primary_target': row[20].strip().split(' ')[0]
            }
            data.append(item)

#----------------------- Convert Raw Data to node / node / count data

class SankeyData:

    def __init__(self):
        self.data = {}

    def add(self, node1, node2):
        if node1 not in self.data:
            self.data[node1] = {}

        if node2 not in self.data[node1]:
            self.data[node1][node2] = 0

        self.data[node1][node2] += 1

    def get_data_as_string(self):
        out = ''
        for node1 in self.data.keys():
            for node2 in self.data[node1].keys():
                out += \
                    node1.replace(',', '') + ',' + \
                    node2.replace(',', '') + ',' + \
                    str(self.data[node1][node2]) + "\n"
        return out

sankey_data = SankeyData()
for d in data:
    sankey_data.add(d['project_id'], d['primary_goal'])
    if d['primary_target']:
        sankey_data.add(d['primary_goal'], d['primary_target'])

#----------------------- Output data

with open('sankey.txt', 'w') as out_file:
    out_file.write(sankey_data.get_data_as_string())
