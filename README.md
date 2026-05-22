# Shifting-Grounds-Tower-Defense
A procedurally generated tower defense game built with Python and Pygame
The natural build order would be something like:

1. Grid system — drawable map with a defined path from start to end ✅ (the implementation i wanted to do rna into too many issues, moved to something much simpler for my sanity)
2. Enemy waves — enemies that follow the path, with health and speed ✅ 
3. Towers — placeable on non-path tiles, with range and attack logic ❌
4. Projectiles — towers targeting and shooting nearest enemy in range ✅
5. Game loop — lives, money, wave counter, game over screen ❌
6. 2-3 tower types — e.g. basic, slow, splash damage ❌
7. 2-3 enemy types — e.g. fast/weak, slow/tanky, armored ❌
8. UI — tower selection panel, sell/upgrade towers ❌