import FreeSimpleGUI as sg              # pip install FreeSimpleGUI
import numpy as np                      # pip install numpy
from PIL import Image                   # pip install pillow
import os
# from gemmy import smart_downsample_fixed_output

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

BLOCK_SIZES = ['2', '4', '8', '16']
DEFAULT_BLOCK_SIZE = '4'
COMPRESSION_MIN = 100
COMPRESSION_MAX = 5000
COMPRESSION_DEFAULT = 1500

layout = [
    [sg.Text('Image to Compress:', size=(15,1)),
     sg.Input(key = '-INPUT-FILE-', size = (50,1)),
     sg.FileBrowse(file_types=(("All Files", "*.*"),))],

     [sg.Text('Save to Folder:', size=(15, 1)),
      sg.Input(key = '-OUTPUT-DIR-', size = (50,1), default_text= os.getcwd()),
      sg.FolderBrowse()],

      [sg.Text('\nVariance Threshold:', size=(15, 2)),
        sg.Slider(range=(COMPRESSION_MIN, COMPRESSION_MAX),
            default_value=COMPRESSION_DEFAULT,
            orientation='horizontal',
            size=(46, 15),
            key='-SLIDER-STRENGTH-',
            enable_events=True,
            tooltip='Set the variance threshold for smart downsampling.')],
        
        [sg.Text('Block Size (N x N):', size=(15, 1)),
        sg.Combo(BLOCK_SIZES,
            default_value=DEFAULT_BLOCK_SIZE,
            key='-BLOCK-SIZE-',
            readonly=True,  # Prevents users from typing invalid values
            tooltip='Size of the pixel block for variance check (e.g., 4 means 4x4).'),
        sg.Text('(Pixels to average if similar)', size=(25, 1))],

       [sg.Button('Compress', size = (10,1)),
        sg.Text('', size = (30,1), key = '-STATUS-')],

        [sg.ProgressBar(key='-PROGRESS-',
                        max_value=100,
                        orientation='horizontal',
                        size=(50,1),
                        bar_color='green')]
]

window = sg.Window('Simple File Compressor', layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == '-SLIDER-STRENGTH-':
        current_val = int(values['-SLIDER-STRENGTH-'])
        window['-SLIDER-VALUE-DISPLAY-'].update(f'Current: {current_val}')
    
    if event == 'Compress':
        input_file = values['-INPUT-FILE-']
        output_folder = values['-OUTPUT-DIR-']
        #----------
        if not input_file:
            window['-STATUS-'].update('❌ Error: Please select a file first.', text_color='red')
            continue

        block_size = int(values['-BLOCK-SIZE-'])
        variance_threshold = int(values['-SLIDER-STRENGTH-'])

        window['-STATUS-'].update(f'Compressing {os.path.basename(input_file)}...', text_color='yellow')
        #--------------------
        OUTPUT_FILE = 'compressed.jpg'
        smart_downsample_fixed_output(input_file, OUTPUT_FILE, block_size, variance_threshold)
        #--------------------

        window['-STATUS-'].update(f'✅ Compression of {os.path.basename(input_file)} Finished!', text_color='green')

window.close()