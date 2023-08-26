import pygame, sys

import pygame

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        self.level = 1
        self.exp = 0
        self.exp_per_level = 100
        self.exp_per_click = 1.0
        self.level_up_button = pygame.Rect(300, 300, 200, 100)
        self.level_up_button_color = (0, 255, 0)
        self.clicked = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.mouse_pos = pygame.mouse.get_pos()
                if self.level_up_button.collidepoint(self.mouse_pos):
                    self.exp += self.exp_per_click
                    if self.exp >= self.exp_per_level:
                        self.exp -= self.exp_per_level
                        self.level += 1
                        self.exp_per_level *= 1.5

    def render(self):
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, self.level_up_button_color, self.level_up_button, border_radius=10)

        text = self.font.render(f"Level: {self.level} | Exp: {int(self.exp)}/{self.exp_per_level}", True, (255, 255, 255))
        self.screen.blit(text, (20, 20))

        pygame.display.update()

    def run(self):
        while True:
            self.handle_events()
            self.render()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()

pygame.init()
width = 800
height = 600

game = Game()

screen = pygame.display.set_mode(size=(width, height))
text_font = pygame.font.Font(None, 50)
title = text_font.render("Level +One!", True, "black")
clock = pygame.time.Clock()

while True:
  screen.fill("white")
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
  screen.blit(title, (270, 15))
  game.render()
  pygame.display.update()
  clock.tick(60)