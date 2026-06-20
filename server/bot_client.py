import socket
import json
import time
import random

def run_ai_bot():
    server_ip = "127.0.0.1"
    port = 5555
    bot_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    GRID_COLS = 16
    GRID_ROWS = 12
    midpoint = GRID_COLS // 2

    print("[AI BOT] Attempting to connect to local game server...")
    try:
        bot_socket.connect((server_ip, port))
        print("[AI BOT] Connected successfully! Operating as Player 2.")
    except Exception as e:
        print(f"[AI BOT] Connection failed: {e}. Is main_server.py running?")
        return
    
    built_positions = set()

    print("[AI BOT] Entering automated gameplay loop. Placing towers...")
    try:
        while True:
            time.sleep(4.0)
            rand_x = random.randint(midpoint, GRID_COLS - 1)
            rand_y = random.randint(midpoint, GRID_ROWS - 1)

            if (rand_x, rand_y) not in built_positions:
                action_packet = {
                    "action": "place_tower",
                    "tower_type": "Standard",
                    "grid_x": rand_x,
                    "grid_y": rand_y
                }

                payload = json.dumps(action_packet) + "\n"
                bot_socket.sendall(payload.encode('utf-8'))

                built_positions.add((rand_x, rand_y))
                print(f"[AI BOT] Request sent to place tower at {rand_x}, {rand_y}")

            try:
                bot_socket.setblocking(False)
                bot_socket.recv(4096)
            except BlockingIOError:
                pass

    except KeyboardInterrupt:
        print("[AI BOT] Disconnecting")
    finally:
        bot_socket.close()

if __name__ == "__main__":
    run_ai_bot()