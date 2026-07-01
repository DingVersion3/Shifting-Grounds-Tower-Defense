import socket
import json

class NetworkClient:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 5555
        self.is_connected = False
        self.player_id = None
        self.side = None
        self.map_seed = None
        self.recv_buffer = ""

    def start_connection(self, ip_address):
        try:
            print(f"[NETWORK] Connecting to server at {ip_address}:{self.port}...")
            self.client.connect((ip_address, self.port))

            # Read handshake while still blocking
            raw = self.client.recv(4096).decode('utf-8')
            first_message = raw.strip().split('\n')[0]
            handshake = json.loads(first_message)

            self.player_id = handshake["player_id"]
            self.side = handshake["side"]
            self.map_seed = handshake["map_seed"]

            # Now switch to non-blocking for the game loop
            self.client.setblocking(False)
            self.is_connected = True
            print(f"[NETWORK] Connected. ID: {self.player_id}, Side: {self.side}, Seed: {self.map_seed}")

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
        if not self.is_connected:
            return None
        latest_state = None
        try:
            while True:
                raw_data = self.client.recv(8192).decode('utf-8')
                if not raw_data:
                    break
                self.recv_buffer += raw_data
                while '\n' in self.recv_buffer:
                    line, self.recv_buffer = self.recv_buffer.split('\n', 1)
                    if line:
                        try:
                            latest_state = json.loads(line)
                        except Exception as e:
                            print(f"DEBUG json parse fail: {e}")
        except BlockingIOError:
            pass
        except Exception as e:
            print(f"[NETWORK] Connection lost from the host: {e}")
            self.is_connected = False
        return latest_state
        
            