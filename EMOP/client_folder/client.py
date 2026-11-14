# client folder/client.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import socket
import sys
import os

# Allow importing from the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from mop_protocol import (
    send_mop_message, receive_mop_message,
    MSG_LIST, MSG_FETCH, MSG_PUT, MSG_UNCHANGED, MSG_FAIL,
    SOURCE_ORIGIN, STATUS_OK
)

HOST = "127.0.0.1"
PORT = 9091 # Pointing to Proxy
PSK = b'0123456789abcdef0123456789abcdef'

# Define current folder as the client root for saving files
CLIENT_ROOT = os.path.dirname(os.path.abspath(__file__))

class MOPClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MOP Protocol Client")
        self.root.geometry("600x520")
        
        # Message Type Selection
        tk.Label(root, text="Message Type:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.msg_type_var = tk.StringVar(value="FETCH")
        self.type_dropdown = ttk.Combobox(root, textvariable=self.msg_type_var, state="readonly", 
                                          values=["LIST", "FETCH", "PUT", "UNCHANGED", "FAIL"])
        self.type_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.type_dropdown.bind("<<ComboboxSelected>>", self.toggle_inputs)

        # Filename Input (For FETCH)
        tk.Label(root, text="Filename (Fetch/Check):").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.filename_entry = tk.Entry(root, width=30)
        self.filename_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.filename_entry.insert(0, "b.txt")

        # File Picker (For PUT)
        tk.Label(root, text="File to Upload (PUT):").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.filepath_var = tk.StringVar()
        self.filepath_entry = tk.Entry(root, textvariable=self.filepath_var, width=30, state="disabled")
        self.filepath_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        self.browse_btn = tk.Button(root, text="Browse", command=self.browse_file, state="disabled")
        self.browse_btn.grid(row=2, column=2, padx=10, pady=10)

        # Send Button
        self.send_btn = tk.Button(root, text="Send Request", bg="lightblue", command=self.send_request)
        self.send_btn.grid(row=3, column=0, columnspan=3, pady=15)

        # Console Output
        self.console = scrolledtext.ScrolledText(root, width=72, height=14, state="disabled")
        self.console.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

    def log(self, text):
        self.console.config(state="normal")
        self.console.insert(tk.END, text + "\n")
        self.console.see(tk.END)
        self.console.config(state="disabled")

    def toggle_inputs(self, event=None):
        selection = self.msg_type_var.get()
        if selection == "PUT":
            self.filename_entry.config(state="disabled")
            self.browse_btn.config(state="normal")
        elif selection in ["FETCH", "UNCHANGED"]:
            self.filename_entry.config(state="normal")
            self.browse_btn.config(state="disabled")
        else: # LIST, FAIL
            self.filename_entry.config(state="disabled")
            self.browse_btn.config(state="disabled")

    def browse_file(self):
        filepath = filedialog.askopenfilename(title="Select File to Upload")
        if filepath: self.filepath_var.set(filepath)

    def send_request(self):
        msg_str = self.msg_type_var.get()
        payload = b""
        
        msg_mapping = {"LIST": MSG_LIST, "FETCH": MSG_FETCH, "PUT": MSG_PUT, "UNCHANGED": MSG_UNCHANGED, "FAIL": MSG_FAIL}
        msg_type = msg_mapping[msg_str]

        target_filename = ""
        if msg_str in ["FETCH", "UNCHANGED"]:
            target_filename = self.filename_entry.get().strip()
            if not target_filename: return messagebox.showerror("Error", "Filename cannot be empty.")
            payload = target_filename.encode('utf-8')
        elif msg_str == "PUT":
            filepath = self.filepath_var.get()
            if not os.path.exists(filepath): return messagebox.showerror("Error", "Invalid file selected.")
            filename = os.path.basename(filepath).encode('utf-8')
            with open(filepath, 'rb') as f:
                file_data = f.read()
            payload = bytes([len(filename)]) + filename + file_data
        elif msg_str == "FAIL":
            payload = b"Manual Client Error Test"

        self.log(f"--- Sending {msg_str} to Proxy ({PORT}) ---")
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            send_mop_message(s, msg_type, outcome=0, source=SOURCE_ORIGIN, payload=payload, psk=PSK)
            
            response = receive_mop_message(s, psk=PSK)
            self.log(f"[Response] Type: {response['msg_type']}, Outcome: {response['outcome']}, Source: {response['source']}")
            
            resp_payload = response['payload']
            
            # --- NEW: Automatically save fetched file to client folder ---
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
            s.close()
        except Exception as e:
            self.log(f"[!] Network Error: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MOPClientGUI(root)
    root.mainloop()