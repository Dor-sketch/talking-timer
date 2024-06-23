import asyncio
import pygame
import configparser
import time

# Initialize Pygame
pygame.init()

# Constants and Configuration
WIDTH, HEIGHT = 800, 600
RED = (255, 0, 0)
DARK_MODE_BG = (20, 20, 20)
LIGHT_MODE_BG = (240, 240, 240)
DARK_MODE_TEXT = (240, 240, 240)
LIGHT_MODE_TEXT = (20, 20, 20)

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')
pomodoro_time = config.getint('Timer', 'pomodoro_time', fallback=1500)  # 25 minutes
short_break_time = config.getint('Timer', 'short_break_time', fallback=300)  # 5 minutes
long_break_time = config.getint('Timer', 'long_break_time', fallback=900)  # 15 minutes
pomodoros_until_long_break = config.getint('Timer', 'pomodoros_until_long_break', fallback=4)

# Themes and Fonts
THEMES = {
    "light": {
        "bg_color": LIGHT_MODE_BG,
        "text_color": LIGHT_MODE_TEXT,
        "button_color": (0, 122, 255),
        "button_hover_color": (0, 101, 210),
        "button_text_color": (255, 255, 255),
        "highlight_color": (255, 87, 34),
        "progress_bar_color": (0, 122, 255),
        "overlay_color": (255, 255, 255, 100)
    },
    "dark": {
        "bg_color": DARK_MODE_BG,
        "text_color": DARK_MODE_TEXT,
        "button_color": (0, 122, 255),
        "button_hover_color": (0, 101, 210),
        "button_text_color": (255, 255, 255),
        "highlight_color": (255, 87, 34),
        "progress_bar_color": (0, 122, 255),
        "overlay_color": (0, 0, 0, 100)
    }
}

FONT = pygame.font.Font(None, 80)
SUB_FONT = pygame.font.Font(None, 40)

# Globals
remaining_time = pomodoro_time
pomodoros_completed = 0
session_type = "Pomodoro"  # Can be "Pomodoro", "Short Break", or "Long Break"
running = False
paused = False
current_theme = "light"
last_update_time = time.time()

# Classes
class Button:
    def __init__(self, x, y, w, h, color, hover_color, text, text_color):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.text_color = text_color
        self.is_hovered = False

    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        text_surface = SUB_FONT.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def set_hovered(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class ProgressBar:
    def __init__(self, x, y, w, h, color, max_value):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.max_value = max_value
        self.current_value = 0

    def draw(self, screen):
        progress_width = int(self.rect.width * self.current_value / self.max_value)
        progress_rect = pygame.Rect(self.rect.x, self.rect.y, progress_width, self.rect.height)
        pygame.draw.rect(screen, self.color, progress_rect, border_radius=10)

    def update(self, value):
        self.current_value = value

class TimerApp:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF | pygame.HWSURFACE)
        pygame.display.set_caption("Designer Pomodoro Timer")
        self.theme = THEMES[current_theme]
        self.buttons = []
        self.progress_bar = ProgressBar(50, 500, 700, 20, self.theme["progress_bar_color"], pomodoro_time)
        self.create_buttons()
        self.last_update_time = time.time()

    def create_buttons(self):
        self.buttons.append(Button(50, 550, 100, 40, self.theme["button_color"], self.theme["button_hover_color"], "Start", self.theme["button_text_color"]))
        self.buttons.append(Button(200, 550, 100, 40, self.theme["button_color"], self.theme["button_hover_color"], "Pause", self.theme["button_text_color"]))
        self.buttons.append(Button(350, 550, 100, 40, self.theme["button_color"], self.theme["button_hover_color"], "Stop", self.theme["button_text_color"]))

    def draw_background(self):
        self.screen.fill(self.theme["bg_color"])
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill(self.theme["overlay_color"])
        self.screen.blit(overlay, (0, 0))

    def update_timer_display(self):
        global remaining_time, session_type, pomodoros_completed
        mins, secs = divmod(remaining_time, 60)
        timer_str = f"{mins:02d}:{secs:02d}"

        self.draw_background()

        timer_text = FONT.render(timer_str, True, self.theme["text_color"])
        session_text = SUB_FONT.render(session_type, True, self.theme["text_color"])
        pomo_text = SUB_FONT.render(f"Pomodoros: {pomodoros_completed}", True, self.theme["text_color"])

        self.screen.blit(timer_text, (self.screen.get_width() // 2 - timer_text.get_width() // 2, 100))
        self.screen.blit(session_text, (self.screen.get_width() // 2 - session_text.get_width() // 2, 250))
        self.screen.blit(pomo_text, (self.screen.get_width() // 2 - pomo_text.get_width() // 2, 300))

        self.progress_bar.draw(self.screen)

        for button in self.buttons:
            button.draw(self.screen)

        pygame.display.flip()

    def display_message(self, message, color):
        self.draw_background()
        text = SUB_FONT.render(message, True, color)
        self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, self.screen.get_height() // 2 - text.get_height() // 2))
        pygame.display.flip()

    def handle_events(self):
        global remaining_time, session_type, pomodoros_completed, running, paused, current_theme
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_n:
                    remaining_time = 0
                elif event.key == pygame.K_q:
                    pygame.quit()
                    return False
                elif event.key == pygame.K_t:
                    # Cycle through themes
                    themes = list(THEMES.keys())
                    current_index = themes.index(current_theme)
                    current_theme = themes[(current_index + 1) % len(themes)]
                    self.theme = THEMES[current_theme]
                    self.create_buttons()
            elif event.type == pygame.MOUSEMOTION:
                for button in self.buttons:
                    button.set_hovered(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button.is_clicked(event.pos):
                        if button.text == "Start":
                            running = True
                            paused = False
                        elif button.text == "Pause":
                            paused = not paused
                        elif button.text == "Stop":
                            running = False
                            remaining_time = pomodoro_time
        return True

    async def menu(self):
        self.display_message("Press S to Start or Q to Quit", self.theme["text_color"])
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        return False
                    elif event.key == pygame.K_s:
                        return True
            await asyncio.sleep(0)

    async def run(self):
        global remaining_time, pomodoros_completed, session_type, running, paused, current_theme

        if not await self.menu():
            return

        running = True
        paused = False

        while True:
            current_time = time.time()
            if running and not paused:
                remaining_time -= int(current_time - self.last_update_time)
                self.last_update_time = current_time

            if remaining_time <= 0:
                if session_type == "Pomodoro":
                    pomodoros_completed += 1
                    if pomodoros_completed % pomodoros_until_long_break == 0:
                        session_type = "Long Break"
                        remaining_time = long_break_time
                    else:
                        session_type = "Short Break"
                        remaining_time = short_break_time
                elif session_type == "Short Break":
                    session_type = "Pomodoro"
                    remaining_time = pomodoro_time
                elif session_type == "Long Break":
                    session_type = "Pomodoro"
                    remaining_time = pomodoro_time

                self.display_message(f"{session_type} time!", RED)
                await asyncio.sleep(2)

            # Update progress bar
            self.progress_bar.update(pomodoro_time - remaining_time)

            # Update display
            self.update_timer_display()

            # Handle events
            if not self.handle_events():
                return

            await asyncio.sleep(1)

# Run the timer application
if __name__ == "__main__":
    timer_app = TimerApp()
    asyncio.run(timer_app.run())
