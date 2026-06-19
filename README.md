# Shifting Grounds Tower Defense v 0.3.0

A procedurally generated tower defense game built with Python and Pygame.

Every game generates a new map with a unique path for enemies to follow, so no two playthroughs are the same.

## Artwork
- Im currently using free source assets from:
    1. https://kenney.nl/assets/tower-defense-top-down
    2. https://kenney.nl/assets/kenney-fonts
- If interested in showing the artist some love you can suport them here:
    1. https://kenney.nl/donate

## How to Play

- Press your S key or click the Start button to start the game at the main menu
- Enemies spawn in waves and follow the path from the start (square symbol) to the end (x symbol)
- Click a tower in the shop bar at the bottom to select it, then click an empty tile to place it
- Towers automatically attack enemies in range
- Earn gold by killing enemies and spend it on towers
- You have 3 lives — each enemy that reaches the end costs you one
- Survive as long as possible. You can press R on the game over screen to restart

## Tower Types

- **Basic Tower (100g)** — balanced damage and fire rate
- **JT Tower (1,000g)** — splash damage, hits all enemies in range
- **Laser Tower (10,000g)** — fast fire rate, high damage, save up for these
- **Sniper Tower (100,000g)** - long range, slow rate of fire, delete enemies they hit

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
    - clean looking buttons
- Gameplay adjustments
    - beautify UI
    - find assets to beautify the map(trees, buildings, bushes, etc)
- Multiplayer
    - Initial thought is each player owns a side of the map where you can place towers and generate units to send at the opponent. If you're old like me and played "Age of War", then im thinking something like that but just multiplayer instead of going against an "ai".
    - How will multiplayer work? Great question, I'm not sure yet. I'm thinking of just splitting the map in half and each player gets a half to defend. Not sure if using randomly generated paths would be a good idea or not in this scenario so I might have to spend some time creating maps. Unsure of the direction at this time.
    

## Known Bugs
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

## Patch Notes v 0.2.2
- Settings page added. Fullscreen and windowed are now supported.
- Updated organization of Tower code(all tower types now live in tower.py)
- Added a Pause Feature! currently cant quit the game while paused unless you ctrl + c from your console (WIP)
- Can press "q" to quit the game when at the game over screen
- Updated Tower assets, some logic still needed for it to all look clean

## Patch Notes v 0.2.3
- Updated fonts in Main Menu, UI and Game Over screens
- Towers and Tower shots now rotate towrds enemies correctly
- Updated Basic Towers to use a different shot asset
- Press "Q" while paused to quit the game
- Bug Fix: Game loads in windowed to fix the fullscreen on multiple monitors bug, go into settings to play in full screen

## Patch Notes v 0.3 
- Sniper Towers! Late game towers that will delete enemies from afar
- Updated start and end tiles to match path
- The map will change scenery based on your wave number(Grass, Sand or Concrete)
- The main menu now features a dynamic, procedurally generated game instance in the background instead of a static image.(No two visits will look the same!)
- Bug Fix: Restarting no longer brings you back to the main menu and will create a new game state
- Bug Fix: Restarting no longer resets your fullscreen back to windowed
**This is starting to feel like a finalized project that im happy with, not sure how many more updates will come, but 1.0 will be the final release barring some desire to add to this project. v0.5 will mean that I'm done with all core gameplay mechanics for single player and that the UI and Main Menu have been finalized for single player. Any version above 0.5 will be me working on multiplayer and how that will work and look**

