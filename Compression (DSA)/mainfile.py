import FreeSimpleGUI as sg
import os # Useful for file operations

# Define the layout using a list of lists (each inner list is a row)
layout = [
    # Row 1: File selection
    [sg.Text('File to Compress:', size=(15, 1)), 
     sg.Input(key='-INPUT-FILE-'), 
     sg.FileBrowse(file_types=(("All Files", "*.*"),))],
    
    # Row 2: Destination folder selection
    [sg.Text('Output Folder:', size=(15, 1)), 
     sg.Input(key='-OUTPUT-FOLDER-', default_text=os.getcwd()), # Use current directory as default
     sg.FolderBrowse()],
    
    # Row 3: Action Button
    [sg.Button('Compress', size=(15, 1), bind_return_key=True)], # bind_return_key allows pressing Enter
    
    # Row 4: Status/Output Text
    [sg.Text('', size=(50, 1), key='-STATUS-')]
]

# Create the Window
window = sg.Window('Simple File Compressor', layout)

# Event Loop to process events and get the values of the inputs
while True:
    event, values = window.read()

    # Part 1: Handle Window Closure
    if event == sg.WIN_CLOSED:
        break
    
    # Part 2: Handle the 'Compress' Button Click
    if event == 'Compress':
        input_file = values['-INPUT-FILE-']
        output_folder = values['-OUTPUT-FOLDER-']
        
        # --- YOUR FILE COMPRESSION LOGIC GOES HERE ---
        
        if not input_file:
            window['-STATUS-'].update('❌ Error: Please select a file first.', text_color='red')
            continue
            
        # Example of calling your compression function:
        # success = compress_file(input_file, output_folder) 
        
        # For demonstration, we'll just show success:
        window['-STATUS-'].update(f'✅ Compressing {os.path.basename(input_file)}...', text_color='green')

# Close the window
window.close()