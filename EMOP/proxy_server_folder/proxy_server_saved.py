# proxy server folder/proxy_server.py
import socket
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from mop_protocol import (
    send_mop_message, receive_mop_message,
    MSG_FETCH, MSG_OBJECT, MSG_FAIL,
    SOURCE_PROXY, STATUS_OK, STATUS_BAD_GATEWAY
)

PROXY_HOST = "0.0.0.0"
PROXY_PORT = 9091       
ORIGIN_HOST = "100.122.19.68"
ORIGIN_PORT = 9090      
PSK = b'0123456789abcdef0123456789abcdef'

# Proxy root directory for checking and saving cached files
PROXY_ROOT = os.path.dirname(os.path.abspath(__file__))

def forward_request_to_origin(msg_type: int, payload: bytes):
    try:
        origin_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        origin_sock.connect((ORIGIN_HOST, ORIGIN_PORT))
        send_mop_message(origin_sock, msg_type, outcome=0, source=SOURCE_PROXY, payload=payload, psk=PSK)
        response = receive_mop_message(origin_sock, psk=PSK)
        origin_sock.close()
        return response
    except Exception as e:
        print(f"    [!] Failed to reach Origin: {e}")
        return None

def run_proxy():
    proxy_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy_sock.bind((PROXY_HOST, PROXY_PORT))
    proxy_sock.listen(1)
    
    print(f"[*] Pure Filesystem Proxy Server running in: {PROXY_ROOT}")
    print(f"[*] Listening on {PROXY_HOST}:{PROXY_PORT}...")

    while True:
        client_conn, addr = proxy_sock.accept()
        try:
            while True:
                request = receive_mop_message(client_conn, psk=PSK)
                msg_type = request["msg_type"]
                payload = request["payload"]
                
                if msg_type == MSG_FETCH:
                    filename = payload.decode('utf-8')
                    filepath = os.path.join(PROXY_ROOT, filename)
                    
                    # 1. Pure Filesystem Cache HIT Check
                    if os.path.isfile(filepath):
                        print(f"\n -> [Cache HIT] Found '{filename}' on Proxy disk! Serving locally.")
                        with open(filepath, 'rb') as f:
                            cached_data = f.read()
                        
                        # Served directly from proxy folder -> Source: 2 (PROXY)
                        send_mop_message(client_conn, MSG_OBJECT, outcome=STATUS_OK, source=SOURCE_PROXY, payload=cached_data, psk=PSK)
                    
                    # 2. Pure Filesystem Cache MISS Check
                    else:
                        print(f"\n -> [Cache MISS] '{filename}' not found on Proxy disk. Fetching from Origin...")
                        origin_response = forward_request_to_origin(msg_type, payload)
                        
                        if origin_response and origin_response["outcome"] == STATUS_OK:
                            print(f"    [Cache STORE] Saving '{filename}' to Proxy folder.")
                            
                            # Write file directly to the proxy folder on disk
                            with open(filepath, 'wb') as f:
                                f.write(origin_response["payload"])
                                
                            # Freshly fetched from origin -> Source: 1 (ORIGIN)
                            send_mop_message(
                                client_conn, 
                                MSG_OBJECT, 
                                outcome=STATUS_OK, 
                                source=origin_response["source"], 
                                payload=origin_response["payload"], 
                                psk=PSK
                            )
                        else:
                            fail_payload = origin_response["payload"] if origin_response else b"Origin Unreachable"
                            fail_outcome = origin_response["outcome"] if origin_response else STATUS_BAD_GATEWAY
                            send_mop_message(client_conn, MSG_FAIL, outcome=fail_outcome, source=SOURCE_PROXY, payload=fail_payload, psk=PSK)
                
                else:
                    # Transparent pass-through for LIST, PUT, UNCHANGED, FAIL
                    origin_response = forward_request_to_origin(msg_type, payload)
                    if origin_response:
                        send_mop_message(client_conn, origin_response["msg_type"], outcome=origin_response["outcome"], source=origin_response["source"], payload=origin_response["payload"], psk=PSK)
                    else:
                        send_mop_message(client_conn, MSG_FAIL, outcome=STATUS_BAD_GATEWAY, source=SOURCE_PROXY, payload=b"Bad Gateway", psk=PSK)
                        
        except ConnectionError:
            pass
        except Exception as e:
            print(f"[-] Error: {e}")
        finally:
            client_conn.close()

if __name__ == "__main__":
    run_proxy()