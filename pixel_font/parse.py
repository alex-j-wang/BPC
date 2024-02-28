'''
Note: generate raw.c from .ttf file using the following website:
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
conversion = str.maketrans('%.', '█ ')

with open(os.path.join(dir, 'raw.c'), 'r') as f:
    data = f.read()

width = int(re.search(r'(?<=\.w_px = )\d+', data).group(0))
height = int(re.search(r'(?<=\.h_px = )\d+', data).group(0))

# Comments showing pixel font start with '//'
matches = re.findall(r'(?<=//)[\.%]{' + str(width) + '}', data)
if len(matches) != 26 * height:
    raise ParseError('Error: incorrect number of line matches')

pixel_font_map = {}
# Parse characters
for i, char in enumerate(string.ascii_uppercase):
    pixel_string = '\n'.join(matches[i * height: (i + 1) * height]).translate(conversion)
    pixel_font_map[char] = pixel_string

with open(os.path.join(dir, 'dim.json'), 'w') as f:
    json.dump({'width': width, 'height': height}, f, indent=4)

with open(os.path.join(dir, 'map.json'), 'w') as f:
    json.dump(pixel_font_map, f, indent=4)

with open(os.path.join(dir, 'display.txt'), 'w') as f:
    f.write('\n\n'.join(pixel_font_map.values()))