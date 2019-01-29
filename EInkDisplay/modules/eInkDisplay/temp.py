#!/usr/bin/python3
# -*- coding:utf-8 -*-

import drawingDisplay

print('Start Creat display')
display = drawingDisplay.DrawingDisplay('Room Title', '123456 789012345678 901234 567890 1234 56789', 'time', 'format Time')

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
