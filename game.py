from random import choice

from settings import (
    BLOCK_OFFSET,
    CELL_SIZE,
    COLUMNS,
    GAME_HEIGHT,
    GAME_WIDTH,
    GRAY,
    LINE_COLOR,
    MOVE_WAIT_TIME,
    PADDING,
    ROWS,
    TETROMINOS,
    UPDATE_START_SPEED,
    pygame,
)
from timer import Timer


class Game:
    def __init__(self) -> None:
        self.surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(topleft=(PADDING, PADDING))

        self.sprites = pygame.sprite.Group()

        self.grid_surface = self.surface.copy()
        self.grid_surface.fill((0, 255, 0))
        self.grid_surface.set_colorkey((0, 255, 0))
        self.grid_surface.set_alpha(120)

        self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
        self.tetromino = Tetromino(
            choice(list(TETROMINOS.keys())),
            self.sprites,
            self.create_new_tetromino,
            self.field_data,
        )

        # timer
        self.timers = {
            "vertical move": Timer(UPDATE_START_SPEED, True, self.move_down),
            "horizontal move": Timer(MOVE_WAIT_TIME),
        }
        self.timers["vertical move"].activate()

    def create_new_tetromino(self):
        self.tetromino = Tetromino(
            choice(list(TETROMINOS.keys())),
            self.sprites,
            self.create_new_tetromino,
            self.field_data,
        )

    def timer_update(self):
        for timer in self.timers.values():
            timer.update()

    def move_down(self):
        # print("Timer",pygame.time.get_ticks())
        self.tetromino.move_down()

    def draw_grid(self):
        for col in range(1, COLUMNS):
            x = col * CELL_SIZE
            pygame.draw.line(
                self.grid_surface,
                LINE_COLOR,
                (x, 0),
                (x, self.surface.get_height()),
                width=1,
            )
        for row in range(1, ROWS):
            y = row * CELL_SIZE
            pygame.draw.line(
                self.grid_surface,
                LINE_COLOR,
                (0, y),
                (self.surface.get_width(), y),
                width=1,
            )
        self.surface.blit(self.grid_surface, (0, 0))

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.timers["horizontal move"].active:
            if keys[pygame.K_LEFT]:
                self.tetromino.move_horizontal(-1)
                self.timers["horizontal move"].activate()
            if keys[pygame.K_RIGHT]:
                self.tetromino.move_horizontal(1)
                self.timers["horizontal move"].activate()

        # for event in pygame.event.get():
        #     if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
        #         if event.key == pygame.K_LEFT:
        #             self.tetromino.move_horizontal(-1)
        #         elif event.key == pygame.K_RIGHT:
        #             self.tetromino.move_horizontal(1)

    def run(self):
        # update
        self.input()
        self.timer_update()
        self.sprites.update()
        # drawing
        self.surface.fill(GRAY)
        self.sprites.draw(self.surface)

        self.draw_grid()
        self.display_surface.blit(self.surface, (PADDING, PADDING))
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 2)


class Tetromino:
    def __init__(self, shape, group, create_new_tetromino, field_data) -> None:
        self.block_positions = TETROMINOS[shape]["shape"]
        self.color = TETROMINOS[shape]["color"]
        self.blocks = [Block(group, pos, self.color) for pos in self.block_positions]
        self.create_new_tetromino = create_new_tetromino
        self.field_data = field_data

    def create_new_tetromino(self):
        self.tetromino = Tetromino(
            choice(list(TETROMINOS.keys())),
            self.sprites,
            self.create_new_tetromino,
            self.field_data,
        )

    # collisions
    def next_move_horizontal_collide(self, blocks, direction: int):
        collision_list = [
            block.horizontal_collide(int(block.pos.x + direction), self.field_data)
            for block in blocks
        ]
        return True if any(collision_list) else False

    def next_move_vertical_collide(self, blocks, direction):
        collision_list = [
            block.vertical_collide(int(block.pos.y + direction), self.field_data)
            for block in blocks
        ]
        return True if any(collision_list) else False

    def move_down(self):
        if not self.next_move_vertical_collide(self.blocks, 1):
            for block in self.blocks:
                block.pos.y += 1
        else:
            for block in self.blocks:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block
            self.create_new_tetromino()

    def move_horizontal(self, direction):
        if not self.next_move_horizontal_collide(self.blocks, direction):
            for block in self.blocks:
                block.pos.x += direction


class Block(pygame.sprite.Sprite):
    def __init__(self, group, pos, color) -> None:
        # general
        super().__init__(group)
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(color)

        # position
        self.pos = pygame.Vector2(pos) + BLOCK_OFFSET
        self.rect = self.image.get_rect(topleft=self.pos * CELL_SIZE)

    def horizontal_collide(self, x, field_data) -> bool:
        if not 0 <= x < COLUMNS:
            return True
        if field_data[int(self.pos.y)][x]:
            return True

    def vertical_collide(self, y, field_data) -> bool:
        if y >= ROWS:
            return True
        if y >= 0 and field_data[y][int(self.pos.x)]:
            return True

    def update(self):
        self.rect.topleft = self.pos * CELL_SIZE
