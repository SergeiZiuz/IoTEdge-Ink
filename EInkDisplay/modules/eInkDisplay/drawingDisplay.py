#!/usr/bin/python
# -*- coding:utf-8 -*-

import pdb
import epd7in5
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
from datetime import datetime

# VARS
FORMATTIMEFROMJSON = '%d/%m/%Y %H:%M'
SCREENTIMEFORMAT = '%H:%M'
MAXLINELENGTH = 35
FONT18 = ImageFont.truetype('./fonts/wqy-microhei.ttc', 18)
FONT24 = ImageFont.truetype('./fonts/wqy-microhei.ttc', 24)
FONT30 = ImageFont.truetype('./fonts/wqy-microhei.ttc', 30)
FONT46 = ImageFont.truetype('./fonts/wqy-microhei.ttc', 46)
LOGOPATH = './images/VTB.png'
BUSYPATH = './images/LogoBusy.bmp'
FREEPATH = './images/LogoFree.bmp'
# SENSOR = ''
# TEMPERATURE = ''
# HUMIDITY = ''
# DEVICEID = '4_3242289432'

class DrawingDisplay:
    def __init__(self, roomTitle, formatTime):
        self.roomTitle = roomTitle
        self.formatTime = formatTime
        self.sensor = ''
        self.temperature = ''
        self.humidity = ''
        self.deviceID = '4_3242289432'
        

    def drawDisplay(self, engagements):
        print("Engagements", engagements)
        if engagements != []:
            title = engagements[0]["Title"]
            countEngagements = len(engagements)
            if len(title) <= MAXLINELENGTH:
                self.drawOneLineDisplay(countEngagements, engagements)
            else:
                self.drawTwoLinesDisplay(countEngagements, engagements)
        else:
            self.drawDisplayWithoutEngagements()

    def drawRoomSensors(self, sensors):
        for sensor in sensors:
            print("DeviceID", sensor["DeviceId"])
            if sensor["DeviceId"] == self.deviceID:
                print("Sensor", sensor["ValueLabel"])
                if sensor["ValueLabel"] == 'Sensor':
                    self.sensor = sensor["Value"]
                    print('Sensor',sensor["Value"])
                elif sensor["ValueLabel"] == 'Temperature':
                    self.temperature = sensor["Value"]
                    print('Temperature', sensor["Value"])
                elif sensor["ValueLabel"] == 'Relative Humidity':
                    self.humidity = sensor["Value"]
                    print('Humidity', sensor["Value"])
        print(self.sensor, self.temperature, self.humidity)
        

    def drawOneLineDisplay(self, countEngagements, engagements):
        try:
            epd = epd7in5.EPD()
            epd.init()
            # epd.Clear(0xFF)

            HImage = Image.new('1', (epd7in5.EPD_WIDTH, epd7in5.EPD_HEIGHT), 255) # 255: Clear the frame
            draw = ImageDraw.Draw(HImage)

            # local var
            firstLineTime = ''
            firstLineText = ''
            secondLineTime = ''
            secondLineText = ''
            thirdLineTime = ''
            thirdLineText = ''

            countEngagements = 0
            for engagement in engagements:
                startTime = datetime.strptime(engagement["StartTime"], FORMATTIMEFROMJSON)
                timeEnd = datetime.strptime(engagement["EndTime"], FORMATTIMEFROMJSON)
                if countEngagements == 0:
                    firstLineTime = startTime.strftime(SCREENTIMEFORMAT) + "-" + timeEnd.strftime(SCREENTIMEFORMAT)
                    firstLineText = engagement["Title"]
                elif countEngagements == 1:
                    secondLineTime = startTime.strftime(SCREENTIMEFORMAT) + "-" + timeEnd.strftime(SCREENTIMEFORMAT)
                    secondLineText = engagement["Title"]
                elif countEngagements == 2:
                    thirdLineTime = startTime.strftime(SCREENTIMEFORMAT) + "-" + timeEnd.strftime(SCREENTIMEFORMAT)
                    thirdLineText = engagement["Title"]
                else:
                    print(engagement["Title"])
                countEngagements += 1
            
            # Draw frame
            draw.line((0, 90, 640, 90), fill = 0)
            draw.line((0, 91, 640, 91), fill = 0)
            draw.line((0, 92, 640, 92), fill = 0)
            draw.line((0, 93, 640, 93), fill = 0)
            draw.line((0, 94, 640, 94), fill = 0)
            draw.line((0, 158, 640, 158), fill = 0)
            draw.line((0, 222, 640, 222), fill = 0)
            draw.line((0, 286, 640, 286), fill = 0)
            draw.line((0, 287, 640, 287), fill = 0)
            draw.line((0, 288, 640, 288), fill = 0)
            draw.line((0, 289, 640, 289), fill = 0)
            draw.line((0, 290, 640, 290), fill = 0)
            draw.line((155, 94, 155, 290), fill = 0)

            # Draw logo
            png = Image.open(LOGOPATH)
            HImage.paste(png, (520, 20))
            busyLogo = Image.open(BUSYPATH)
            freeLogo = Image.open(FREEPATH)
            if self.sensor == 'True':
                HImage.paste(busyLogo, (530, 300))
            else:
                HImage.paste(freeLogo, (530, 300))
                draw.text((540, 305), 'Свободно', font = FONT18, fill = 0)


            # Draw title room
            draw.text((20, 30), self.roomTitle, font = FONT30, fill = 0)

            # Draw schedule
            draw.text((5, 110), firstLineTime, font = FONT24, fill = 0)
            draw.text((170, 110), firstLineText, font = FONT24, fill = 0)
            draw.text((5, 174), secondLineTime, font = FONT24, fill = 0)
            draw.text((170, 174), secondLineText, font = FONT24, fill = 0)
            draw.text((5, 238), thirdLineTime, font = FONT24, fill = 0)
            draw.text((170, 238), thirdLineText, font = FONT24, fill = 0)
            draw.text((5, 305), datetime.now().strftime(self.formatTime), font = FONT46, fill = 0)
            draw.text((440, 310), 't ' + str(self.temperature) + ' C', font = FONT24, fill = 0)
            draw.text((440, 340), 'h ' + str(self.humidity) + ' %', font = FONT24, fill = 0)

            epd.display(epd.getbuffer(HImage))
            time.sleep(2)
            epd.sleep()
        except:
            print('traceback.format_exc():\n%s', traceback.format_exc())
            exit()

    def separatingAtTwoLines(self, engagement):
        lengthEngagementTitle = len(engagement["Title"])
        if engagement["Title"][MAXLINELENGTH] != ' ':
            for count in range(1, MAXLINELENGTH):
                nc = MAXLINELENGTH - count
                if engagement["Title"][nc] == ' ':
                    firstStLineColon = engagement["Title"][0:nc]
                    secondStLineColon = engagement["Title"][nc+1:lengthEngagementTitle]
                    break
        else:
            firstStLineColon = engagement["Title"][0:MAXLINELENGTH]
            secondStLineColon = engagement["Title"][MAXLINELENGTH + 1:lengthEngagementTitle]
        rowLines = {"FirstLine": firstStLineColon, "SecondLine": secondStLineColon}
        return (rowLines)

    def drawTwoLinesDisplay(self, countEngagements, engagements):
        try:
            epd = epd7in5.EPD()
            epd.init()
            # epd.Clear(0xFF)

            HImage = Image.new('1', (epd7in5.EPD_WIDTH, epd7in5.EPD_HEIGHT), 255) # 255: Clear the frame
            draw = ImageDraw.Draw(HImage)

            # Local vars
            firstRowTime = ''
            firstRowOneLineText = ''
            firstRowTwoLineText = ''
            secondRowTime = ''
            secondRowOneLineText = ''
            secondRowTwoLineText = ''
            secondRowCenterLineText = ''
            # temperature = 't ' + str(self.temperature) + ' C'
            
            # Set local vars
            countEngagements = 0
            for engagement in engagements:
                startTime = datetime.strptime(engagement["StartTime"], FORMATTIMEFROMJSON)
                timeEnd = datetime.strptime(engagement["EndTime"], FORMATTIMEFROMJSON)
                if countEngagements == 0:
                    firstRowTime = startTime.strftime(SCREENTIMEFORMAT) + "-" + timeEnd.strftime(SCREENTIMEFORMAT)
                    firstRowOneLineText = self.separatingAtTwoLines(engagement)["FirstLine"]
                    firstRowTwoLineText = self.separatingAtTwoLines(engagement)["SecondLine"]
                elif countEngagements == 1:
                    secondRowTime = startTime.strftime(SCREENTIMEFORMAT) + "-" + timeEnd.strftime(SCREENTIMEFORMAT)
                    lengthEngagementTitle = len(engagement["Title"])
                    if lengthEngagementTitle > MAXLINELENGTH:
                        secondRowOneLineText = self.separatingAtTwoLines(engagement)["FirstLine"]
                        secondRowTwoLineText = self.separatingAtTwoLines(engagement)["SecondLine"]
                    else:
                        secondRowCenterLineText = engagement["Title"]
                else:
                    print(engagement["Title"])
                countEngagements += 1

            # Draw frame
            draw.line((0, 90, 640, 90), fill = 0)
            draw.line((0, 91, 640, 91), fill = 0)
            draw.line((0, 92, 640, 92), fill = 0)
            draw.line((0, 93, 640, 93), fill = 0)
            draw.line((0, 94, 640, 94), fill = 0)
            draw.line((0, 190, 640, 190), fill = 0)
            draw.line((0, 286, 640, 286), fill = 0)
            draw.line((0, 287, 640, 287), fill = 0)
            draw.line((0, 288, 640, 288), fill = 0)
            draw.line((0, 289, 640, 289), fill = 0)
            draw.line((0, 290, 640, 290), fill = 0)
            draw.line((155, 94, 155, 290), fill = 0)

            # Draw logo
            png = Image.open(LOGOPATH)
            HImage.paste(png, (520, 20))
            busyLogo = Image.open(BUSYPATH)
            freeLogo = Image.open(FREEPATH)
            if self.sensor == 'True':
                HImage.paste(busyLogo, (530, 300))
            else:
                HImage.paste(freeLogo, (530, 300))
                draw.text((540, 305), 'Свободно', font = FONT18, fill = 0)

            # Draw title room
            draw.text((20, 30), self.roomTitle, font = FONT30, fill = 0)

            # Draw schedule
            draw.text((5, 130), firstRowTime, font = FONT24, fill = 0)
            draw.text((170, 110), firstRowOneLineText, font = FONT24, fill = 0)
            draw.text((170, 145), firstRowTwoLineText, font = FONT24, fill=0)
            draw.text((5, 226), secondRowTime, font = FONT24, fill = 0)
            draw.text((170, 206), secondRowOneLineText, font = FONT24, fill = 0)
            draw.text((170, 241), secondRowTwoLineText, font = FONT24, fill = 0)
            draw.text((170, 226), secondRowCenterLineText, font = FONT24, fill=0)
            draw.text((5, 305), datetime.now().strftime(self.formatTime), font = FONT46, fill = 0)
            draw.text((440, 310), 't ' + str(self.temperature) + ' C', font = FONT24, fill = 0)
            draw.text((440, 340), 'h ' + str(self.humidity) + ' %', font = FONT24, fill = 0)

            epd.display(epd.getbuffer(HImage))
            time.sleep(2)
            epd.sleep()
        except:
            print('traceback.format_exc():\n%s', traceback.format_exc())
            exit()

    def drawDisplayWithoutEngagements(self):
        try:
            epd = epd7in5.EPD()
            epd.init()
            # epd.Clear(0xFF)

            HImage = Image.new('1', (epd7in5.EPD_WIDTH, epd7in5.EPD_HEIGHT), 255) # 255: Clear the frame
            draw = ImageDraw.Draw(HImage)

            # Draw frame
            draw.line((0, 90, 640, 90), fill = 0)
            draw.line((0, 91, 640, 91), fill = 0)
            draw.line((0, 92, 640, 92), fill = 0)
            draw.line((0, 93, 640, 93), fill = 0)
            draw.line((0, 94, 640, 94), fill = 0)
            draw.line((0, 286, 640, 286), fill = 0)
            draw.line((0, 287, 640, 287), fill = 0)
            draw.line((0, 288, 640, 288), fill = 0)
            draw.line((0, 289, 640, 289), fill = 0)
            draw.line((0, 290, 640, 290), fill = 0)

            # Draw logo
            png = Image.open(LOGOPATH)
            HImage.paste(png, (520, 20))
            busyLogo = Image.open(BUSYPATH)
            freeLogo = Image.open(FREEPATH)
            if self.sensor == 'True':
                HImage.paste(busyLogo, (530, 300))
            else:
                HImage.paste(freeLogo, (530, 300))
                draw.text((540, 305), 'Свободно', font = FONT18, fill = 0)

            # Draw title room
            draw.text((20, 30), self.roomTitle, font = FONT30, fill = 0)

            # Draw time
            draw.text((5, 305), datetime.now().strftime(self.formatTime), font = FONT46, fill = 0)

            # Draw sensors
            draw.text((440, 310), 't ' + str(self.temperature) + ' C', font = FONT24, fill = 0)
            draw.text((440, 340), 'h ' + str(self.humidity) + ' %', font = FONT24, fill = 0)

            epd.display(epd.getbuffer(HImage))
            time.sleep(2)
            epd.sleep()
        except:
            print('traceback.format_exc():\n%s', traceback.format_exc())
            exit()

### END OF FILE ###

