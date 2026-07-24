import numpy as np
from PIL import Image
import os

def smart_downsample(input_path, output_path, block_size=4, variance_threshold=500):
    """
    Selectively downsamples an image based on the variance (difference) of pixels in local blocks.

    Args:
        input_path (str): Path to the input image.
        output_path (str): Path to save the processed image.
        block_size (int): The size of the square block (e.g., 4 means 4x4 pixels).
        variance_threshold (int): If a block's color variance is below this, it is averaged (compressed).
    """
    try:
        # 1. Load image and convert to NumPy array (ensuring 3 channels for RGB)
        img = Image.open(input_path).convert("RGB")
        img_array = np.array(img, dtype=np.float32) # Use float for calculations

        H, W, C = img_array.shape
        
        # Calculate the size of the new, processed array
        # The new dimensions will be larger than H/block_size, but smaller than H
        new_H = 0
        new_W = 0
        
        # List to store the new, processed pixel values
        processed_pixels = []

        # 2. Iterate through the image using defined blocks
        for i in range(0, H, block_size):
            row_pixels = []
            for j in range(0, W, block_size):
                # Define the current block slice (handling edges)
                block = img_array[i:i+block_size, j:j+block_size, :]
                
                # Check if the block is empty (only happens at the very end of edge cases)
                if block.size == 0:
                    continue

                # --- 3. CORE LOGIC: VARIANCE ANALYSIS ---
                
                # Calculate the variance across all color channels in the block.
                # High variance means high detail/drastic differences (e.g., an edge).
                # Low variance means uniform color (e.g., a sky or flat wall).
                color_variance = np.var(block) 
                
                if color_variance < variance_threshold:
                    # Case 1: Low Variance (Compress/Downsample)
                    # Average the block to a single pixel and append it.
                    avg_pixel = np.mean(block, axis=(0, 1))
                    
                    # Store the single averaged pixel.
                    row_pixels.append(avg_pixel)
                    
                else:
                    # Case 2: High Variance (Keep Detail)
                    # Keep the original pixels from the block.
                    # We flatten and then append each original pixel.
                    for row in block:
                        for pixel in row:
                            row_pixels.append(pixel)
                            
            processed_pixels.extend(row_pixels)
            
        # 4. Determine New Dimensions and Reconstruct the Image
        
        # Calculate the actual width based on the number of pixels processed in the first row
        # (This is complex because the width of each processed row can change, 
        # so this method needs a more structured output format than a simple list).
        
        # The simplest way to handle this variable-size output is to just create a long 1D array
        # and display the highly-mixed result, or to pad the downsampled blocks to the original size.
        
        print("\n--- Downsampling Complete ---")
        print("Note: Because high-variance blocks were expanded to their original size and low-variance blocks were reduced, the resulting image array is not a neat rectangle.")
        
        # To make this code functional and savable, we must choose a fixed output structure. 
        # For simplicity, let's stick to the block-averaging for now and refine the 'smart' output structure.

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

# --- Example Usage ---
# NOTE: Replace 'input.jpg' with the actual path to your image file
INPUT_FILE = 'Uncomp.png'
OUTPUT_FILE = 'smart_compressed2.jpg'

# 1. Setup a standard 4x4 block size and a moderate threshold
BLOCK_SIZE = 2
THRESHOLD = 8192

# 2. Refined Logic: Fixed Block Output (Slightly simpler, less true "adaptive resolution")
# A true adaptive resolution would require a non-rectangular image format (not supported by PNG/JPEG) 
# or a complex data structure that is too advanced for a basic introduction.
# Let's refine the logic to simply replace the block with an average or the original block data.

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
smart_downsample_fixed_output(INPUT_FILE, OUTPUT_FILE, block_size=4, variance_threshold=800)