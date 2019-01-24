#!/usr/bin/python
# -*- coding:utf-8 -*-

import epd7in5
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
from datetime import date

try:
    epd = epd7in5.EPD()
    epd.init()
    print("Clear")
    epd.Clear(0xFF)
    
    # Drawing on the Horizontal image
    print("Drawing on th Horizontal image")
    Himage = Image.new('1', (epd7in5.EPD_WIDTH, epd7in5.EPD_HEIGHT), 255)  # 255: clear the frame    
    draw = ImageDraw.Draw(Himage)
    font24 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 24)
    font30 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 30)
    font46 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 46)
    lableRoomText = 'Название комнаты'
    firstLineTime = '10:00 - 11:00'
    firstLineText = 'Test screen'
    secondLineTime = '11:00 - 12:00'
    secondLineText = 'Test screen line two'
    thirdLineTime = '12:00 - 13:00'
    thirdLineText = 'Test screen line three'
    currentTime = '19 Февраля 2019 14:56'
    print ("Drawing \"Text\"")
    draw.text((200, 30), lableRoomText, font = font30, fill = 0)
    draw.text((5, 110), firstLineTime, font = font24, fill = 0)
    draw.text((170, 110), firstLineText, font = font24, fill = 0)
    draw.text((5, 174), secondLineTime, font = font24, fill = 0)
    draw.text((170, 174), secondLineText, font = font24, fill = 0)
    draw.text((5, 238), thirdLineTime, font = font24, fill = 0)
    draw.text((170, 238), thirdLineText, font = font24, fill = 0)
    draw.text((5, 305), currentTime, font = font46, fill = 0)
    print("read bmp file on window")
    bmp = Image.open('VTB.png')
    Himage.paste(bmp, (520,20))
    print ("Drawing \"Line\"")
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
#    draw.rectangle((20, 50, 70, 100), outline = 0)
#    draw.line((165, 50, 165, 100), fill = 0)
#    draw.line((140, 75, 190, 75), fill = 0)
#    draw.arc((140, 50, 190, 100), 0, 360, fill = 0)
#    draw.rectangle((80, 50, 130, 100), fill = 0)
#    draw.chord((200, 50, 250, 100), 0, 360, fill = 0)
    Himage.save("vtb.bmp")
    epd.display(epd.getbuffer(Himage))
    time.sleep(2)
    
    # Drawing on the Vertical image
#    Limage = Image.new('1', (epd7in5.EPD_HEIGHT, epd7in5.EPD_WIDTH), 255)  # 255: clear the frame
#    draw = ImageDraw.Draw(Limage)
#    font18 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 18)
#    draw.text((2, 0), 'hello world', font = font18, fill = 0)
#    draw.text((2, 20), '7.5inch epd', font = font18, fill = 0)
#    draw.text((20, 50), u'微雪电子', font = font18, fill = 0)
#    draw.line((10, 90, 60, 140), fill = 0)
#    draw.line((60, 90, 10, 140), fill = 0)
#    draw.rectangle((10, 90, 60, 140), outline = 0)
#    draw.line((95, 90, 95, 140), fill = 0)
#    draw.line((70, 115, 120, 115), fill = 0)
#    draw.arc((70, 90, 120, 140), 0, 360, fill = 0)
#    draw.rectangle((10, 150, 60, 200), fill = 0)
#    draw.chord((70, 150, 120, 200), 0, 360, fill = 0)
#    epd.display(epd.getbuffer(Limage))
#    time.sleep(2)
    
#    print("read bmp file")
#    Himage = Image.open('7in5.bmp')
#   epd.display(epd.getbuffer(Himage))
#    time.sleep(2)
    
#    print("read bmp file on window")
#    Himage2 = Image.new('1', (epd7in5.EPD_WIDTH, epd7in5.EPD_HEIGHT), 255)  # 255: clear the frame
#    bmp = Image.open('100x100.bmp')
#    Himage2.paste(bmp, (50,10))
#    epd.display(epd.getbuffer(Himage2))
#    time.sleep(2)
    
#    print("Drawing")
#    Himage3 = Image.new('1', (epd7in5.EPD_WIDTH, epd7in5.EPD_HEIGHT), 255)
#    draw = ImageDraw.Draw(Himage3)
#    font18 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 18)
#    draw.text((268, 102), 'VTB', font = font24, fill = 0)
#    draw.line((0, 130, 640, 130), fill = 20)
#    epd.display(epd.getbuffer(Himage3))
#    time.sleep(2)

    epd.sleep()
        
except:
    print('traceback.format_exc():\n%s', traceback.format_exc())
    exit()

