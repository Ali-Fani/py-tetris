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
    ROTATE_WAIT_TIME,
    ROWS,
    SCORE_DATA,
    TETROMINOS,
    UPDATE_START_SPEED,
    pygame,
)
from timer import Timer


class Game:
    def __init__(self, get_next_shape, update_score) -> None:
        self.surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(topleft=(PADDING, PADDING))

        self.sprites = pygame.sprite.Group()

        self.get_next_shape = get_next_shape

        self.grid_surface = self.surface.copy()
        self.grid_surface.fill((0, 255, 0))
        self.grid_surface.set_colorkey((0, 255, 0))
        self.grid_surface.set_alpha(120)
        self.update_score = update_score
        self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
        self.tetromino = Tetromino(
            choice(list(TETROMINOS.keys())),
            self.sprites,
            self.create_new_tetromino,
            self.field_data,
        )

        # timer
        self.down_speed = UPDATE_START_SPEED
        self.down_speed_faster = self.down_speed * 0.3
        self.down_pressed = False
        self.timers = {
            "vertical move": Timer(UPDATE_START_SPEED, True, self.move_down),
            "horizontal move": Timer(MOVE_WAIT_TIME),
            "rotate": Timer(ROTATE_WAIT_TIME),
        }
        self.timers["vertical move"].activate()

        self.current_level = 1
        self.current_score = 0
        self.current_lines = 0

    def calculate_score(self, lines):
        self.current_lines += lines
        self.current_score += SCORE_DATA[lines] * self.current_level
        if self.current_lines / 10 > self.current_level:
            self.current_level += 1
            self.down_speed *= 0.80
            self.down_speed_faster = self.down_speed * 0.3
            self.timers["vertical_move"].duration = self.down_speed
        self.update_score(self.current_lines, self.current_score, self.current_level)

    def create_new_tetromino(self):
        self.check_finished_rows()
        self.tetromino = Tetromino(
            self.get_next_shape(),
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

        # checking horizontal movemnt
        if not self.timers["horizontal move"].active:
            if keys[pygame.K_LEFT]:
                self.tetromino.move_horizontal(-1)
                self.timers["horizontal move"].activate()
            if keys[pygame.K_RIGHT]:
                self.tetromino.move_horizontal(1)
                self.timers["horizontal move"].activate()
        # check for rotation
        if not self.timers["rotate"].active:
            if keys[pygame.K_UP]:
                self.tetromino.rotate()
                self.timers["rotate"].activate()
        if not self.down_pressed and keys[pygame.K_DOWN]:
            self.down_pressed = True
            self.timers["vertical move"].duration = self.down_speed_faster

        if self.down_pressed and not keys[pygame.K_DOWN]:
            self.down_pressed = False
            self.timers["vertical move"].duration = self.down_speed

    def check_finished_rows(self):
        # get the full rows indexes
        delete_rows = []
        for index, row in enumerate(self.field_data):
            if all(row):
                delete_rows.append(index)
        if delete_rows:
            for delete_row in delete_rows:
                for block in self.field_data[delete_row]:
                    block.kill()

                # move done blocks
                for row in self.field_data:
                    for block in row:
                        if block and block.pos.y < delete_row:
                            block.pos.y += 1

            self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
            for block in self.sprites:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block
            self.calculate_score(len(delete_rows))

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
        self.shape = shape
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

    # rotate
    def rotate(self):
        if self.shape != "O":
            # 1. pivot point
            pivot_pos = self.blocks[0].pos

            # 2. new block positions
            new_block_positions = [block.rotate(pivot_pos) for block in self.blocks]

            # 3. check for collisions
            for pos in new_block_positions:
                # horizontal check
                if pos.x < 0 or pos.x >= COLUMNS:
                    return
                # field check
                if self.field_data[int(pos.y)][int(pos.x)]:
                    return
                # floor check
                if pos.y > ROWS:
                    return
            for index, block in enumerate(self.blocks):
                block.pos = new_block_positions[index]


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

    def rotate(self, pivot_pos):
        # distance = self.pos - pivot_pos
        # rotated = distance.rotate(90)
        # new_pos = pivot_pos + rotated
        # return new_pos
        return pivot_pos + (self.pos - pivot_pos).rotate(90)

    def update(self):
        self.rect.topleft = self.pos * CELL_SIZE
