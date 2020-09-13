from koordinates import LKSToLatLon
import json

file = 'LaukiGeojson/Rozlejas_8.geojson'

def cords(file):
    cords = []
    with open(file) as f:
        data = json.load(f)
    for feature in data['features']:
        cords =  feature['geometry']['coordinates'][0]
        i = 0
        while len(cords) > i:
            x = []
            x += LKSToLatLon(cords[i][0], cords[i][1])
            i += 1
            print(x,', ')
        print('\n')
    return cords

cords(file)