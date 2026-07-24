from PIL import Image
import numpy as np

img = Image.open('leonida.png')

# Output basic information
print(f"Format: {img.format}") # e.g., 'JPEG'
print(f"Size: {img.size}")     # e.g., (800, 600)
print(f"Mode: {img.mode}")     # e.g., 'RGB'

# Pillow Image to NumPy Array
img_array = np.array(img)
print(img_array[0])
# for rows in range(img_array:
#     for cols in rows:
#         for colors in cols:
#             for val in colors[0:2]:
#                 new_val= (val+1)//16

# NumPy Array back to Pillow Image
#processed_img = Image.fromarray(img_array.astype(np.uint8))

# Save the result
#processed_img.save('output_custom.jpg')

# my algo is as follows:

# for rows in img_array:
#     for cols in rows:
#         for colors in cols:
#             for val in colors:
#                 val = (val+1)//16

# how would i use np array for this?