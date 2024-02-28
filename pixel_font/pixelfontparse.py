'''
Note: generate pixelfontraw from .ttf file using the following website:
https://lvgl.io/tools/font_conv_v5_3

Extend all characters of improper width
'''

import os
import re
import json
import string

class ParseError(Exception):
    pass

dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(dir, 'pixelfontraw.c'), 'r') as f:
    data = f.read()

width = int(re.search(r'(?<=\.w_px = )\d+', data).group(0))
height = int(re.search(r'(?<=\.h_px = )\d+', data).group(0))

matches = re.findall(r'(?<=//)[\.%]{' + str(width) + '}', data)
if len(matches) != 26 * height:
    raise ParseError('Error: incorrect number of line matches')

for i, char in enumerate(string.ascii_uppercase):
    bitmap = '\n'.join(matches[i * height: (i + 1) * height]).replace('%', '█').replace('.', ' ')
    with open(os.path.join(dir, f'{char}.txt'), 'w') as f:
        f.write(bitmap)

with open(os.path.join(dir, 'dim.json'), 'w') as f:
    json.dump({'width': width, 'height': height}, f)