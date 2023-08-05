"""oximouse_formatter.py: Formats the oximouse data (https://oximouse.hms.harvard.edu/download.html) 
to be more ProteoSushi friendly"""

import csv

oxi_data = csv.reader(open("site_all.csv", 'r'))

formatted_data = open("oximouse_formatted.csv", 'w')

data_writer = csv.writer(formatted_data)

header = oxi_data.readline()
sequences = [i for i, h in enumerate(header) if "sequence" in h.lower()]
for row in oxi_data:
    i = 0
    while row[sequences[i]] != "NA":
        i += 1
    if i >= len(sequences):
        continue
    seq = row[sequences[i]]
    