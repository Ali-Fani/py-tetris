from settings import *

class Game:
    def __init__(self) -> None:
        
        self.surface = pygame.Surface((GAME_WIDTH,GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(topleft = (PADDING,PADDING))
        self.grid_surface = self.surface.copy()
        self.grid_surface.fill((0,255,0))
        self.grid_surface.set_colorkey((0,255,0))
        self.grid_surface.set_alpha(120)


    def draw_grid(self):
        for col in range(1, COLUMNS):
            x = col * CELL_SIZE
            pygame.draw.line(self.grid_surface,LINE_COLOR,(x,0),(x,self.surface.get_height()),width=1)
        for row in range(1, ROWS):
            y = row * CELL_SIZE
            pygame.draw.line(self.grid_surface,LINE_COLOR,(0,y),(self.surface.get_width(),y),width=1)
        self.surface.blit(self.grid_surface,(0,0))
    def run(self):

        self.surface.fill(GRAY)


        self.draw_grid()
        self.display_surface.blit(self.surface, (PADDING,PADDING))
        pygame.draw.rect(self.display_surface,LINE_COLOR,self.rect,2,2)