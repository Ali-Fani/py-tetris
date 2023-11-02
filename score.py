from os import path

from settings import (
    GAME_HEIGHT,
    GRAY,
    LINE_COLOR,
    PADDING,
    SCORE_HEIGHT_FRACTION,
    SIDEBAR_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    pygame,
)


class Score:
    def __init__(self) -> None:
        self.surface = pygame.Surface(
            (SIDEBAR_WIDTH, GAME_HEIGHT * SCORE_HEIGHT_FRACTION - PADDING)
        )
        self.rect = self.surface.get_rect(
            bottomright=(WINDOW_WIDTH - PADDING, WINDOW_HEIGHT - PADDING)
        )
        self.display_surface = pygame.display.get_surface()

        self.font = pygame.font.Font(path.join(".", "assets", "Russo_One.ttf"), 30)

        self.increment_height = self.surface.get_height() / 3

        # data
        self.score = 0
        self.level = 1
        self.lines = 0

    def display_text(self, position, text):
        text_surface = self.font.render(
            f"{text[0]}: {text[1]}", True, pygame.Color("white")
        )
        text_rect = text_surface.get_rect(center=position)
        self.surface.blit(text_surface, text_rect)

    def run(self):
        self.surface.fill(GRAY)
        for index, text in enumerate(
            [("Score", self.score), ("Level", self.level), ("Lines", self.lines)]
        ):
            x = self.surface.get_width() / 2
            y = self.increment_height / 2 + index * self.increment_height
            self.display_text((x, y), text)
        self.display_surface.blit(self.surface, self.rect)
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 2)
