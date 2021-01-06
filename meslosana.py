import pygame
import sys
import json
from shapely.geometry import shape, Point, Polygon
from poligoni import poligoni, caMa, caMi, mapMa, mapMi, kclMa, kclMi
import numpy as np

laukumi = poligoni

# for id comparison for buzzer
idTemp = 0
id = 999
# buzz time
buzz = 0.5

maxx = 56.57420958740996
maxy = 21.157708785995734
minx = 56.57136294966174
miny = 21.149561136265678

minCa = caMi
maxCa = caMa
maxMap = mapMa
minMap = mapMi
kclMax = kclMa
kclMin = kclMi

pygame.init()
windowSurface = pygame.display.set_mode((800, 480))

myfont2 = pygame.font.SysFont("cambria", 50)

#
lat_in_degrees = 56.580603    #0
long_in_degrees = 21.157510   #0
#
piln = myfont2.render('Pilnekr.', 1, (255, 255, 255))
map = myfont2.render('MAP', 1, (255, 255, 255))
ca = myfont2.render('Ca', 1, (255, 255, 255))
kcl = myfont2.render('KCl', 1, (255, 255, 255))
mapProF = myfont2.render('MAP%', 1, (255, 255, 255))
caProF = myfont2.render('Ca%', 1, (255, 255, 255))
kclProF = myfont2.render('KCl%', 1, (255, 255, 255))
mapKilo = myfont2.render('MAP kg/ha', 1, (255, 255, 255))
caT = myfont2.render('Ca t/ha', 1, (255, 255, 255))
kclKilo = myfont2.render('KCl kg/ha', 1, (255, 255, 255))
#
izvele = 1
exit = False


while not exit:
    windowSurface.fill((0, 0, 0))
    # x, y constantes for map to be centered
    scale = max(maxx - minx, maxy - miny) / 5



    px = lat_in_degrees
    py = long_in_degrees
    px -= (maxx + minx) / 2
    py -= (maxy + miny) / 2
    px /= scale / 100
    py /= scale / 58
    py += 200
    px += 200
    movex = 400-px
    movey = 240-py

    for i in range(0, len(poligoni)):
        for j in range(0, len(poligoni[i])):
            poligoni[i][j][0] += movex
            poligoni[i][j][1] += movey
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True

        if event.type == pygame.MOUSEBUTTONUP:
            mouse = pygame.mouse.get_pos()  # mouse position
            click = pygame.mouse.get_pressed()  # determane if mouse clicked, format (0,0,0)
            if (mouse[0] > 750 and mouse[0] < 800 and mouse[1] > 50 and mouse[1] < 100):
                if buzz < 4:
                    buzz *=2
            elif (mouse[0] > 750 and mouse[0] < 800 and mouse[1] > 100 and mouse[1] < 150):
                if buzz > 0.25:
                    buzz/=2
            elif (mouse[0] > 0 and mouse[0] < 200 and mouse[1] > 0 and mouse[1] < 50):
                izvele = 1
            elif (mouse[0] > 200 and mouse[0] < 400 and mouse[1] > 0 and mouse[1] < 50):
                izvele = 2
            elif (mouse[0] > 400 and mouse[0] < 600 and mouse[1] > 0 and mouse[1] < 50):
                izvele = 3
            elif (mouse[0] > 600 and mouse[0] < 800 and mouse[1] > 0 and mouse[1] < 50):
                    pygame.display.toggle_fullscreen()

    # construct point based on lon/lat returned by geocoder
    point = Point(float(lat_in_degrees), float(long_in_degrees))
    with open('LaukiGeojson/Paraugu_dati.geojson') as f:
        js = json.load(f)
    i = 0
    for feature in js['features']:
        polygon = shape(feature['geometry'])
        if polygon.contains(point):
                id = feature['properties']['ID']
                mapPro = feature['properties']['map%']
                mapKg = feature['properties']['mapkg/h']
                kclKg = feature['properties']['kclkg/ha']
                kclPro = feature['properties']['kcl%']
                catHa = feature['properties']['cat/ha']
                caPro = feature['properties']['ca%']

        if izvele == 1:
            pygame.draw.rect(windowSurface, (60, 60, 60),
                                 (0, 0, 200, 50))
            windowSurface.blit(kclKilo, (5, 425))
            windowSurface.blit(kclProF, (405, 425))
            kclKg = feature['properties']['kclkg/ha']
            if polygon.contains(point):
                    label = myfont2.render((str(kclKg)), 1, (255, 255, 255))
                    windowSurface.blit(label, (300, 425))
                    label = myfont2.render((str(kclPro)), 1, (255, 255, 255))
                    windowSurface.blit(label, (700, 425))
            if kclKg == 0:
                #laukumi[i] = list(np.array(laukumi[i]) + 10)
                pygame.draw.polygon(windowSurface, (0, 0, 255), laukumi[i])
            else:
                #laukumi[i] = list(np.array(laukumi[i]) + 10)
                pygame.draw.polygon(windowSurface, (
                    (255 - ((1 / (kclMax - kclMin)) * (kclKg - kclMin)) * 255),
                    ((1 / (kclMax - minMap)) * (kclKg - kclMin)) * 255, 0), laukumi[i])
        elif izvele == 2:
            pygame.draw.rect(windowSurface, (60, 60, 60),
                                 (200, 0, 200, 50))
            catHa = feature['properties']['cat/ha']
            windowSurface.blit(caT, (5, 425))
            windowSurface.blit(caProF, (405, 425))
            if polygon.contains(point):
                label = myfont2.render((str(catHa)), 1, (255, 255, 255))
                windowSurface.blit(label, (300, 425))
                label = myfont2.render((str(caPro)), 1, (255, 255, 255))
                windowSurface.blit(label, (700, 425))
            if catHa == 0:
                pygame.draw.polygon(windowSurface, (0, 0, 255), laukumi[i])
            else:
                pygame.draw.polygon(windowSurface, (((255 - (
                        (1 / (maxCa - minCa)) * (catHa - minCa)) * 255),
                                                     ((1 / (maxCa - minCa)) * (catHa - minCa)) * 255,
                                                     0), laukumi[i]))
        elif izvele == 3:
            pygame.draw.rect(windowSurface, (60, 60, 60),
                                 (400, 0, 200, 50))
            mapKg = feature['properties']['mapkg/h']
            windowSurface.blit(mapKilo, (5, 425))
            windowSurface.blit(mapProF, (405, 425))
            if polygon.contains(point):
                label = myfont2.render((str(mapKg)), 1, (255, 255, 255))
                windowSurface.blit(label, (300, 425))
                label = myfont2.render((str(mapPro)), 1, (255, 255, 255))
                windowSurface.blit(label, (700, 425))
            if mapKg == 0:
                pygame.draw.polygon(windowSurface, (0, 0, 255), laukumi[i])
            else:
                pygame.draw.polygon(windowSurface, ((255 - ((1 / (maxMap - minMap)) * (mapKg - minMap)) * 255),
                                                    ((1 / (maxMap - minMap)) * (mapKg - minMap)) * 255, 0),
                                    laukumi[i])
        i+=1

    for i in range(0, len(laukumi)):
        for j in range(0, len(poligoni[i]) - 1):
            pygame.draw.line(windowSurface, (255, 255, 255), (poligoni[i][j][0], poligoni[i][j][1]),
                             (poligoni[i][j + 1][0], poligoni[i][j + 1][1]), 2)
            x = poligoni[i][j][0]
            y = poligoni[i][j][1]



    #izvele
    pygame.draw.line(windowSurface, (255, 255, 255), (0, 50), (800, 50), 2)
    pygame.draw.line(windowSurface, (255, 255, 255), (200, 0), (200, 50), 2)
    pygame.draw.line(windowSurface, (255, 255, 255), (400, 0), (400, 50), 2)
    pygame.draw.line(windowSurface, (255, 255, 255), (600, 0), (600, 50), 2)

    # + -
    pygame.draw.line(windowSurface, (255, 255, 255), (750, 50), (750, 150), 2)
    pygame.draw.line(windowSurface, (255, 255, 255), (750, 100), (800, 100), 2)
    pygame.draw.line(windowSurface, (255, 255, 255), (750, 150), (800, 150), 2)
    pygame.draw.line(windowSurface, (255, 255, 255), (760, 75), (790, 75), 2)
    pygame.draw.line(windowSurface, (255, 255, 255), (775, 60), (775, 90), 2)
    pygame.draw.line(windowSurface, (255, 255, 255), (760, 125), (790, 125), 2)

    #kg %
    pygame.draw.line(windowSurface, (255, 255, 255), (0, 430), (800, 430), 2)
    pygame.draw.line(windowSurface, (255, 255, 255), (400, 430), (400, 480), 2)

    windowSurface.blit(piln, (605, 2))
    windowSurface.blit(ca, (205, 2))
    windowSurface.blit(kcl, (5, 2))
    windowSurface.blit(map, (405, 2))

    # centrs
    x = float(lat_in_degrees)
    y = float(long_in_degrees)
    pygame.draw.circle(windowSurface, (10, 10, 10), (400, 240), 7)  # map centre
    pygame.draw.circle(windowSurface, (255, 0, 255), (400, 240), 4)  # map centre

    #buzz
    label = myfont2.render((str(buzz) + 's'), 1, (255, 255, 255))
    windowSurface.blit(label, (650, 50))
    pygame.display.flip()

    # turn on buzzer if entered different polygon by id
    '''
    if (id != idTemp):
        GPIO.output(buzzer, GPIO.HIGH)
        sleep(buzz)
        GPIO.output(buzzer, GPIO.LOW)
        sleep(buzz)
        idTemp = id
    '''


    for i in range(0, len(poligoni)):
        for j in range(0, len(poligoni[i])):
            poligoni[i][j][0] -= movex
            poligoni[i][j][1] -= movey