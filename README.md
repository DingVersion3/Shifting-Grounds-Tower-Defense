# Shifting Grounds Tower Defense v 0.1.1

A procedurally generated tower defense game built with Python and Pygame.

Every game generates a new map with a unique path for enemies to follow, so no two playthroughs are the same.

## Artwork
- Im currently using free source assets from https://kenney.nl/assets/tower-defense-top-down 
- If interested in showing the artist some love you can suport them here https://kenney.nl/donate

## How to Play

- Press your S key to start the game at the main menu
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

## Patch Notes

- Added a Main Menu(planning on beautifying this menu at a later time)
- Adjusted the gameplay loop to create more tense moments. This means the randomly generated paths will make it impossible to beat wave 1 sometimes, looking into making the gameplay loop a bit more tense and keeping it rewarding without situations where you're forced to fail
- You can no longer place towers on top of other towers

## Planned Work

- Better looking Main Menu
- Gameplay adjustments
- Multiplayer

## Suggestions 

- I currently don't have a system for suggestions however you're welcome to put your suggestions in the boot.dev personal project thread i have going here https://discord.com/channels/551921866173054977/1507828092989734982

- Thanks again for taking the time to play my game! Much love to you!