#getValues
import json
import csv

GEOJSON_FILE = 'LaukiGeojson/Zemdegas.geojson'
CSV_FILE = 'LaukiAnalizes/Zemdegas.csv'

with open(GEOJSON_FILE, encoding='utf8') as f:
    geo_data = json.load(f)

with open(CSV_FILE, encoding='utf8', newline='') as f:
    reader = csv.reader(f, delimiter=',')
    lines = list(reader)

for i, feature in enumerate(geo_data['features']):
    pH = feature['properties']['pH']
    if i < len(lines):
        lines[i][1] = pH
    else:
        lines.append([1, pH, 1, 1, 1])

with open(CSV_FILE, 'w', encoding='utf8', newline='') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerows(lines)