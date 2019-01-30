#!/usr/bin/python
# -*- coding:utf-8 -*-

import pdb
import epd7in5
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
from datetime import datetime

class DrawingDisplay:
    def __init__(self, roomTitle, formatTime):
        self.roomTitle = roomTitle
        self.formatTime = formatTime

    def drawDisplay(self, engagements):
        print("Engagements", engagements)
        if engagements != []:
            title = engagements[0]["Title"]
            countEngagements = len(engagements)
            if len(title) <= 35:
                self.drawOneLineDisplay(countEngagements, engagements)
            else:
                self.drawTwoLinesDisplay(countEngagements, engagements)
        else:
            self.drawDisplayWithoutEngagements()

    def drawOneLineDisplay(self, countEngagements, engagements):
        try:
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
            currentTime = datetime.now().strftime('%d/%m/%Y %H:%M')

            countEngagements = 0
            for engagement in engagements:
                lt = len(engagement["StartTime"]) - 3
                if countEngagements == 0:
                    firstLineTime = engagement["StartTime"][11:lt] + "-" + engagement["EndTime"][11:lt]
                    firstLineText = engagement["Title"]
                elif countEngagements == 1:
                    secondLineTime = engagement["StartTime"][11:lt] + "-" + engagement["EndTime"][11:lt]
                    secondLineText = engagement["Title"]
                elif countEngagements == 2:
                    thirdLineTime = engagement["StartTime"][11:lt] + "-" + engagement["EndTime"][11:lt]
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
            for count in range(1, 35):
                nc = 35 - count
                if engagement["Title"][nc] == ' ':
                    firstStLineColon = engagement["Title"][0:nc]
                    secondStLineColon = engagement["Title"][nc+1:lengthEngagementTitle]
                    break
        else:
            firstStLineColon = engagement["Title"][0:35]
            secondStLineColon = engagement["Title"][36:lengthEngagementTitle]
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
            secondRowCenterLineText = ''
            currentTime = datetime.now().strftime('%d/%m/%Y %H:%M')
            
            # Set local vars
            countEngagements = 0
            for engagement in engagements:
                lt = len(engagement["StartTime"]) - 3
                if countEngagements == 0:
                    firstRowTime = engagement["StartTime"][11:lt] + "-" + engagement["EndTime"][11:lt]
                    firstRowOneLineText = self.separatingAtTwoLines(engagement)["FirstLine"]
                    firstRowTwoLineText = self.separatingAtTwoLines(engagement)["SecondLine"]
                elif countEngagements == 1:
                    secondRowTime = engagement["StartTime"][11:lt] + "-" + engagement["EndTime"][11:lt]
                    lengthEngagementTitle = len(engagement["Title"])
                    if lengthEngagementTitle > 35:
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
            draw.text((170, 226), secondRowCenterLineText, font = font24, fill=0)
            draw.text((5, 305), currentTime, font = font46, fill = 0)

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

            # Local var
            font30 = ImageFont.truetype('./fonts/wqy-microhei.ttc', 30)
            font46 = ImageFont.truetype('./fonts/wqy-microhei.ttc', 46)
            logoPath = './images/VTB.png'
            currentTime = datetime.now().strftime('%d/%m/%Y %H:%M')

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
            draw.text((5, 305), currentTime, font = font46, fill = 0)

            epd.display(epd.getbuffer(HImage))
            time.sleep(2)
            epd.sleep()
        except:
            print('traceback.format_exc():\n%s', traceback.format_exc())
            exit()

### END OF FILE ###

