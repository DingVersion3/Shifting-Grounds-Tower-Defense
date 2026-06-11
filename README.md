# Shifting Grounds Tower Defense v 0.1.2

A procedurally generated tower defense game built with Python and Pygame.

Every game generates a new map with a unique path for enemies to follow, so no two playthroughs are the same.

## Artwork
- Im currently using free source assets from https://kenney.nl/assets/tower-defense-top-down 
- If interested in showing the artist some love you can suport them here https://kenney.nl/donate

## How to Play

- Press your S key or click the Start button to start the game at the main menu
- Enemies spawn in waves and follow the path from the start (green x) to the end (black x)
- Click a tower in the shop bar at the bottom to select it, then click an empty tile to place it
- Towers automatically attack enemies in range
- Earn gold by killing enemies and spend it on towers
- You have 3 lives — each enemy that reaches the end costs you one
- Survive as long as possible. You can press R on the game over screen to restart

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

## Planned Work

- Better looking Main Menu
    - Game instance running as the menus background
    - cleaner looking buttons
    - cleaner title text
- Gameplay adjustments
    - Fine tuning numbers
    - Adjustments are hard considering paths are randomly generated and theres going to be times where its too easy or too hard. Trying to find a balance between how often the extremes happen
- Multiplayer
    - How will multiplayer work? Great question, I'm not sure yet. I'm thinking of just splitting the map in half and each player gets a half to defend. Not sure if using randomly generated paths would be a good idea or not in this scenario so I might have to spend some time creating maps. Unsure of the direction at this time.
    

## Suggestions 

- I currently don't have a system for suggestions however you're welcome to put your suggestions in the boot.dev personal project thread i have going here https://discord.com/channels/551921866173054977/1507828092989734982

- Thanks again for taking the time to play my game! Much love to you!

## Patch Notes v 0.1.1

- Added a Main Menu(planning on beautifying this menu at a later time)
- Adjusted the gameplay loop to create more tense moments. This means the randomly generated paths will make it impossible to beat wave 1 sometimes, looking into making the gameplay loop a bit more tense and keeping it rewarding without situations where you're forced to fail
- You can no longer place towers on top of other towers

## Patch Notes v 0.1.2
- Small adjustments to the main menu logic, also added a background image. Currently looking into having a game instance running as the background. 

## Patch Notes v 0.1.3
- Added Tanks! The won't spawn until at least wave 20, higher health enemies that move slower.
- Bug Fix: Enemies now correctly face the direction they are moving along the path