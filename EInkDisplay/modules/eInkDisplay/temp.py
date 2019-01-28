#!/usr/bin/python3
# -*- coding:utf-8 -*-

import drawingDisplay

print('Start Creat display')
display = drawingDisplay.DrawingDisplay('Room Title', '123456789012345678901234567890123456789', 'time', 'format Time')

display.drawDisplay()
#display.drawTwoLinesDisplay()

# {  
#     'type': 'object',
#     'properties': {
#         'RoomId': {
#             'type': 'string'
#         },
#         'Schedule': {
#             'type': 'array',
#             'items': {}
#         }
#     },
#     'required': [
#         'RoomId',
#         'Schedule'
#     ]
# }
