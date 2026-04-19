import pygame
import config

class LyricsDisplay:
    def __init__(self):
        pygame.init()
        self.font = pygame.font.SysFont("Arial", config.FONT_SIZE, bold=True)

        if config.FULLSCREEN:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((1280, 720))

        pygame.display.set_caption("Lyrics Display")
        self.current_line = ""
        self.running = True

    def update(self, line: str | None):
        """Update the displayed lyric line."""
        if line is not None:
            self.current_line = line

    def render(self):
        """Draw the current lyric line to the screen."""
        # handle quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

        # clear screen
        self.screen.fill(config.BACKGROUND_COLOR)

        if self.current_line:
            # wrap long lines
            words = self.current_line.split()
            lines = []
            current = ""

            for word in words:
                test = current + " " + word if current else word
                if self.font.size(test)[0] < self.screen.get_width() - 100:
                    current = test
                else:
                    lines.append(current)
                    current = word
            if current:
                lines.append(current)

            # draw each wrapped line centered
            total_height = len(lines) * (config.FONT_SIZE + 10)
            y = (self.screen.get_height() - total_height) // 2

            for line in lines:
                surface = self.font.render(line, True, config.FONT_COLOR)
                x = (self.screen.get_width() - surface.get_width()) // 2
                self.screen.blit(surface, (x, y))
                y += config.FONT_SIZE + 10

        pygame.display.flip()

    def close(self):
        """Shut down the display."""
        pygame.quit()
