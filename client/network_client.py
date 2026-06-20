import socket
import json

class NetworkClient:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 5555
        self.is_connected = False
        self.player_id = None

    def start_connection(self, ip_address):
        try:
            print(f"[NETWORK] Connecting to server at {ip_address}:{self.port}...")

            # establish internet connection handshake
            self.client.connect((ip_address, self.port))

            # turn off blocking mode so our window never freezes
            self.client.setblocking(False)

            self.is_connected = True
            print("[NETWORK] Successfully connected to server!")

        except Exception as e:
            print(f"[NETWORK] Connection failed: {e}")
            self.is_connected = False

    def send_data(self, data_dict):
        # convert python dict of movements/actions to json data and transmit it
        if not self.is_connected:
            return
        try:
            json_string = json.dumps(data_dict) + "\n"
            self.client.sendall(json_string.encode('utf-8'))
        except Exception as e:
            print(f"[NETWORK] Transmission error: {e}")
            self.is_connected = False

    def update(self):
        # pumps network data, listens for server broadcasts without pausing the main loop
        if not self.is_connected:
            return None
        try:
            # peek inside the network stream buffer
            raw_data = self.client.recv(4096).decode('utf-8')
            if not raw_data:
                return None
            # decode incoming string payload back to python
            game_state = json.loads(raw_data.strip())
            return game_state
        except BlockingIOError:
            # server hasnt sent any new packets during the specific 1/60th of a second frame
            return None
        except Exception as e:
            print(f"[NETWORK] Connection lost from the host: {e}")
            self.is_connected = False
            return None
        
            