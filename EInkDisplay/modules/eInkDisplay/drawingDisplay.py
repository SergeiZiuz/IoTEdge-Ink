#!/usr/bin/python
# -*- coding:utf-8 -*-

import pdb
import epd7in5
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
from datetime import date

class DrawingDisplay:
    def __init__(self, roomTitle, formatTime):
        self.roomTitle = roomTitle
        self.formatTime = formatTime

    def drawDisplay(self, engagements):
        title = engagements[0]["Title"]
        countEngagements = len(engagements)
        if countEngagements != None:
            if len(title) <= 35:
                self.drawOneLineDisplay(countEngagements, engagements)
            else:
                self.drawTwoLinesDisplay(countEngagements, engagements)
        else:
            self.drawDisplayWithoutEngagements()

            # print(len(self.sensor))
            
            # self.drawTwoLinesDisplay()

    def drawOneLineDisplay(self, countEngagements, engagements):
        try:
            print('One line display')
            epd = epd7in5.EPD()
            epd.init()
            # epd.Clear(0xFF)

            HImage = Image.new('1', (epd7in5.EPD_WIDTH, epd7in5.EPD_HEIGHT), 255) # 255: Clear the frame
            draw = ImageDraw.Draw(HImage)

            # local var
            font24 = ImageFont.truetype('./fonts/wqy-microhei.ttc', 24)
            font30 = ImageFont.truetype('./fonts/wqy-microhei.ttc', 30)
            font46 = ImageFont.truetype('./fonts/wqy-microhei.ttc', 46)
            logoPath = './images/VTB.png'
            firstLineTime = ''
            firstLineText = ''
            secondLineTime = ''
            secondLineText = ''
            thirdLineTime = ''
            thirdLineText = ''
            currentTime = ''

            i = 0
            lt = len(engagements["StartTime"]) - 3
            for engagement in engagements:
                if i == 0:
                    firstLineTime = engagement["StartTime"][11:lt] + "-" + engagement["EndTime"][11:lt]
                    firstLineText = engagement["Title"]
                elif i == 1:
                    secondLineTime = engagement["StartTime"][11:lt] + "-" + engagement["EndTime"][11:lt]
                    secondLineText = engagement["Title"]
                elif i == 2:
                    thirdLineTime = engagement["StartTime"][11:lt] + "-" + engagement["EndTime"][11:lt]
                    thirdLineText = engagement["Title"]
                else:
                    print(engagement[i]["Title"])
                i += 1
            
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
            png = Image.open(logoPath)
            HImage.paste(png, (520, 20))

            # Draw title room
            draw.text((200, 30), self.roomTitle, font = font30, fill = 0)

            # Draw schedule
            draw.text((5, 110), firstLineTime, font = font24, fill = 0)
            draw.text((170, 110), firstLineText, font = font24, fill = 0)
            draw.text((5, 174), secondLineTime, font = font24, fill = 0)
            draw.text((170, 174), secondLineText, font = font24, fill = 0)
            draw.text((5, 238), thirdLineTime, font = font24, fill = 0)
            draw.text((170, 238), thirdLineText, font = font24, fill = 0)
            draw.text((5, 305), currentTime, font = font46, fill = 0)

            epd.display(epd.getbuffer(HImage))
            time.sleep(2)
            epd.sleep()
        except:
            print('traceback.format_exc():\n%s', traceback.format_exc())
            exit()

    def separatingAtTwoLines(self, engagement):
        lengthEngagementTitle = len(engagement["Title"])
        if engagement["Title"][35] != ' ':
            for i in range(1, 35):
                nc = 35 - i
                if engagement["Title"][nc] == ' ':
                    firstStLineColon = engagement["Title"][0:nc]
                    secondStLineColon = engagement[nc+1:lengthEngagementTitle]
                    break
        else:
            firstStLineColon = engagement["Title"][0:35]
            secondStLineColon = engagement["Title"][36:lengthEngagementTitle]
        rowLines = {"FirstLine": firstStLineColon, "SecondLine": secondStLineColon}
        return (rowLines)

    def drawTwoLinesDisplay(self, countEngagements, engagements):
        try:
            print('Two line display')
            epd = epd7in5.EPD()
            epd.init()
            # epd.Clear(0xFF)

            HImage = Image.new('1', (epd7in5.EPD_WIDTH, epd7in5.EPD_HEIGHT), 255) # 255: Clear the frame
            draw = ImageDraw.Draw(HImage)

            # Local vars
            font24 = ImageFont.truetype('./fonts/wqy-microhei.ttc', 24)
            font30 = ImageFont.truetype('./fonts/wqy-microhei.ttc', 30)
            font46 = ImageFont.truetype('./fonts/wqy-microhei.ttc', 46)
            logoPath = './images/VTB.png'
            firstRowTime = ''
            firstRowOneLineText = ''
            firstRowTwoLineText = ''
            secondRowTime = ''
            secondRowOneLineText = ''
            secondRowTwoLineText = ''
            currentTime = '19 Февраля 2019 14:56'
            
            # Set local vars
            i = 0
            lt = len(engagements["StartTime"]) - 3
            for engagement in engagements:
                if i == 0:
                    firstRowTime = engagements["StartTime"][11:lt] + "-" + engagements["EndTime"][11:lt]
                    # firstRowOneLineText = self.separatingAtTwoLines(engagement)["FirstLine"]
                    lengthEngagementTitle = len(engagement["Title"])
                    if engagement["Title"][35] != " ":
                        for i in range(1, 35):
                            nc = 35 - i
                            if engagement["Title"][nc] == ' ':
                                firstRowOneLineText = engagement["Title"][0:nc]
                                firstRowTwoLineText = engagement["Title"][nc+1:lengthEngagementTitle]
                                break
                    else:
                        firstRowOneLineText = engagement["Title"][0:35]
                        firstRowTwoLineText = engagement["Title"][36:lengthEngagementTitle]
                elif i == 1:
                    secondRowTime = engagements["StartTime"][11:lt] + "-" + engagements["EndTime"][11:lt]
                    lengthEngagementTitle = len(engagement["Title"])
                    if engagement["Title"][35] != " ":
                        for i in range(1, 35):
                            nc = 35 - i
                            if engagement["Title"][nc] == ' ':
                                secondRowOneLineText = engagement["Title"][0:nc]
                                secondRowTwoLineText = engagement["Title"][nc+1:lengthEngagementTitle]
                                break
                    else:
                        secondRowOneLineText = engagement["Title"][0:35]
                        secondRowTwoLineText = engagement["Title"][36:lengthEngagementTitle]
                else:
                    print(engagements[i]["Title"])
                i += 1

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
            png = Image.open(logoPath)
            HImage.paste(png, (520, 20))

            # Draw title room
            draw.text((200, 30), self.roomTitle, font = font30, fill = 0)

            # Draw schedule
            draw.text((5, 130), firstRowTime, font = font24, fill = 0)
            draw.text((170, 110), firstRowOneLineText, font = font24, fill = 0)
            draw.text((170, 145), firstRowTwoLineText, font = font24, fill=0)
            draw.text((5, 226), secondRowTime, font = font24, fill = 0)
            draw.text((170, 206), secondRowOneLineText, font = font24, fill = 0)
            draw.text((170, 241), secondRowTwoLineText, font = font24, fill = 0)
            draw.text((5, 305), currentTime, font = font46, fill = 0)

            epd.display(epd.getbuffer(HImage))
            time.sleep(2)
            epd.sleep()
        except:
            print('traceback.format_exc():\n%s', traceback.format_exc())
            exit()

    def drawDisplayWithoutEngagements(self):
        try:
            print('Drawing display without engagements')
            epd = epd7in5.EPD()
            epd.init()
            # epd.Clear(0xFF)

            HImage = Image.new('1', (epd7in5.EPD_WIDTH, epd7in5.EPD_HEIGHT), 255) # 255: Clear the frame
            draw = ImageDraw.Draw(HImage)

            # Local var
            logoPath = './images/VTB.png'

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
            png = Image.open(logoPath)
            HImage.paste(png, (520, 20))

            # Draw title room
            draw.text((200, 30), self.roomTitle, font = font30, fill = 0)

            epd.display(epd.getbuffer(HImage))
            time.sleep(2)
            epd.sleep()
        except:
            print('traceback.format_exc():\n%s', traceback.format_exc())
            exit()

### END OF FILE ###

