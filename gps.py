import serial  # import serial pacakge
import pygame, sys
from pygame.locals import *
import json
from shapely.geometry import shape, Point
import RPi.GPIO as GPIO
from time import sleep

# declare variables
minx = 9999  # minimum x coordinate from geojson coordinates
miny = 9999  # minimum y coordinate from geojson coordinates
maxx = 0  # maximum x coordinate from geojson coordinates
maxy = 0  # maximum y coordinate from geojson coordinates
GPIO.setwarnings(False)  # No warning for GPIO already in use
GPIO.setmode(GPIO.BCM)
buzzer = 23  # buzzer connected to pin 23
GPIO.setup(buzzer, GPIO.OUT)

width = 800  # screen width
height = 480  # screen height

# display starting values
mapKg = 0
mapPro = 0
kclKg = 0
kclPro = 0
catHa = 0
caPro = 0

# for id comparison for buzzer
idTemp = 0
id = 999

# map scale
scalex = 400
scaley = 236

# buzz time
buzz = 0.5

pygame.init()
windowSurface = pygame.display.set_mode((width, height))
myfont = pygame.font.SysFont("cambria", 100)  # font ant font size
myfont2 = pygame.font.SysFont("cambria", 50)

# finds minx, miny, maxx, maxy and calculates map scale
with open('LaukiGeojson/Ogas.geojson') as f:
    js = json.load(f)
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
scale = max(maxx - minx, maxy - miny)  # map scale


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

while True:
    received_data = (str)(ser.readline())  # read NMEA string received
    GPGGA_data_available = received_data.find(gpgga_info)  # check for NMEA GPGGA string
    if (GPGGA_data_available > 0):
        GPGGA_buffer = received_data.split("$GPGGA,", 1)[1]  # store data coming after "$GPGGA," string
        NMEA_buff = (GPGGA_buffer.split(','))  # store comma separated data in buffer
        GPS_Info()  # get time, latitude, longitude
        # print("lat in degrees:", lat_in_degrees, " long in degree: ", long_in_degrees, '\n')

        windowSurface.fill((0, 0, 0))  # fill screen black to prevent overlay
        mouse = pygame.mouse.get_pos()  # mouse position
        click = pygame.mouse.get_pressed()  # determane if mouse clicked, format (0,0,0)
        # if(mouse[0]>0 and mouse[0]<200 and mouse[1] > 0 and mouse[1]<90):
        # if(click[0] == 1):
        # pygame.display.toggle_fullscreen()

        # map zoom in
        if (mouse[0] > 600 and mouse[0] < 700 and mouse[1] > 390 and mouse[1] < 480):
            if (click[0] == 1):
                scalex *= 1.2
                scaley *= 1.2
        # map zoom out
        if (mouse[0] > 700 and mouse[0] < 800 and mouse[1] > 390 and mouse[1] < 480):
            if (click[0] == 1):
                scalex /= 1.2
                scaley /= 1.2

        # x, y constantes for map to be centered
        xconst = (50 * scale / scalex) + ((maxx + minx) / 2)
        yconst = (-5 * scale / scaley) + ((maxy + miny) / 2)

        for event in pygame.event.get():
            # top right exit button
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # fullscreen button
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    if (mouse[0] > 0 and mouse[0] < 200 and mouse[1] > 0 and mouse[1] < 90):
                        pygame.display.toggle_fullscreen()
                    if (mouse[0] > 400 and mouse[0] < 600 and mouse[1] > 390 and mouse[1] < 480):
                        buzz /= 2
                    if (mouse[0] > 200 and mouse[0] < 400 and mouse[1] > 390 and mouse[1] < 480):
                        buzz *= 2

        # construct point based on lon/lat returned by geocoder
        point = Point(float(lat_in_degrees), float(long_in_degrees))
        # load GeoJSON file containing sectors
        with open('LaukiGeojson/Paraugu_dati.geojson') as f:
            js = json.load(f)
        # check each polygon to see if it contains the point
        point = Point(float(lat_in_degrees), float(long_in_degrees))
        for feature in js['features']:
            polygon = shape(feature['geometry'])
            # read data from polygon
            if polygon.contains(point):
                id = feature['properties']['ID']
                mapPro = feature['properties']['map%']
                mapKg = feature['properties']['mapkg/h']
                kclKg = feature['properties']['kclkg/ha']
                kclPro = feature['properties']['kcl%']
                catHa = feature['properties']['cat/ha']
                caPro = feature['properties']['ca%']

            cord = feature['geometry']['coordinates'][0]  # get polygon coordinates
            i = 0
            x = float(lat_in_degrees)
            y = float(long_in_degrees)

            # move map instead of dot for map to be centered
            movex = xconst - x
            movey = yconst - y

            # calculate coordinates to pixel coordinates CAN BE OPTIMIZED BY PRECALCULATING
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

                pygame.draw.line(windowSurface, (255, 255, 255), (px, py), (px1, py1))  # draw line
                i += 1

        pygame.draw.circle(windowSurface, (255, 0, 0), (700, 195), 4)  # map centre
        # black rectangles for map to stay in boundaries
        pygame.draw.rect(windowSurface, (0, 0, 0),
                         (0, 0, 600, 480))
        pygame.draw.rect(windowSurface, (0, 0, 0),
                         (0, 390, 800, 90))

        # turn on buzzer if entered different polygon by id
        if (id != idTemp):
            GPIO.output(buzzer, GPIO.HIGH)
            sleep(buzz)
            GPIO.output(buzzer, GPIO.LOW)
            sleep(buzz)
            idTemp = id

        # render text
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

        label = myfont2.render(str(NMEA_buff[0]), 1, (255, 255, 255))
        windowSurface.blit(label, (10, 400))
        label = myfont2.render('Pilnekr.', 1, (255, 255, 255))
        windowSurface.blit(label, (10, 10))

        label = myfont.render(str(mapPro), 1, (255, 255, 255))
        windowSurface.blit(label, (420, 120))
        label = myfont.render(str(kclPro), 1, (255, 255, 255))
        windowSurface.blit(label, (420, 220))
        label = myfont.render(str(caPro), 1, (255, 255, 255))
        windowSurface.blit(label, (420, 320))

        # draw lines
        pygame.draw.line(windowSurface, (255, 255, 255), (0, 390), (800, 390), 2)
        pygame.draw.line(windowSurface, (255, 255, 255), (600, 0), (600, 480), 2)
        pygame.draw.line(windowSurface, (255, 255, 255), (700, 390), (700, 480), 2)
        pygame.draw.line(windowSurface, (255, 255, 255), (0, 90), (600, 90), 2)
        pygame.draw.line(windowSurface, (255, 255, 255), (0, 190), (600, 190), 2)
        pygame.draw.line(windowSurface, (255, 255, 255), (0, 290), (600, 290), 2)
        pygame.draw.line(windowSurface, (255, 255, 255), (200, 480), (200, 0), 2)
        pygame.draw.line(windowSurface, (255, 255, 255), (400, 390), (400, 0), 2)

        # +, -
        pygame.draw.line(windowSurface, (255, 255, 255), (625, 435), (675, 435), 4)
        pygame.draw.line(windowSurface, (255, 255, 255), (650, 411), (650, 459), 4)
        pygame.draw.line(windowSurface, (255, 255, 255), (725, 435), (775, 435), 4)

        label = myfont.render((str(buzz) + 's'), 1, (255, 255, 255))
        windowSurface.blit(label, (300, 400))

        # +, -
        pygame.draw.line(windowSurface, (255, 255, 255), (225, 435), (275, 435), 4)
        pygame.draw.line(windowSurface, (255, 255, 255), (250, 411), (250, 459), 4)
        pygame.draw.line(windowSurface, (255, 255, 255), (525, 435), (575, 435), 4)

        # update screen
        pygame.display.flip()