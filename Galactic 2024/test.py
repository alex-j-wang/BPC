from PIL import Image

import numpy as np

# Load the image
image = Image.open('default.png')

# Get the colors of all pixels in the image
colors = np.array(image.getdata())

# Print the list of RGB values
print(colors.shape)