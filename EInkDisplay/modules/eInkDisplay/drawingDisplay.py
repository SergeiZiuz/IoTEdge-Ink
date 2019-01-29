#!/usr/bin/python
# -*- coding:utf-8 -*-

import pdb
import epd7in5
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
from datetime import date

# FIRSTLINECOLON = ''
# SECONDLINECOLON = ''

class DrawingDisplay:
    def __init__(self,  formatTime):
        self.roomSchedule = roomSchedule
        self.sensor = sensor
        self.currentTime1 = currentTime1
        self.formatTime = formatTime
        self.firstStLineColon = ''
        self.secondStLineColon = ''

    def drawDisplay(self):
        lengthSt = len(self.sensor)
        if lengthSt <= 35:
            print(len(self.sensor))
            self.firstStLineColon = self.sensor
            self.drawDisplayOneLine()
        else:
            print(len(self.sensor))
            if self.sensor[35] != ' ':
                for i in range(1, 35):
                    nc = 35 - i
                    if self.sensor[nc] == ' ':
                        self.firstStLineColon = self.sensor[0:nc]
                        self.secondStLineColon = self.sensor[nc+1:lengthSt]
                        print(self.firstStLineColon)
                        print(self.secondStLineColon)
                        break
                        
            else:
                self.firstStLineColon = self.sensor[0:35]
                self.secondStLineColon = self.sensor[36:lengthSt]
            self.drawTwoLinesDisplay()

    def drawDisplayOneLine(self):
        try:
            print('One line display')
            epd = epd7in5.EPD()
            epd.init()
            # epd.Clear(0xFF)

            HImage = Image.new('1', (epd7in5.EPD_WIDTH, epd7in5.EPD_HEIGHT), 255) # 255: Clear the frame
            draw = ImageDraw.Draw(HImage)

            #____
            font24 = ImageFont.truetype('./fonts/wqy-microhei.ttc', 24)
            font30 = ImageFont.truetype('./fonts/wqy-microhei.ttc', 30)
            font46 = ImageFont.truetype('./fonts/wqy-microhei.ttc', 46)
            logoPath = './images/VTB.png'
            # roomID = len(self.roomSchedule["RoomID"])
            # engagements_cnt = len(self.roomSchedule["Schedule"])

            # Temp ___
            #lableRoomText = 'Название комнаты'
            firstLineTime = '10:00 - 11:00'
            secondLineTime = '11:00 - 12:00'
            secondLineText = 'Test screen line two'
            thirdLineTime = '12:00 - 13:00'
            thirdLineText = 'Test screen line three'
            currentTime = '19 Февраля 2019 14:56'
            # ____

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
            draw.text((200, 30), self.roomSchedule, font = font30, fill = 0)

            # Draw schedule
            draw.text((5, 110), firstLineTime, font = font24, fill = 0)
            draw.text((170, 110), self.firstStLineColon, font = font24, fill = 0)
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

    def drawTwoLinesDisplay(self):
        try:
            print('Two line display')
            epd = epd7in5.EPD()
            epd.init()
            # epd.Clear(0xFF)

            HImage = Image.new('1', (epd7in5.EPD_WIDTH, epd7in5.EPD_HEIGHT), 255) # 255: Clear the frame
            draw = ImageDraw.Draw(HImage)

            #____
            font24 = ImageFont.truetype('./fonts/wqy-microhei.ttc', 24)
            font30 = ImageFont.truetype('./fonts/wqy-microhei.ttc', 30)
            font46 = ImageFont.truetype('./fonts/wqy-microhei.ttc', 46)
            logoPath = './images/VTB.png'

            # Temp ___
            #lableRoomText = 'Название комнаты'
            firstLineTime = '10:00 - 11:00'
            thirdLineTime = '12:00 - 13:00'
            thirdLineText = 'Test screen line three'
            currentTime = '19 Февраля 2019 14:56'
            # ____

            # Draw frame
            draw.line((0, 90, 640, 90), fill = 0)
            draw.line((0, 91, 640, 91), fill = 0)
            draw.line((0, 92, 640, 92), fill = 0)
            draw.line((0, 93, 640, 93), fill = 0)
            draw.line((0, 94, 640, 94), fill = 0)
            #draw.line((0, 158, 640, 158), fill = 0)
            draw.line((0, 190, 640, 190), fill = 0)
            #draw.line((0, 222, 640, 222), fill = 0)
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
            draw.text((200, 30), self.roomSchedule, font = font30, fill = 0)

            # Draw schedule
            draw.text((5, 130), firstLineTime, font = font24, fill = 0)
            draw.text((170, 110), self.firstStLineColon, font = font24, fill = 0)
            draw.text((170, 145), self.secondStLineColon, font = font24, fill=0)
            #draw.text((5, 174), secondLineTime, font = font24, fill = 0)
            #draw.text((170, 174), secondLineText, font = font24, fill = 0)
            draw.text((5, 226), thirdLineTime, font = font24, fill = 0)
            draw.text((170, 206), thirdLineText, font = font24, fill = 0)
            draw.text((170, 241), thirdLineText, font = font24, fill = 0)
            draw.text((5, 305), currentTime, font = font46, fill = 0)

            epd.display(epd.getbuffer(HImage))
            time.sleep(2)
            epd.sleep()
        except:
            print('traceback.format_exc():\n%s', traceback.format_exc())
            exit()

### END OF FILE ###

