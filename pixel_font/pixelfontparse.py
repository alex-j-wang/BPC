import os

dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(dir, 'pixelfontraw.txt'), 'r') as f:
    data = f.read()

entries = data.split('\n\n')

for entry in entries:
    filename = entry[0] + '.txt'
    with open(os.path.join(dir, filename), 'w') as f:
        f.write(entry[2:])