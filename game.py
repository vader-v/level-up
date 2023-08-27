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
        self.level_up_button = pygame.Rect(500, 300, 200, 100)
        self.level_up_button_color = (0, 255, 0)
        self.clicked = False

        self.gold = 300
        self.gold_per_click = 1.0
        self.gold_per_level = 300
        self.gold_mine_button = pygame.Rect(200, 300, 200, 100)
        self.gold_mine_button_color = (255, 255, 0)
        self.clicked = False

        self.auto_clicker_button = pygame.Rect(100, 100, 80, 90)
        self.auto_clicker_button_color = (255, 255, 100)
        self.auto_clicker_active = False
        self.auto_clicker_cost = 300
        self.exp_per_click_multiplier = 1.5
        self.auto_clicker_cost_multiplier = 1.3 

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if self.level_up_button.collidepoint(mouse_pos):
                    self.exp += self.exp_per_click
                    if self.exp >= self.exp_per_level:
                        self.exp -= self.exp_per_level
                        self.level += 1
                        print(self.level, "level up!")
                        self.exp_per_level *= 1.5
                        self.exp_per_click *= 1.5
                        self.gold_per_level *= 1.5
                        self.gold_per_click *= 1.5
                        self.update_button_texts()
                elif self.gold_mine_button.collidepoint(mouse_pos):
                    self.gold += self.gold_per_click
                    print(self.gold, "struck gold!")
                elif self.auto_clicker_button.collidepoint(mouse_pos):
                    if self.gold >= self.auto_clicker_cost:
                        self.auto_clicker_active = True
                        self.gold -= self.auto_clicker_cost
                        self.auto_clicker_cost = int(self.auto_clicker_cost * self.auto_clicker_cost_multiplier)
                        self.exp_per_click *= self.exp_per_click_multiplier 

    def update_button_texts(self):
        self.level_up_button_text = self.font.render(f"Level Up! ({int(self.exp_per_click)})", True, (255, 255, 255))
        self.gold_mine_button_text = self.font.render(f"Gold Mine! ({int(self.gold_per_click)})", True, (255, 255, 255))

    def render(self):
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, self.level_up_button_color, self.level_up_button, border_radius=10)
        pygame.draw.rect(self.screen, self.gold_mine_button_color, self.gold_mine_button, border_radius=10)
        pygame.draw.rect(self.screen, self.auto_clicker_button_color, self.auto_clicker_button, border_radius=10)

        text = self.font.render(f"Level: {self.level} | Exp: {int(self.exp)}/{self.exp_per_level}", True, (255, 255, 255))
        self.screen.blit(text, (20, 20))
        text = self.font.render(f"Gold: {int(self.gold)}/{self.gold_per_level}", True, (255, 255, 255))
        self.screen.blit(text, (20, 50))
        text = self.font.render(f"Level Up! ({int(self.exp_per_click)})", True, ("black"))
        self.screen.blit(text, (self.level_up_button.x + 10, self.level_up_button.y + 10))
        text = self.font.render(f"Gold Mine! ({int(self.gold_per_click)})", True, ("black"))
        self.screen.blit(text, (self.gold_mine_button.x + 10, self.gold_mine_button.y + 10))
        text = self.font.render(f"Auto Clicker ({int(self.auto_clicker_cost)})", True, ("black"))
        self.screen.blit(text, (self.auto_clicker_button.x + 10, self.auto_clicker_button.y + 10))

        pygame.display.update()

    def run(self):
        auto_clicker_timer = 0
        while True:
            self.handle_events()
            if self.auto_clicker_active:
                auto_clicker_timer += 1
                if auto_clicker_timer >= 60:
                    auto_clicker_timer = 0
                    self.exp += self.exp_per_click
                    if self.exp >= self.exp_per_level:
                        self.exp -= self.exp_per_level
                        self.level += 1
                        print(self.level, "level up!")
                        self.exp_per_level *= 1.5
                        self.exp_per_click *= 1.5
                        self.gold_per_level *= 1.5
                        self.gold_per_click *= 1.5
                        self.update_button_texts()

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
pygame.display.set_caption("Level +One!")
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