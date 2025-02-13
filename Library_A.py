import time
import pygame
import button

class ClickerGame:
    def __init__(self, screen_size=(800, 500), fps=60):
        pygame.init()
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = screen_size
        self.FPS = fps
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Clicker Game")

        self.cookies = 0
        self.value_per_click = 1
        self.auto_click_rate = 0
        self.upgrades = []

        cookie_img = pygame.image.load('Cookie.png').convert_alpha()
        cookie_img = pygame.transform.scale(cookie_img, (150, 150))
        self.cookie_button = button.Button(425, 100, cookie_img, 2)

    def render_text(self, text, x, y, font, color=(50, 50, 50)):
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def add_upgrade(self, name, cost, effect, max_level=10):
        upgrade = {"name": name, "cost": cost, "effect": effect, "level": 0, "max_level": max_level}
        self.upgrades.append(upgrade)

    def purchase_upgrade(self, index):
        if index < len(self.upgrades):
            upgrade = self.upgrades[index]
            if self.cookies >= upgrade["cost"] and upgrade["level"] < upgrade["max_level"]:
                self.cookies -= upgrade["cost"]
                upgrade["level"] += 1
                upgrade["cost"] = int(upgrade["cost"] * 1.5)
                if upgrade["effect"] == "auto":
                    self.auto_click_rate += 1
                elif isinstance(upgrade["effect"], (int, float)):
                    self.value_per_click *= upgrade["effect"]

    def click_cookie(self):
        self.cookies += self.value_per_click

    def auto_click(self):
        self.cookies += self.auto_click_rate * self.value_per_click 

    def update(self):
        current_time = pygame.time.get_ticks()
        clicks_per_second = 10  # Increase the frequency (e.g., 10 times per second)
        interval = 1000 // clicks_per_second  # Time between clicks in milliseconds

        if self.auto_click_rate > 0 and current_time % interval < self.FPS: #also please someone fix the slower autoclicker when you hold mouse down
            self.scaled_click_value = self.auto_click_rate / self.cookies + 1 #cookies slow down the more you have
            self.auto_click()

    def get_game_state(self):
        return {
            "cookies": self.cookies,
            "value_per_click": self.value_per_click,
            "auto_click_rate": self.auto_click_rate,
            "upgrades": self.upgrades,
        }
    
    def render_button(self):
        self.cookie_button.draw(self.screen)
        if self.cookie_button.clicked:
            self.click_cookie() 
            time.sleep(0.08)
    
    def Click_anywhere(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.click_cookie()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if pygame.K_1 <= event.key <= pygame.K_9:  # Check if key is between 1-9
                index = event.key - pygame.K_1  # Convert key press to an index (0-8)
                self.purchase_upgrade(index)  # Attempt to purchase the upgrade at that index

    def render(self, font):
        self.screen.fill((255, 255, 255))
        self.render_text(f"Cookies: {self.cookies}", 20, 50, font)
        self.render_text(f"Value per Click: {self.value_per_click}", 20, 80, font)
        self.render_text(f"Auto Click Rate: {self.auto_click_rate}/s", 20, 110, font)
        self.render_button()
        pygame.display.update()

    def cleanup(self):
        pygame.quit()