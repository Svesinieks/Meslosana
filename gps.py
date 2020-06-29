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

pygame.init()
windowSurface = pygame.display.set_mode((800, 480))
myfont = pygame.font.SysFont("cambria", 100)
id = 0
pH = 0
p = 0
k = 0
mg = 0

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

    print("NMEA Time: ", nmea_time, '\n')
    print("NMEA Latitude:", nmea_latitude, "NMEA Longitude:", nmea_longitude, '\n')

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

            print("lat in degrees:", lat_in_degrees, " long in degree: ", long_in_degrees, '\n')
            map_link = 'http://maps.google.com/?q=' + lat_in_degrees + ',' + long_in_degrees  # create link to plot location on Google map
            print(
                "<<<<<<<<press ctrl+c to plot location on google maps>>>>>>\n")  # press ctrl+c to plot on map and exit
            print("------------------------------------------------------------\n")

            windowSurface.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            # construct point based on lon/lat returned by geocoder
            point = Point(float(lat_in_degrees), float(long_in_degrees))
            # load GeoJSON file containing sectors
            with open('LaukiGeojson/Balti.geojson') as f:
                js = json.load(f)
            # check each polygon to see if it contains the point
            for feature in js['features']:
                polygon = shape(feature['geometry'])
                if polygon.contains(point):
                    id = feature['properties']['ID']
                    pH = feature['properties']['pH']
                    p = feature['properties']['P']
                    k = feature['properties']['K']
                    mg = feature['properties']['Mg']
                    print(id, pH, p, k, mg)


            # render text





            label = myfont.render('ID '+str(id), 1, (255, 255, 255))
            windowSurface.blit(label, (20, 20))
            label = myfont.render(str(pH)+' pH', 1, (255, 255, 255))
            windowSurface.blit(label, (20, 160))
            label = myfont.render(str(p)+' P', 1, (255, 255, 255))
            windowSurface.blit(label, (20, 240))
            label = myfont.render(str(k)+' K', 1, (255, 255, 255))
            windowSurface.blit(label, (20, 90))
            label = myfont.render(str(mg)+' Mg', 1, (255, 255, 255))
            windowSurface.blit(label, (20, 310))
            label = myfont.render(lat_in_degrees, 1, (255, 255, 255))
            windowSurface.blit(label, (70, 400))
            label = myfont.render(long_in_degrees, 1, (255, 255, 255))
            windowSurface.blit(label, (470, 400))

            pygame.draw.line(windowSurface,(255,255,255),(0,390),(800,390),2)
            pygame.draw.line(windowSurface, (255, 255, 255), (400, 0), (400, 390), 2)

            pygame.display.flip()

except KeyboardInterrupt:
    webbrowser.open(map_link)  # open current position information in google map
    sys.exit(0)

