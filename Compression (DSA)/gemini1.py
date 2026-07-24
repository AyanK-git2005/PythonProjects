import numpy as np
from PIL import Image

# 1. Load Image and convert to a NumPy Array (must be 8-bit for 'P' mode later)
img = Image.open('smart_compressed.jpg').convert('RGB')
img_array = np.array(img, dtype=np.uint8)

# 2. Apply your custom quantization algorithm (e.g., 4-bit/16-level quantization)
# Example: Reducing 256 possibilities to 16 (0-15)
# Note: We divide by 16 and then multiply back to 'snap' the color to a new value.
quant_factor = 16
quantized_array = (img_array // quant_factor) * quant_factor

# The quantized_array now only contains 16 possible values for R, G, and B.
# It is still 24-bit RGB in form, but the information is greatly simplified.

# Convert the processed 3D NumPy array back to a PIL Image object
processed_img = Image.fromarray(quantized_array)

# 'colors=256' is the max. If your quantization resulted in, say, 100 unique colors, 
# Pillow will build a palette with those 100 colors.
max_palette_colors = 256 
palettized_img = processed_img.quantize(colors=max_palette_colors) 

# 'palettized_img' is now in 'P' mode (Palettized)
print(f"New Mode: {palettized_img.mode}") # Output: P

# For PNG (Lossless compression, excellent for palettized images)
palettized_img.save('comp_nature.png', 
                    optimize=True) # Use optimize flag for extra lossless reduction

# For GIF (Uses a strict 8-bit palette maximum)
# palettized_img.save('output_compressed.gif')