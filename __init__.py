# @victoriomolina

# Command Line Arguments
# argv[1] = image source
# argv[2] = scale factor
# argv[3] = image tuning factor
# argv[4] = resulted image bg color 
# argv[5] = gradient "from" color  
# argv[6] = gradient "to" color 
# argv[7] = result image path

import sys
import numpy as np
from PIL import Image, ImageFont, ImageDraw
from colour import Color

# Open the input file
img_src = sys.argv[1];
img = Image.open(img_src);

# Load the system font
font = ImageFont.load_default()

# Get letter with and height
letter_width = font.getsize("x")[0]
letter_height = font.getsize("x")[1]

WCF = letter_height / letter_width

# Get the scale factor
scale_factor = float(sys.argv[2])

# Calculate how many ASCII letters are needed to cover the image width and height
img_width = img.size[0]
img_height = img.size[1]
width_by_letter = round(img_width * WCF * scale_factor)
height_by_letter = round(img_height * scale_factor)
S = (width_by_letter, height_by_letter)

# Resize the image based on the symbol width and height
img = img.resize(S)

# Convert image colors to grayscale
# https://www.johndcook.com/blog/2009/08/24/algorithms-convert-color-grayscale/

img = np.sum(np.asarray(img), axis = 2)
img -= img.min()
img = (1.0 - img / img.max())

# Adjust the image brightness
image_tuning_factor = float(sys.argv[3])
img = img ** image_tuning_factor

# ASCII symbols ordered by degrees of darkness
ascii_symbols = np.asarray(list(' .,:irs?@9B&#'))

# Map grayscale values to the index of symbol in the array
img = (img * (ascii_symbols.size - 1)).astype(int)

# Generate the ASCII Art symbol lines 
lines = ("\n".join(("".join(symbol) for symbol in ascii_symbols[img]))).split("\n")

# Create an image object
bgcolor = sys.argv[4]
new_img_width = letter_width * width_by_letter
new_img_height = letter_height * height_by_letter
new_img = Image.new("RGBA", (new_img_width, new_img_height), bgcolor)
draw = ImageDraw.Draw(new_img)

# Define lines' colors within a gradient spectrum
gradient_from = sys.argv[5]
gradient_to = sys.argv[6]
n_bins = len(lines)
lines_colors = list(Color(gradient_from).range_to(Color(gradient_to), n_bins))

# Print symbols to image
padding_left = 0
y = 0
line_index=0
for line in lines:
  color = lines_colors[line_index]
  draw.text((padding_left, y), line, color.hex, font = font)
  y += letter_height
  line_index += 1

# Save the image
new_img_path = sys.argv[7]
new_img.save(new_img_path)
