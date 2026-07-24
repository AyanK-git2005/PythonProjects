import numpy as np
from PIL import Image
import os

def smart_downsample_fixed_output(input_path, output_path, block_size=4, variance_threshold=500):
    try:
        img = Image.open(input_path).convert("RGB")
        img_array = np.array(img, dtype=np.float32)
        H, W, C = img_array.shape

        # Ensure dimensions are multiples of block_size for simpler processing (crop any edges)
        H = H - (H % block_size)
        W = W - (W % block_size)
        img_array = img_array[:H, :W, :]

        # Create an output array of the same shape to overwrite blocks
        output_array = np.copy(img_array)

        # 1. Iterate over the image in blocks
        for i in range(0, H, block_size):
            for j in range(0, W, block_size):
                block = img_array[i:i+block_size, j:j+block_size, :]
                color_variance = np.var(block) 

                if color_variance < variance_threshold:
                    # Case 1: Low Variance (Compress the block)
                    # Calculate the average color of the block.
                    avg_pixel = np.mean(block, axis=(0, 1))
                    
                    # Fill the entire block in the output array with the single average color.
                    # This is quantization, not resolution change, but it simplifies the data for compression.
                    output_array[i:i+block_size, j:j+block_size, :] = avg_pixel
                
                # Case 2 (High Variance): If variance is high, the block in output_array remains unchanged 
                # (since output_array was a copy of img_array).

        # 2. Convert back to image, cast to 8-bit, and save.
        output_array = output_array.astype(np.uint8)
        processed_img = Image.fromarray(output_array)
        
        # Save as JPEG with high compression (low quality) to leverage the simplified data
        processed_img.save(output_path, quality=50, optimize=True)

        print(f"Successfully processed image saved to: {output_path}")
        print(f"Original size: {os.path.getsize(input_path) / 1024:.2f} KB")
        print(f"Compressed size: {os.path.getsize(output_path) / 1024:.2f} KB")

    except Exception as e:
        print(f"An error occurred: {e}")
        return False
        
# -----------------------------------------------------------
# To run this, ensure you have an image file named 'image_to_compress.jpg'
# in the same directory, and run the function:
# -----------------------------------------------------------
INPUT_FILE = 'red.jpg'
OUTPUT_FILE = 'smart_compressed.jpg'
smart_downsample_fixed_output(INPUT_FILE, OUTPUT_FILE, block_size=8, variance_threshold=600)