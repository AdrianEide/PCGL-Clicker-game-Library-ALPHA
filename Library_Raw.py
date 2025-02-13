import pygame
import button

# Initialize Pygame
pygame.init()

# Game Settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 500
FPS = 60

# Game Variables
selected_Upg = 0
cookies = 100000
value_per_click = 1
rebirth_multiplier = 9  # Persistent multiplier that increases with each rebirth
dark_mode = False
URebirth = False

# Upgrade System
upgrades = []

auto_click_rate = 0

# Colors and Themes
THEMES = {
    "Default": {
        "background": (255, 255, 255),
        "text": (50, 50, 50),
        "highlight": (0, 128, 255),
        "dialog": (240, 240, 240),
        "dialog_border": (0, 128, 255),
    },
}

current_theme = "Default"
colors = THEMES[current_theme]

# Initialize Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cookie Clicker Pro")
clock = pygame.time.Clock()

# Fonts
FONT = pygame.font.SysFont('Comic sans', 20, bold=True)
TITLE_FONT = pygame.font.SysFont('Comic sans', 30, bold=True)

# Load and Scale Images
cookie_img = pygame.image.load('Cookie.png').convert_alpha()
cookie_img = pygame.transform.scale(cookie_img, (150, 150))

# Buttons
cookie_button = button.Button(425, 100, cookie_img, 2)

# Utility Functions
def switch_theme(theme_name):
    """Switch to a different theme."""
    global colors, current_theme
    if theme_name in THEMES:
        current_theme = theme_name
        colors = THEMES[theme_name]

def render_text(text, x, y, font=FONT, color=(50, 50, 50)):
    """Render text on the screen."""
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

    
def render_upgrades():
    """Render the upgrades UI."""
    for i, upgrade in enumerate(upgrades):
        y_offset = 300 + i * 40
        upgrade_text = (
            f"{upgrade['name']} (Level {upgrade['level']}/{upgrade['max_level']}): "
            f"Cost: {upgrade['cost']}"
        )
        color = colors["text"]
        if cookies < upgrade["cost"] or upgrade["level"] >= upgrade["max_level"]:
            color = (150, 150, 150)  # Dim color if not affordable or maxed out
        render_text(upgrade_text, 20, y_offset, FONT, color)

def purchase_upgrade(index):
    """Attempt to purchase an upgrade."""
    global cookies, value_per_click, auto_click_rate, rebirth_multiplier
    upgrade = upgrades[index]
    if cookies >= upgrade["cost"] and upgrade["level"] < upgrade["max_level"]:
        cookies -= upgrade["cost"]
        upgrade["level"] += 1
        upgrade["cost"] = int(upgrade["cost"] * 1.5)  # Increase cost for next level
        if upgrade["effect"] == "auto":
            auto_click_rate += 1
        elif upgrade["effect"] == "Rebirth":
            rebirth_multiplier += 1
            if rebirth_multiplier >= 5:
                value_per_click = 1 * rebirth_multiplier * rebirth_multiplier
                upgrade["cost"] / 2
            else:
                value_per_click = 1 * rebirth_multiplier  # Reset value but include rebirth multiplier
            cookies = 1
            for other_upgrade in upgrades:
                other_upgrade["level"] = 0
        else:
            upgrade["cost"] / 2
            value_per_click *= upgrade["effect"]

def main():
    global cookies

    run = True
    last_auto_click = pygame.time.get_ticks()

    while run:
        # Fill Background
        screen.fill(colors["background"])

  

        # Render Title and Stats
        render_text("Cookie Clicker Pro", SCREEN_WIDTH // 2 - 150, 20, TITLE_FONT, colors["highlight"])
        render_text(f"Cookies: {cookies}", 20, 80, FONT, colors["text"])
        render_text(f"Value per Click: {value_per_click}", 20, 120, FONT, colors["text"])
        if auto_click_rate > 0:
            render_text(f"Auto Click Rate: {auto_click_rate}/s", 20, 160, FONT, colors["text"])
        # Render Buttons
        if cookie_button.draw(screen):
            cookies += value_per_click
        render_upgrades()
        
        # Auto Clicker Logic
        current_time = pygame.time.get_ticks()
        if auto_click_rate > 0 and current_time - last_auto_click >= 1000:
            cookies += auto_click_rate * value_per_click
            last_auto_click = current_time

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Handle Upgrade Purchases
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if selected_Upg >= 0:
                        selected_Upg -= 1
                #elif event.key == pygame.K_UP:
                    #if selected_Upg <= upgrades.index:

                elif event.key == pygame.K_1:
                    purchase_upgrade(0)
                # Toggle Themes
                elif event.key == pygame.K_d:
                        switch_theme("Default")

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

# Run the Game
if __name__ == "__main__":
    main()

