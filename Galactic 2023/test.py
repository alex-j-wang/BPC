from PIL import Image

# Load the image
image = Image.open('default (2).png')  # Replace 'your_image.png' with your image path

# Convert the image to RGB format (if not already in that mode)
image = image.convert('RGB')

# Get the width and height of the image
width, height = image.size

# Get the pixel data of the image as a list
pixels = list(image.getdata())

# Extract the first row of pixels
first_row = pixels[:width]

# Output the color values of the first row
print(['#%02x%02x%02x' % x for x in dict.fromkeys(first_row)])