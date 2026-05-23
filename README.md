# Shifting Grounds Tower Defense

A procedurally generated tower defense game built with Python and Pygame.

Every game generates a new map with a unique path for enemies to follow, so no two playthroughs are the same.

## How to Play

- Enemies spawn in waves and follow the path from the start (green x) to the end (black x)
- Click a tower in the shop bar at the bottom to select it, then click an empty tile to place it
- Towers automatically attack enemies in range
- Earn gold by killing enemies and spend it on towers
- You have 3 lives — each enemy that reaches the end costs you one
- Survive all waves to win, or press R on the game over screen to restart

## Tower Types

- **Basic Tower (100g)** — balanced damage and fire rate
- **JT Tower (10,000g)** — splash damage, hits all enemies in range
- **Laser Tower (100,000g)** — fast fire rate, high damage, save up for these

## Setup

```bash
git clone https://github.com/DingVersion3/Shifting-Grounds-Tower-Defense
cd Shifting-Grounds-Tower-Defense
python -m venv .venv
source .venv/bin/activate
pip install pygame
python main.py
```

## Requirements

- Python 3.12+
- Pygame 2.6+