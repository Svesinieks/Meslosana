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
    id = feature['properties']['ID']
    print(id)
    pH = feature['properties']['pH']
    p = feature['properties']['P']
    k = feature['properties']['K']
    mg = feature['properties']['Mg']
    if i+1 < len(lines):

        lines[0][0] = 'ID'
        lines[0][1] = 'pH'
        lines[0][2] = 'P'
        lines[0][3] = 'K'
        lines[0][4] = 'Mg'

        lines[i+1][0] = id
        lines[i+1][1] = pH
        lines[i+1][2] = p
        lines[i+1][3] = k
        lines[i+1][4] = mg
    else:
        lines.append([id, pH, p, k, mg])

with open(CSV_FILE, 'w', encoding='utf8', newline='') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerows(lines)