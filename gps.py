import serial  # import serial pacakge
from time import sleep
import webbrowser  # import package for opening link in browser
import sys  # import system package
import csv
import pygame, sys
from pygame.locals import *
import json
from shapely.geometry import shape, Point
import random
import RPi.GPIO as GPIO
from time import sleep

with open('LaukiGeojson/Balti.geojson') as f:
    js = json.load(f)
minx = 9999
miny = 9999
maxx = 0
maxy = 0
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
buzzer = 23
GPIO.setup(buzzer, GPIO.OUT)

for feature in js['features']:
    cord = feature['geometry']['coordinates'][0]
    i = 0

    while i < len(cord):
        if minx > cord[i][0]:
            minx = cord[i][0]
        if maxx < cord[i][0]:
            maxx = cord[i][0]
        if miny > cord[i][1]:
            miny = cord[i][1]
        if maxy < cord[i][1]:
            maxy = cord[i][1]

        i += 1
scale = max(maxx - minx, maxy - miny)

pygame.init()
windowSurface = pygame.display.set_mode((800, 480))
myfont = pygame.font.SysFont("cambria", 100)
mapKg = 0
mapPro = 0
kclKg = 0
kclPro = 0
catHa = 0
caPro = 0
idTemp = 0
id = 999
scalex = 400
scaley = 236


def GPS_Info():
    global NMEA_buff
    global lat_in_degrees
    global long_in_degrees
    nmea_time = []
    nmea_latitude = []
    nmea_longitude = []
    nmea_time = NMEA_buff[0]  # extract time from GPGGA string
    nmea_latitude = NMEA_buff[1]  # extract latitude from GPGGA string
    nmea_longitude = NMEA_buff[3]  # extract longitude from GPGGA string

    # print("NMEA Time: ", nmea_time, '\n')
    # print("NMEA Latitude:", nmea_latitude, "NMEA Longitude:", nmea_longitude, '\n')

    lat = float(nmea_latitude)  # convert string into float for calculation
    longi = float(nmea_longitude)  # convertr string into float for calculation

    lat_in_degrees = convert_to_degrees(lat)  # get latitude in degree decimal format
    long_in_degrees = convert_to_degrees(longi)  # get longitude in degree decimal format


# convert raw NMEA string into degree decimal format
def convert_to_degrees(raw_value):
    decimal_value = raw_value / 100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - int(decimal_value)) / 0.6
    position = degrees + mm_mmmm
    position = "%.4f" % (position)
    return position


gpgga_info = "$GPGGA,"
ser = serial.Serial("/dev/ttyS0")  # Open port with baud rate
GPGGA_buffer = 0
NMEA_buff = 0
lat_in_degrees = 0
long_in_degrees = 0

try:
    while True:
        received_data = (str)(ser.readline())  # read NMEA string received
        GPGGA_data_available = received_data.find(gpgga_info)  # check for NMEA GPGGA string
        if (GPGGA_data_available > 0):
            GPGGA_buffer = received_data.split("$GPGGA,", 1)[1]  # store data coming after "$GPGGA," string
            NMEA_buff = (GPGGA_buffer.split(','))  # store comma separated data in buffer
            GPS_Info()  # get time, latitude, longitude

            # print("lat in degrees:", lat_in_degrees, " long in degree: ", long_in_degrees, '\n')
            # map_link = 'http://maps.google.com/?q=' + lat_in_degrees + ',' + long_in_degrees  # create link to plot location on Google map
            # print(
            # "<<<<<<<<press ctrl+c to plot location on google maps>>>>>>\n")  # press ctrl+c to plot on map and exit
            # print("------------------------------------------------------------\n")

            windowSurface.fill((0, 0, 0))
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            # if(mouse[0]>0 and mouse[0]<200 and mouse[1] > 0 and mouse[1]<90):
            # if(click[0] == 1):
            # pygame.display.toggle_fullscreen()
            if (mouse[0] > 600 and mouse[0] < 700 and mouse[1] > 390 and mouse[1] < 480):
                if (click[0] == 1):
                    scalex *= 1.2
                    scaley *= 1.2
            if (mouse[0] > 700 and mouse[0] < 800 and mouse[1] > 390 and mouse[1] < 480):
                if (click[0] == 1):
                    scalex /= 1.2
                    scaley /= 1.2
            xconst = (50 * scale / scalex) + ((maxx + minx) / 2)
            yconst = (-5 * scale / scaley) + ((maxy + miny) / 2)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        if (mouse[0] > 0 and mouse[0] < 200 and mouse[1] > 0 and mouse[1] < 90):
                            pygame.display.toggle_fullscreen()

            # construct point based on lon/lat returned by geocoder
            point = Point(float(lat_in_degrees), float(long_in_degrees))
            # load GeoJSON file containing sectors
            with open('LaukiGeojson/Paraugu_dati.geojson') as f:
                js = json.load(f)
            # check each polygon to see if it contains the point
            point = Point(float(lat_in_degrees), float(long_in_degrees))
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
                cord = feature['geometry']['coordinates'][0]
                i = 0
                x = float(lat_in_degrees)
                y = float(long_in_degrees)

                movex = xconst - x
                movey = yconst - y
                while i < len(cord) - 1:
                    px = cord[i][0] + movex
                    py = cord[i][1] + movey
                    px -= (maxx + minx) / 2
                    py -= (maxy + miny) / 2
                    px1 = cord[i + 1][0] + movex
                    py1 = cord[i + 1][1] + movey
                    px1 -= (maxx + minx) / 2
                    py1 -= (maxy + miny) / 2
                    px /= scale / scalex
                    py /= scale / scaley
                    py += 200
                    px += 650
                    px1 /= scale / scalex
                    py1 /= scale / scaley
                    py1 += 200
                    px1 += 650

                    pygame.draw.line(windowSurface, (255, 255, 255), (px, py), (px1, py1))

                    i += 1

            pygame.draw.circle(windowSurface, (255, 0, 0), (700, 195), 4)
            pygame.draw.rect(windowSurface, (0, 0, 0),
                             (0, 0, 600, 480))
            pygame.draw.rect(windowSurface, (0, 0, 0),
                             (0, 390, 800, 90))
            # render text

            if (id != idTemp):
                GPIO.output(buzzer, GPIO.HIGH)
                sleep(0.5)
                GPIO.output(buzzer, GPIO.LOW)
                sleep(0.5)
                idTemp = id

            label = myfont.render('MAP ', 1, (255, 255, 255))
            windowSurface.blit(label, (20, 120))
            label = myfont.render('KCl ', 1, (255, 255, 255))
            windowSurface.blit(label, (20, 220))
            label = myfont.render('Ca ', 1, (255, 255, 255))
            windowSurface.blit(label, (20, 320))

            label = myfont.render('Kg/ha ', 1, (255, 255, 255))
            windowSurface.blit(label, (205, 15))
            label = myfont.render('% ', 1, (255, 255, 255))
            windowSurface.blit(label, (470, 15))

            label = myfont.render(str(mapKg), 1, (255, 255, 255))
            windowSurface.blit(label, (220, 120))
            label = myfont.render(str(kclKg), 1, (255, 255, 255))
            windowSurface.blit(label, (220, 220))
            label = myfont.render(str(catHa), 1, (255, 255, 255))
            windowSurface.blit(label, (220, 320))

            label = myfont.render(str(mapPro), 1, (255, 255, 255))
            windowSurface.blit(label, (420, 120))
            label = myfont.render(str(kclPro), 1, (255, 255, 255))
            windowSurface.blit(label, (420, 220))
            label = myfont.render(str(caPro), 1, (255, 255, 255))
            windowSurface.blit(label, (420, 320))

            pygame.draw.line(windowSurface, (255, 255, 255), (0, 390), (800, 390), 2)
            pygame.draw.line(windowSurface, (255, 255, 255), (600, 0), (600, 480), 2)
            pygame.draw.line(windowSurface, (255, 255, 255), (700, 390), (700, 480), 2)
            pygame.draw.line(windowSurface, (255, 255, 255), (0, 90), (600, 90), 2)
            pygame.draw.line(windowSurface, (255, 255, 255), (0, 190), (600, 190), 2)
            pygame.draw.line(windowSurface, (255, 255, 255), (0, 290), (600, 290), 2)
            pygame.draw.line(windowSurface, (255, 255, 255), (200, 390), (200, 0), 2)
            pygame.draw.line(windowSurface, (255, 255, 255), (400, 390), (400, 0), 2)

            pygame.display.flip()

except KeyboardInterrupt:
    # webbrowser.open(map_link)  # open current position information in google map
    sys.exit(0)

