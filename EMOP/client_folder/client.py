# client folder/client.py
import FreeSimpleGUI as sg
import socket
import sys
import os
import threading

# Allow importing from the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from EMOP import (
    send_mop_message, receive_mop_message,
    MSG_LIST, MSG_FETCH, MSG_PUT, MSG_UNCHANGED, MSG_FAIL,
    SOURCE_ORIGIN, STATUS_OK
)

HOST = "100.98.59.20" # Tailscale IP of Proxy (or 127.0.0.1 for local testing)
PORT = 9091 
PSK = b'0123456789abcdef0123456789abcdef'

CLIENT_ROOT = os.path.dirname(os.path.abspath(__file__))

class MOPClientGUI:
    def __init__(self):
        self.persistent_sock = None # Tracks active persistent socket

        layout = [
            [sg.Text("Message Type:", size=(20, 1)), 
             sg.Combo(["LIST", "FETCH", "PUT", "UNCHANGED", "FAIL"], default_value="FETCH", key="-MSG_TYPE-", readonly=True, enable_events=True, size=(28, 1))],
            
            [sg.Text("Filename (Fetch/Check):", size=(20, 1)), 
             sg.Input("b.txt", key="-FILENAME-", size=(30, 1))],
            
            [sg.Text("File to Upload (PUT):", size=(20, 1)), 
             sg.Input(key="-FILEPATH-", size=(30, 1), disabled=True), 
             sg.FileBrowse("Browse", key="-BROWSE-", disabled=True)],
            
            [sg.Checkbox("Enable Persistent Connection Mode", default=False, key="-PERSISTENT-", enable_events=True),
             sg.Push(),
             sg.Button("Close Persistent Socket", key="-DISCONNECT-", button_color=("black", "orange"), disabled=True)],
            
            [sg.Push(), sg.Button("Send Request", key="-SEND-", button_color=("black", "lightblue")), sg.Push()],
            
            [sg.Text("Transfer Progress:", size=(15, 1)),
             sg.ProgressBar(100, orientation='h', size=(42, 18), key="-PROGRESS-")],
            
            [sg.Multiline(size=(78, 15), key="-CONSOLE-", disabled=True, autoscroll=True)]
        ]

        self.window = sg.Window("MOP Protocol Client (Persistent & Non-Persistent)", layout, finalize=True)

    def log(self, text):
        self.window.write_event_value("-LOG-", text)

    def update_progress(self, value):
        self.window.write_event_value("-UPDATE_PROG-", value)

    def toggle_inputs(self, selection):
        if selection == "PUT":
            self.window["-FILENAME-"].update(disabled=True)
            self.window["-BROWSE-"].update(disabled=False)
        elif selection in ["FETCH", "UNCHANGED"]:
            self.window["-FILENAME-"].update(disabled=False)
            self.window["-BROWSE-"].update(disabled=True)
        else:
            self.window["-FILENAME-"].update(disabled=True)
            self.window["-BROWSE-"].update(disabled=True)

    def toggle_persistent_mode(self, is_persistent):
        if not is_persistent and self.persistent_sock:
            self.close_persistent_socket()

    def close_persistent_socket(self):
        if self.persistent_sock:
            try:
                self.persistent_sock.close()
            except:
                pass
            self.persistent_sock = None
            self.log("[*] Persistent TCP connection closed manually.")
        self.window.write_event_value("-DISCONNECT_STATE-", True)

    def send_request(self, values):
        msg_str = values["-MSG_TYPE-"]
        payload = b""
        
        msg_mapping = {"LIST": MSG_LIST, "FETCH": MSG_FETCH, "PUT": MSG_PUT, "UNCHANGED": MSG_UNCHANGED, "FAIL": MSG_FAIL}
        msg_type = msg_mapping[msg_str]

        target_filename = ""
        if msg_str in ["FETCH", "UNCHANGED"]:
            target_filename = values["-FILENAME-"].strip()
            if not target_filename:
                self.window.write_event_value("-ERROR-", "Filename cannot be empty.")
                return
            payload = target_filename.encode('utf-8')
        elif msg_str == "PUT":
            filepath = values["-FILEPATH-"]
            if not os.path.exists(filepath):
                self.window.write_event_value("-ERROR-", "Invalid file selected.")
                return
            filename = os.path.basename(filepath).encode('utf-8')
            
            # Read file in chunks to reflect progress without freezing
            file_size = os.path.getsize(filepath)
            file_data = bytearray()
            chunk_size = 65536 # 64KB chunks
            bytes_read = 0
            
            self.update_progress(0)
            with open(filepath, 'rb') as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    file_data.extend(chunk)
                    bytes_read += len(chunk)
                    if file_size > 0:
                        # Scale file reading progress up to 50%
                        self.update_progress(int((bytes_read / file_size) * 50))
                        
            payload = bytes([len(filename)]) + filename + bytes(file_data)
        elif msg_str == "FAIL":
            payload = b"Manual Client Error Test"

        is_persistent = values["-PERSISTENT-"]
        mode_str = "PERSISTENT" if is_persistent else "NON-PERSISTENT"
        self.log(f"--- Sending {msg_str} [{mode_str}] to Proxy ---")

        self.window.write_event_value("-SEND_STATE-", True)
        if msg_str != "PUT":
            self.update_progress(10)

        try:
            # Determine socket to use
            if is_persistent:
                if self.persistent_sock is None:
                    self.log("[*] Opening new persistent TCP connection handshake...")
                    self.persistent_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.persistent_sock.connect((HOST, PORT))
                    self.window.write_event_value("-DISCONNECT_STATE-", False)
                sock = self.persistent_sock
            else:
                # Non-persistent: Fresh socket per request
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((HOST, PORT))

            if msg_str == "PUT":
                self.update_progress(60)
            else:
                self.update_progress(40)

            # Send message and receive response
            send_mop_message(sock, msg_type, outcome=0, source=SOURCE_ORIGIN, payload=payload, psk=PSK)
            
            if msg_str == "PUT":
                self.update_progress(85)
            else:
                self.update_progress(70)
                
            response = receive_mop_message(sock, psk=PSK)
            
            self.log(f"[Response] Type: {response['msg_type']}, Outcome: {response['outcome']}, Source: {response['source']}")
            
            resp_payload = response['payload']
            
            if msg_str == "FETCH" and response['outcome'] == STATUS_OK:
                save_path = os.path.join(CLIENT_ROOT, target_filename)
                with open(save_path, 'wb') as f:
                    f.write(resp_payload)
                self.log(f"[+] Saved fetched file '{target_filename}' into client folder!")

            if len(resp_payload) > 500:
                self.log(f"[Payload] {len(resp_payload)} bytes of binary data received.")
            else:
                try:
                    self.log(f"[Payload Text] {resp_payload.decode('utf-8')}")
                except:
                    self.log(f"[Payload Hex] {resp_payload.hex()}")

            # Close socket ONLY if non-persistent
            if not is_persistent:
                sock.close()
                self.log("[*] Non-persistent socket closed automatically.")
            else:
                self.log("[*] Persistent socket remains OPEN for next request.")

            self.update_progress(100)

        except Exception as e:
            self.log(f"[!] Network Error: {e}")
            self.update_progress(0)
            if is_persistent:
                self.close_persistent_socket()
        finally:
            self.window.write_event_value("-SEND_STATE-", False)

    def run(self):
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED:
                if self.persistent_sock:
                    try:
                        self.persistent_sock.close()
                    except:
                        pass
                break
            elif event == "-MSG_TYPE-":
                self.toggle_inputs(values["-MSG_TYPE-"])
            elif event == "-PERSISTENT-":
                self.toggle_persistent_mode(values["-PERSISTENT-"])
            elif event == "-DISCONNECT-":
                self.close_persistent_socket()
            elif event == "-SEND-":
                # Run network transfer in a separate thread so the GUI stays responsive
                threading.Thread(target=self.send_request, args=(values,), daemon=True).start()
            elif event == "-LOG-":
                self.window["-CONSOLE-"].update(values["-LOG-"] + "\n", append=True)
            elif event == "-UPDATE_PROG-":
                self.window["-PROGRESS-"].update(values["-UPDATE_PROG-"])
            elif event == "-DISCONNECT_STATE-":
                self.window["-DISCONNECT-"].update(disabled=values["-DISCONNECT_STATE-"])
            elif event == "-SEND_STATE-":
                self.window["-SEND-"].update(disabled=values["-SEND_STATE-"])
            elif event == "-ERROR-":
                sg.popup_error(values["-ERROR-"], title="Error")

        self.window.close()

if __name__ == "__main__":
    app = MOPClientGUI()
    app.run()