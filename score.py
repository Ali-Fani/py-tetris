from settings import (
    GAME_HEIGHT,
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

    def run(self):
        self.display_surface.blit(self.surface, self.rect)
