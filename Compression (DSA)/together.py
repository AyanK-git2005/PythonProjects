import FreeSimpleGUI as sg
import os
from gemmy import smart_downsample_fixed_output

layout = [
    [sg.Text('File to Compress:', size=(13,1)),
     sg.Input(key = '-INPUT-FILE-', size = (50,1)),
     sg.FileBrowse(file_types=(("All Files", "*.*"),))],

     [sg.Text('Output Folder:', size=(13, 1)),
      sg.Input(key = '-OUTPUT-DIR-', size = (50,1), default_text= os.getcwd()),
      sg.FolderBrowse()],

      [sg.Button('Compress', size = (10,1)),
       sg.Text('', size = (50,1), key = '-STATUS-')]
]

window = sg.Window('Simple File Compressor', layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == 'Compress':
        input_file = values['-INPUT-FILE-']
        output_folder = values['-OUTPUT-DIR-']
        #----------
        if not input_file:
            window['-STATUS-'].update('❌ Error: Please select a file first.', text_color='red')
            continue

        #--------------------
        OUTPUT_FILE = 'compressed.jpg'
        smart_downsample_fixed_output(input_file, OUTPUT_FILE, block_size=8, variance_threshold=600)
        #--------------------

        window['-STATUS-'].update(f'✅ Compressing {os.path.basename(input_file)}...', text_color='green')

window.close()