from PIL import Image
import io

def image_to_pixel_sequence(image_path):
    """Converts an image to a flat list of (R, G, B) tuples."""
    img = Image.open(image_path).convert("RGB")
    width, height = img.size
    pixels = list(img.getdata())
    return pixels, width, height

def custom_rle_compress(data):
    """Applies Run-Length Encoding to the pixel data."""
    if not data:
        return []

    compressed_data = []
    count = 1
    current_pixel = data[0]

    for next_pixel in data[1:]:
        if next_pixel == current_pixel and count < 255: # Max run length for simplicity
            count += 1
        else:
            # Store the run as: (count, pixel_tuple)
            compressed_data.append((count, current_pixel))
            current_pixel = next_pixel
            count = 1
            
    # Add the last run
    compressed_data.append((count, current_pixel))
    return compressed_data

import pickle

def save_compressed_data(compressed_data, width, height, output_path):
    """Saves the compressed data and metadata to a binary file."""
    metadata = {
        'width': width,
        'height': height,
        'data': compressed_data
    }
    with open(output_path, 'wb') as f: # 'wb' for write binary
        pickle.dump(metadata, f)
    print(f"Custom compressed data saved to: {output_path}")

def load_compressed_data(input_path):
    """Loads the compressed data and metadata from the binary file."""
    with open(input_path, 'rb') as f: # 'rb' for read binary
        metadata = pickle.load(f)
    return metadata['data'], metadata['width'], metadata['height']

def custom_rle_decompress(compressed_data):
    """Reverts Run-Length Encoding to the original pixel data."""
    decompressed_data = []
    for count, pixel in compressed_data:
        decompressed_data.extend([pixel] * count)
    return decompressed_data

def pixel_sequence_to_image(pixels, width, height, output_path):
    """Converts a flat list of (R, G, B) tuples back to an image."""
    img = Image.new("RGB", (width, height))
    img.putdata(pixels)
    img.save(output_path)
    print(f"Decompressed image saved to: {output_path}")

# Assuming the functions defined above are available

# --- Setup ---
input_img = "smart_compressed.jpg"  # Use a simple image file with areas of solid color
compressed_file = "custom_compressed.bin"
decompressed_img = "custom_decompressed.png"

# --- Compression ---
# 1. Convert to sequence
pixels, w, h = image_to_pixel_sequence(input_img)
print(f"Original pixel count: {len(pixels)}")

# 2. Custom RLE compress
compressed_pixels = custom_rle_compress(pixels)
print(f"Compressed run count: {len(compressed_pixels)}")

# 3. Save to file
save_compressed_data(compressed_pixels, w, h, compressed_file)

# --- Decompression ---
# 1. Load from file
loaded_data, loaded_w, loaded_h = load_compressed_data(compressed_file)

# 2. Custom RLE decompress
decompressed_pixels = custom_rle_decompress(loaded_data)

# 3. Convert back to image
pixel_sequence_to_image(decompressed_pixels, loaded_w, loaded_h, decompressed_img)