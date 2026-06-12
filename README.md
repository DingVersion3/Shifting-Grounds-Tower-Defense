# Shifting Grounds Tower Defense v 0.2.1

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
- **JT Tower (1,000g)** — splash damage, hits all enemies in range
- **Laser Tower (10,000g)** — fast fire rate, high damage, save up for these

## Setup

```bash
git clone https://github.com/DingVersion3/Shifting-Grounds-Tower-Defense
cd Shifting-Grounds-Tower-Defense
python3.14 -m venv .venv
source .venv/bin/activate
pip install pygame-ce
python main.py
```

## Requirements

- Python 3.14+
- Pygame-CE 2.5+

## Planned Work

- Better looking Main Menu
    - Game instance running as the menus background
    - cleaner looking buttons
    - cleaner title text
    - settings page?
- Gameplay adjustments
    - Scenary Changes based on wave number(randomly chooses a theme that isn't the one you're currently or last used) while keeping the same path and towers up
    - Fine tuning numbers
    - Adjustments are hard considering paths are randomly generated and theres going to be times where its too easy or too hard. Trying to find a balance between how often the extremes happen
    - Update UI to use a matching text font, beautify UI
    - Add more Towers(Nukes, Sniper, Laser Sniper?) Would love suggestions on this!
    - Create multiple map layouts that the "AI" can create
    - Create Tower bases and have towers rotate towards the target they are shooting
    - find assets to beautify the map(trees, buildings, bushes, etc)
- Multiplayer
    - Initial thought is each player owns a side of the map where you can place towers and generate units to send at the opponent. If you're old like me and played "Age of War", then im thinking something like that but just multiplayer instead of going against an "ai".
    - How will multiplayer work? Great question, I'm not sure yet. I'm thinking of just splitting the map in half and each player gets a half to defend. Not sure if using randomly generated paths would be a good idea or not in this scenario so I might have to spend some time creating maps. Unsure of the direction at this time.
    

## Known Bugs
- Restarting currently brings you back to the main menu instead of creating a new game state
- Enemies will randomly cut corners going along the path(edge case)

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

## Patch Notes v 0.2.0
- Added Airplanes!! Move fast but dont have as much health, won't spawn until at least wave 50. Decided against airplanes doing towers to your turrets, would have to add the ability to the other enemies and i dont want that style of gameplay in single player. Could potentially do something like that with multiplayer. 
- Update assets for enemies based on the wave youre on, visually shows enemies getting stronger at various points of your run, enemies will stop changing after wave 75
- Update Game UI Bar to use assets for numbers and $
- Starting Player Money is now $300

## Patch Notes v 0.2.1
- JT Towers and Laser Towers are now cheaper, planning to add more expensive turrets in the future.
- Updated Game Engine to pygame-ce, this allowed me to update to python 3.14. Please be sure to check how to set it up again.