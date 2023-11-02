from os import path

from pygame.image import load

from settings import (
    CELL_SIZE,
    GAME_HEIGHT,
    GRAY,
    LINE_COLOR,
    PADDING,
    PREVIEW_HEIGHT_FRACTION,
    SIDEBAR_WIDTH,
    TETROMINOS,
    WINDOW_WIDTH,
    pygame,
)


class Preview:
    def __init__(self) -> None:
        self.surface = pygame.Surface(
            (SIDEBAR_WIDTH, GAME_HEIGHT * PREVIEW_HEIGHT_FRACTION - PADDING)
        )
        self.rect = self.surface.get_rect(topright=(WINDOW_WIDTH - PADDING, PADDING))
        self.display_surface = pygame.display.get_surface()
        self.shape_surfaces = {
            shape: load(path.join(".", "assets", f"{shape}.png")).convert_alpha()
            for shape in TETROMINOS.keys()
        }
        self.increament_height = self.surface.get_height() / 3

    def display_pieces(self, shapes):
        for index, shape in enumerate(shapes):
            shape_surface = self.shape_surfaces[shape]
            x = self.surface.get_width() / 2
            y = self.increament_height / 2 + index * self.increament_height
            rect = shape_surface.get_rect(center=(x, y))
            self.surface.blit(shape_surface, rect)

    def run(self, next_shapes):
        self.surface.fill(GRAY)
        self.display_pieces(next_shapes)
        self.display_surface.blit(self.surface, self.rect)
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 2)
