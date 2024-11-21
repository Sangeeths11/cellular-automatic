import pygame
import sys
from src.enums.tileStatus import TileStatus


class Visualization:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 60
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # TODO Add more event handlers
                
    def update(self):
        # TODO simulation state
        pass
        
    def draw(self):
        self.screen.fill((255, 255, 255))
        # TODO drawing code
        pygame.display.flip()
        
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    sim = Visualization()
    sim.run()