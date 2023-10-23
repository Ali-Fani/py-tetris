from settings import *

class Preview:
    def __init__(self) -> None:
        
        self.surface = pygame.Surface((SIDEBAR_WIDTH,GAME_HEIGHT * PREVIEW_HEIGHT_FRACTION - PADDING))
        self.rect = self.surface.get_rect(topright = (WINDOW_WIDTH-PADDING,PADDING))
        self.display_surface = pygame.display.get_surface()

    def run(self):
        self.display_surface.blit(self.surface,self.rect)
