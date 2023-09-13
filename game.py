import pygame, sys, math, random

class Particle:
    def __init__(self, x, y):
        self.particle_x = x
        self.particle_y = y
        self.particle_angle = random.uniform(0, 360)
        self.particle_speed = random.uniform(0.5, 10)
        self.particle_color = (255, 255, 255)
        self.particle_radius = 2
        self.particle_lifetime = random.uniform(10, 100)
        self.rise_duration = 30
        self.fall_duration = self.particle_lifetime - self.rise_duration
        self.time_elapsed = 0

    def update(self):
        if self.time_elapsed < self.rise_duration:
            self.particle_y -= self.particle_speed
        else:
            self.particle_y += self.particle_speed

        angle_change = random.uniform(-1, 1)
        self.particle_angle += angle_change

        self.particle_x += math.cos(math.radians(self.particle_angle)) * self.particle_speed

        self.particle_lifetime -= 1
        self.time_elapsed += 1

    def draw(self, screen):
        alpha = int(max(0, min((self.particle_lifetime / 60) * 255, 255)))
        color = (self.particle_color[0], self.particle_color[1], self.particle_color[2], alpha)
        pygame.draw.circle(screen, color, (int(self.particle_x), int(self.particle_y)), self.particle_radius)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 20)

        self.particles = []
        self.particle_generation_timer = 0

        self.level = 1
        self.exp = 0
        self.exp_per_level = 100 * self.level
        self.exp_per_click = 1.0 * self.level
        self.level_up_button = pygame.Rect(500, 300, 200, 100)
        self.level_up_button_color = (0, 255, 0)
        self.clicked = False
        level_up_button_center_x = self.level_up_button.x + self.level_up_button.width / 2

        self.gold = 300
        self.gold_per_click = 1.0 * self.level
        self.gold_per_level = 300 * self.level
        self.gold_mine_button = pygame.Rect(200, 300, 200, 100)
        self.gold_mine_button_color = (255, 255, 0)
        self.clicked = False
        gold_mine_button_center_x = self.gold_mine_button.x + self.gold_mine_button.width / 2

        self.auto_clicker_button = pygame.Rect(50, 170, 170, 60)
        self.auto_clicker_button_color = (255, 255, 100)
        self.auto_clicker_active = False
        self.auto_clicker_cost = 300
        self.exp_per_click_multiplier = 1.5
        self.auto_clicker_cost_multiplier = 1.3 
        self.auto_clicker_bought = False

        self.auto_gold_mine_button = pygame.Rect(50, 100, 170, 60)
        self.auto_gold_mine_button_color = (255, 255, 100)
        self.auto_gold_mine_active = False
        self.auto_gold_mine_cost = 300
        self.auto_gold_mine_gold_per_second = 2.0
        self.gold_per_click_multiplier = 2.0
        self.auto_gold_mine_cost_multiplier = 1.3
        self.auto_gold_mine_bought = False

        self.expedition_10s_button = pygame.Rect(50, 240, 170, 60)
        self.expedition_60s_button = pygame.Rect(50, 310, 170, 60)
        self.expedition_buttons_color = (100, 100, 255)
        self.expedition_10s_active = False
        self.expedition_60s_active = False
        self.expedition_10s_timer = 0
        self.expedition_60s_timer = 0
        self.expedition_10s_duration = 0
        self.expedition_60s_duration = 0
        self.expedition_food_rewards = [random.randint(1, 40) for _ in range(20)]
        self.amount_of_food = 0

    def append_particles(self, x, y):
        exp_scaling_factor = 5
        gold_scaling_factor = 5
        
        num_exp_particles = int(exp_scaling_factor * 2)
        num_gold_particles = int(gold_scaling_factor * 2)

        for _ in range(num_exp_particles):
            particle = Particle(x, y)
            particle.particle_angle = random.uniform(0, 360)
            particle.particle_speed = random.uniform(1, 2)
            self.particles.append(particle)

        for _ in range(num_gold_particles):
            particle = Particle(x, y)
            particle.particle_angle = random.uniform(0, 360)
            particle.particle_speed = random.uniform(1, 2)
            self.particles.append(particle)

    def auto_clicker_particles(self):
        if self.auto_clicker_active:
            self.append_particles(self.level_up_button.centerx, self.level_up_button.y)

    def auto_gold_mine_particles(self):
        if self.auto_gold_mine_active:
            self.append_particles(self.gold_mine_button.centerx, self.gold_mine_button.y)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if self.level_up_button.collidepoint(mouse_pos):
                    self.exp += self.exp_per_click
                    scaling_factor = self.exp_per_click / 10
                    self.append_particles(self.level_up_button.centerx, self.level_up_button.y)

                    if self.exp >= self.exp_per_level:
                        self.exp -= self.exp_per_level
                        self.level += 1
                        print(self.level, "level up!")
                        self.exp_per_level *= 1.5
                        self.exp_per_click *= 1.5
                        self.gold_per_level *= 1.5
                        self.gold_per_click *= 1.5
                        self.update_button_texts()
                if self.gold_mine_button.collidepoint(mouse_pos):
                    self.gold += self.gold_per_click
                    print(self.gold, "struck gold!")
                    scaling_factor = self.gold_per_click / 10
                    self.append_particles(self.gold_mine_button.centerx, self.gold_mine_button.y)

                if self.auto_clicker_button.collidepoint(mouse_pos):
                    if self.gold >= self.auto_clicker_cost:
                        self.auto_clicker_active = True
                        self.auto_clicker_bought = True
                        self.gold -= self.auto_clicker_cost
                        self.auto_clicker_cost = int(self.auto_clicker_cost * self.auto_clicker_cost_multiplier)
                        self.exp_per_click *= self.exp_per_click_multiplier 
                        self.gold_per_click *= self.gold_per_click_multiplier
                        self.update_button_texts()
                if self.auto_gold_mine_button.collidepoint(mouse_pos):
                    if self.level >= 2:
                        if self.gold >= self.auto_gold_mine_cost:
                            self.auto_gold_mine_active = True
                            self.auto_gold_mine_bought = True
                            self.gold -= self.auto_gold_mine_cost
                            self.auto_gold_mine_cost = int(self.auto_gold_mine_cost * self.auto_gold_mine_cost_multiplier)
                            self.auto_gold_mine_gold_per_second *= self.gold_per_click_multiplier
                            self.update_button_texts()
                if self.expedition_10s_button.collidepoint(mouse_pos):
                    if self.level >= 5:
                        if not self.expedition_10s_active:
                            self.expedition_10s_active = True
                            self.expedition_10s_duration = 10
                            self.expedition_10s_timer = self.expedition_10s_duration * 60
                            self.auto_clicker_active = False
                            self.update_button_texts()
                if self.expedition_60s_button.collidepoint(mouse_pos):
                    if self.level >= 10:
                        if not self.expedition_60s_active:
                            self.expedition_60s_active = True
                            self.expedition_60s_duration = 60
                            self.expedition_60s_timer = self.expedition_60s_duration * 60
                            self.auto_clicker_active = False
                            self.update_button_texts()

    def update_button_texts(self):
        self.level_up_button_text = self.font_small.render(f"Level Up! ({math.ceil(self.exp_per_click)})", True, (255, 255, 255))
        self.gold_mine_button_text = self.font_small.render(f"Gold Mine! ({math.ceil(self.gold_per_click)})", True, (255, 255, 255))

    def render(self):
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, self.level_up_button_color, self.level_up_button, border_radius=10)
        pygame.draw.rect(self.screen, self.gold_mine_button_color, self.gold_mine_button, border_radius=10)
        pygame.draw.rect(self.screen, self.auto_clicker_button_color, self.auto_clicker_button, border_radius=10)

        def abbreviate_number(number):
            if number >= 1e18:
                if number % 1e18 == 0:
                    return f'{number/1e18:.0f}Qu'
                else:
                    return f'{number/1e18:.2f}Qu'
            elif number >= 1e15:
                if number % 1e15 == 0:
                    return f'{number/1e15:.0f}Qd'
                else:
                    return f'{number/1e15:.2f}Qd'
            elif number >= 1e12:
                if number % 1e12 == 0:
                    return f'{number/1e12:.0f}T'
                else:
                    return f'{number/1e12:.2f}T'
            elif number >= 1e9:
                if number % 1e9 == 0:
                    return f'{number/1e9:.0f}B'
                else:
                    return f'{number/1e9:.2f}B'
            elif number >= 1e6:
                if number % 1e6 == 0:
                    return f'{number/1e6:.0f}M'
                else:
                    return f'{number/1e6:.2f}M'
            elif number >= 1e3:
                if number % 1e3 == 0:
                    return f'{number/1e3:.0f}K'
                else:
                    return f'{number/1e3:.2f}K'
            else:
                return f'{number:.0f}'

        text = self.font.render(f"Level: {self.level} | Exp: {abbreviate_number(math.ceil(self.exp))}/{abbreviate_number(self.exp_per_level)}", True, (255, 255, 255))
        self.screen.blit(text, (20, 20))
        text = self.font.render(f"Gold: {abbreviate_number(math.ceil(self.gold))}/{abbreviate_number(self.gold_per_level)}", True, (255, 255, 255))
        self.screen.blit(text, (20, 50))
        text = self.font_small.render(f"Level Up! ({abbreviate_number(math.ceil(self.exp_per_click))})", True, ("black"))
        self.screen.blit(text, (self.level_up_button.x + 10, self.level_up_button.y + 10))
        text = self.font_small.render(f"Gold Mine! ({abbreviate_number(math.ceil(self.gold_per_click))})", True, ("black"))
        self.screen.blit(text, (self.gold_mine_button.x + 10, self.gold_mine_button.y + 10))
        text = self.font_small.render(f"Auto EXP ({abbreviate_number(math.ceil(self.auto_clicker_cost))}g)", True, ("black"))
        self.screen.blit(text, (self.auto_clicker_button.x + 10, self.auto_clicker_button.y + 10))
        text = self.font_small.render(f"Food {abbreviate_number(self.amount_of_food)}", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.topright = (780, 20)
        self.screen.blit(text, text_rect)

        if self.level >= 2:
            pygame.draw.rect(self.screen, self.auto_gold_mine_button_color, self.auto_gold_mine_button, border_radius=10)
            text = self.font_small.render(f"Auto Gold ({abbreviate_number(math.ceil(self.auto_gold_mine_cost))}g)", True, ("black"))
            self.screen.blit(text, (self.auto_gold_mine_button.x + 10, self.auto_gold_mine_button.y + 10))
        if self.level >= 5:
            pygame.draw.rect(self.screen, self.expedition_buttons_color, self.expedition_10s_button, border_radius=10)
            text = self.font_small.render(f"10s expedition", True, ("black"))
            self.screen.blit(text, (self.expedition_10s_button.x + 10, self.expedition_10s_button.y + 10))
        if self.level >= 10:
            pygame.draw.rect(self.screen, self.expedition_buttons_color, self.expedition_60s_button, border_radius=10)
            text = self.font_small.render("1m Expedition", True, (0, 0, 0))
            self.screen.blit(text, (self.expedition_60s_button.x + 10, self.expedition_60s_button.y + 10))

        if self.expedition_10s_active:
            text = self.font_small.render(f"10s expedition ({self.expedition_10s_timer // 60}s)", True, (0, 0, 0))
            self.screen.blit(text, (self.expedition_10s_button.x + 10, self.expedition_10s_button.y + 10))
        if self.expedition_60s_active:
            text = self.font_small.render(f"1m Expedition ({self.expedition_60s_timer // 60}s)", True, (0, 0, 0))
            self.screen.blit(text, (self.expedition_60s_button.x + 10, self.expedition_60s_button.y + 10))

        for particle in self.particles:
            particle.update()
            particle.draw(self.screen)
            if particle.particle_lifetime <= 0:
                self.particles.remove(particle)

        pygame.display.update()

    def run(self):
        auto_clicker_timer = 0
        auto_gold_mine_timer = 0
        while True:
            self.handle_events()
            self.particle_generation_timer += 1
            if self.particle_generation_timer >= 60:
                self.auto_clicker_particles()
                self.auto_gold_mine_particles()
                self.particle_generation_timer -= 60

            if self.auto_clicker_active:
                auto_clicker_timer += 1
                if auto_clicker_timer >= 60:
                    auto_clicker_timer -= 60
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
            if self.auto_gold_mine_active:
                auto_gold_mine_timer += 1
                if auto_gold_mine_timer >= 60:
                    auto_gold_mine_timer -= 60
                    self.gold += self.auto_gold_mine_gold_per_second
                    print(self.gold, "struck gold!")
            if self.expedition_10s_active:
                if self.expedition_10s_timer > 0:
                    self.expedition_10s_timer -= 1
                    if self.expedition_10s_timer % 60 == 0:
                        print(f"Expedition time remaining: {self.expedition_10s_timer // 60} seconds")
                else:
                    self.expedition_10s_active = False
                    food_multiplier = self.expedition_10s_duration * self.level / 60
                    random_food_reward = random.choice(self.expedition_food_rewards)
                    food_gain = int(random_food_reward * food_multiplier * self.level)
                    self.amount_of_food += food_gain
                    print(f"Expedition completed! You found {food_gain} units of food.")
                    self.update_button_texts()
                    if self.auto_clicker_bought:
                        self.auto_clicker_active = True

            if self.expedition_60s_active:
                if self.expedition_60s_timer > 0:
                    self.expedition_60s_timer -= 1
                    if self.expedition_60s_timer % 60 == 0:
                        print(f"Expedition time remaining: {self.expedition_60s_timer // 60} seconds")
                else:
                    self.expedition_60s_active = False
                    # Calculate food gain based on expedition duration
                    food_multiplier = self.expedition_60s_duration * self.level / 60
                    random_food_reward = random.choice(self.expedition_food_rewards)
                    food_gain = int(random_food_reward * food_multiplier * self.level)
                    self.amount_of_food += food_gain
                    print(f"Expedition completed! You found {food_gain} units of food.")
                    self.update_button_texts()
                    if self.auto_clicker_bought:
                        self.auto_clicker_active = True

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