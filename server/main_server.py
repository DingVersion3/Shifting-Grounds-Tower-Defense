import socket
import select
import json
import time
import sys
import os
import math

# ensure the server can see the root folder for the importing common constants
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.constants import *

class GameServer:
    def __init__(self):
        self.host = "0.0.0.0" # bind to all available local network adapters
        self.port = 5555

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # allows instant server restarts without "address already in use" errors
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen()
            self.server_socket.setblocking(False)
            print(f"[SERVER] Dedicated Host running on port {self.port}...")
        except Exception as e:
            print(f"[SERVER] Initialization failed: {e}")
            sys.exit(1)

        # track open network connections and active player structures
        self.sockets_list = [self.server_socket]
        self.clients = {}

        # placeholder for shared global simulation engine tracking metrics
        self.game_state = {"players": {}, "enemies": [], "projectiles": []}
        self.player_id_counter = 0

    def run(self):
        # auth global simulation cycle
        tick_rate = 60
        tick_time = 1.0 / tick_rate

        print("[SERVER] Tick loop started. Awaiting players...")

        while True:
            start_time = time.time()
            # gather all incoming network requests asyncd
            self.process_network_traffic()
            # update pyshical game states
            self.update_game_world(tick_time)
            # broadcast updated structural arrays to all connected players
            self.broadcast_game_state()

            # cap loop execution duration to stay syncd with the tick
            elapsed = time.time() - start_time
            if elapsed < tick_time:
                time.sleep(tick_time - elapsed)

    def process_network_traffic(self):
        # select reads our list of sockets and isolates only those with data waiting to be read
        read_sockets, _, exception_sockets = select.select(self.sockets_list, [], self.sockets_list, 0.1)
        for notified_socket in read_sockets:
            if notified_socket == self.server_socket:
                client_socket, client_address = self.server_socket.accept()
                client_socket.setblocking(False)

                self.player_id_counter += 1
                p_id = f"player_{self.player_id_counter}"

                self.sockets_list.append(client_socket)
                self.clients[client_socket] = p_id

                # setup default auth data entry inside our game world state
                self.game_state["players"][p_id] = {"x": 400, "y": 300, "health": 100}
                print(f"[SERVER] Handshake established with {client_address}. Assigned: {p_id}")

            else:
                try:
                    data = notified_socket.recv(4096).decode('utf-8')
                    if not data:
                        self.disconnect_client(notified_socket)
                        continue

                    p_id = self.clients[notified_socket]
                    player_input = json.loads(data.strip())

                    # store input instructions to process world updates
                    self.handle_player_input(p_id, player_input)

                except Exception:
                    self.disconnect_client(notified_socket)

        for notified_socket in exception_sockets:
            self.disconnect_client(notified_socket)

    def handle_player_input(self, player_id, input_data):
        # process actions from clients
        action_type = input_data.get("action")

        if action_type == "place_tower":
            grid_x = input_data.get("grid_x")
            grid_y = input_data.get("grid_y")
            tower_type = input_data.get("tower_type")

            new_tower = {
                "owner": player_id,
                "type": tower_type,
                "grid_x": grid_x,
                "grid_y": grid_y,
                "id": f"tower_{time.time()}"
            }
            self.game_state["projectiles"].append(new_tower)
            print(f"[SERVER] {player_id} built a {tower_type} at ({grid_x, grid_y})")

    def update_game_world(self, dt):
        enemies = self.game_state["enemies"]
        projectiles = self.game_state["projectiles"]

        # if this is the first tick, set up our arrays
        if not hasattr(self, "active towers"):
            self.active_towers = []

            for tower in self.active_towers:
                tower.update(dt, enemies, projectiles)

            for shot in list(projectiles):
                # find enemy in target queue
                target_enemy = next((e for e in enemies if e["id"] == shot["target_enemy_id"]), None)

                if target_enemy:
                    # move shot towards coords
                    dx = target_enemy["x"] - shot["x"]
                    dy = target_enemy["y"] - shot["y"]
                    distance = math.sqrt(dx**2 + dy**2)

                    if distance > 0.2:
                        shot["x"] += (dx / distance) * shot["speed"] * dt
                        shot["y"] += (dy / distance) * shot["speed"] * dt
                    else:
                        target_enemy["hp"] -= shot["damage"]
                        if shot in projectiles:
                            projectiles.remove(shot)

                        if target_enemy["hp"] <= 0:
                            if target_enemy in enemies:
                                enemies.remove(target_enemy)
                                print(f"[SERVER] Enemy neutralized. Giving out gold.")
                            else:
                                if shot in projectiles:
                                    projectiles.remove(shot)

            self.game_state["towers"] = [t.to_dict() for t in self.active_towers]


    def broadcast_game_state(self):
        if not self.clients:
            return
        
        payload = json.dumps(self.game_state) + "\n"
        encoded_payload = payload.encode('utf-8')

        for client_socket in list(self.clients.keys()):
            try:
                client_socket.sendall(encoded_payload)
            except Exception:
                self.disconnect_client(client_socket)

    def disconnect_client(self, client_socket):
        # safely tear down connection arrays when a player quits or drops out
        if client_socket in self.clients:
            p_id = self.clients[client_socket]
            print(f"[SERVER] Connection lost for {p_id}. Clearing vectors.")

            if p_id in self.game_state["players"]:
                del self.game_state["players"][p_id]

            del self.clients[client_socket]
            self.sockets_list.remove(client_socket)
            client_socket.close()

if __name__ == "__main__":
    server = GameServer()
    server.run()
