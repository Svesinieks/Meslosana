
import sys
import json
from shapely.geometry import shape, Point
# depending on your version, use: from shapely.geometry import shape, Point

poligoni = []
maxx = 56.57420958740996
maxy = 21.157708785995734
minx = 56.57136294966174
miny = 21.149561136265678

caMa = 0
caMi = 9999
mapMi = 9999
mapMa = 0
kclMi = 9999
kclMa = 0
with open('LaukiGeojson/Paraugu_dati.geojson') as f:
        js = json.load(f)

for feature in js['features']:
        cord = feature['geometry']['coordinates'][0]
        ca = feature['properties']['cat/ha']
        #print(ca)
        if ca > caMa:
                caMa = ca
                #print(f'caMa {caMa}')
        if ca < caMi and ca != 0:
                caMi = ca
                #print(f'caMi {caMi}')
        mapKg = feature['properties']['mapkg/h']
        if mapKg > mapMa:
                mapMa = mapKg
                #print(f'caMa {caMa}')
        if mapKg < mapMi and mapKg != 0:
                mapMi = mapKg
                #print(f'caMi {caMi}')
        #print(cord)
        kclKg = feature['properties']['kclkg/ha']
        if kclKg > kclMa:
                kclMa = kclKg
                #print(f'caMa {caMa}')
        if kclKg < kclMi and kclKg != 0:
                kclMi = kclKg
                #print(f'caMi {caMi}')
        #print(cord)
        poligoni.append(cord)
        i = 0
        ''''
        while i < len(cord) - 1:
                scale = max(maxx - minx, maxy - miny)

                px = cord[i][0]
                py = cord[i][1]
                px -= (maxx + minx) / 2
                py -= (maxy + miny) / 2

                px /= scale / 100
                py /= scale / 58
                py += 200
                px += 650
                poligoni[i].append((px,py))


                i += 1
        '''

for i in range(0, len(poligoni)):
        for j in range(0, len(poligoni[i])):
                scale = max(maxx - minx, maxy - miny)/5


                px = poligoni[i][j][0]
                py = poligoni[i][j][1]
                px -= (maxx + minx) / 2
                py -= (maxy + miny) / 2

                px /= scale / 100
                py /= scale / 58
                py += 200
                px += 200
                poligoni[i][j][0] = px
                poligoni[i][j][1] = py





