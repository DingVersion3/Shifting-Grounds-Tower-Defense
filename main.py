import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TOWER_HEIGHT, TOWER_WIDTH
from logger import log_state
from tower import Tower
from map import Map
from mapgenerator import MapGenerator
from enemy import Enemy
from wave_manager import WaveManager

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    fps = pygame.time.Clock()
    dt = 0.0
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2
    updateable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    towers = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    Tower.containers = (updateable, drawable)
    tower = Tower(x, y, TOWER_HEIGHT, TOWER_WIDTH)
    game_map = Map()
    generated_map = MapGenerator(game_map.grid)
    path_cells = generated_map.generate_path()
    start = path_cells[0].grid_position
    wave_manager = WaveManager(path_cells)
    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        updateable.update(dt)
        screen.fill("black")
        game_map.draw(screen)
        wave_manager.update(dt, updateable, drawable)
        for draws in drawable:
            draws.draw(screen)
        pygame.display.flip()
        dt = fps.tick(60) / 1000

if __name__ == "__main__":
    main()