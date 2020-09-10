import pygame
import random

pygame.init()
display_width = 450
display_height = 600
surface = pygame.display.set_mode((display_width, display_height))
icon = pygame.image.load("tetris_ico.png")
pygame.display.set_caption('Tetris game')
pygame.display.set_icon(icon)
play_width = 280
play_height = 560
blocks_size = 28

top_left_x = 12
top_left_y = 10

# Позиционирование блоков
I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

blocks = [I, O, S, Z, J, L, T]
blocks_color = [(39, 225, 20), (29, 23, 218), (5, 175, 164), (204, 21, 21), (240, 240, 16), (239, 12, 225),
                (255, 255, 255)]
rows = 20  # y
columns = 10  # x
fall_speed_levels = [0.5, 0.4, 0.3, 0.2, 0.1]
game_score = 0
current_level = 1


class Block(object):
    def __init__(self, x, y, block):
        self.x = x
        self.y = y
        self.block = block
        self.color = blocks_color[blocks.index(block)]
        self.rotation = 0


def create_grid(locked_pos=None):
    if locked_pos is None:
        locked_pos = {}
    grid = [[(20, 20, 20) for x in range(10)] for x in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j, i)]
                grid[i][j] = c
    return grid


def get_block():
    global blocks
    random_num = random.randrange(0, 7, 1)
    return Block(5, 0, blocks[random_num])


def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y
    for i in range(len(grid)):
        pygame.draw.line(surface, (63, 63, 63), (sx, sy + i * blocks_size), (sx + play_width, sy + i * blocks_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (63, 63, 63), (sx + j * blocks_size, sy),
                             (sx + j * blocks_size, sy + play_height))


def draw_window(surface, grid):
    global game_score, current_level
    surface.fill((170, 200, 230))
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 26)
    label = font.render('TETRIS for FPGA', 1, (29, 23, 218))
    surface.blit(label, (299, 18))

    label2 = font.render('Score: ' + str(game_score), 1, (29, 23, 218))
    surface.blit(label2, (325, 310))

    label3 = font.render('Level: ' + str(current_level), 1, (29, 23, 218))
    surface.blit(label3, (325, 440))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j],
                             (top_left_x + j * blocks_size, top_left_y + i * blocks_size, blocks_size, blocks_size), 0)
    pygame.draw.rect(surface, (248, 178, 4), (top_left_x, top_left_y, play_width, play_height), 4)

    draw_grid(surface, grid)


def post_production_block_format(block):
    poses = []
    form = block.block[block.rotation % len(block.block)]

    for i, line in enumerate(form):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                poses.append((block.x + j, block.y + i))
    for i, pos in enumerate(poses):
        poses[i] = (pos[0] - 2, pos[1] - 4)
    return poses


def valid_space(block, grid):
    access_pos = [[(j, i) for j in range(10) if grid[i][j] == (20, 20, 20)] for i in range(20)]
    access_pos = [j for sub in access_pos for j in sub]

    formatted = post_production_block_format(block)

    for pos in formatted:
        if pos not in access_pos:
            if pos[1] > -1:
                return False
    return True


def check_lost(poses):  # chek на lost game
    for pos in poses:
        x, y = pos
        if y < 1:
            return True
    return False


def draw_next_block(block, surface):
    font = pygame.font.SysFont('comicsans', 26)
    label = font.render('Next Block', 1, (29, 23, 218))
    sx = 299
    sy = 115
    form = block.block[block.rotation % len(block.block)]

    for i, line in enumerate(form):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, block.color,
                                 (sx + j * blocks_size, sy + i * blocks_size, blocks_size, blocks_size), 0)
    surface.blit(label, (sx + 24, sy - 30))


def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (20, 20, 20) not in row:
            inc += 1
            index = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < index:
                new_key = (x, y + inc)
                locked[new_key] = locked.pop(key)
    return inc


def main_game():
    global surface, blocks, blocks_color, fall_speed_levels, game_score, current_level
    locked_pos = {}
    grid = create_grid(locked_pos)

    change_block = False
    game_actions = True
    current_block = get_block()
    next_block = get_block()
    clock = pygame.time.Clock()
    fall_time = 0
    current_level = 1
    fall_speed = fall_speed_levels[current_level - 1]
    game_score = 0

    while game_actions:
        grid = create_grid(locked_pos)
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_block.y += 1
            if not (valid_space(current_block, grid)) and current_block.y > 0:
                current_block.y -= 1
                change_block = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_actions = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    current_block.y += 1
                    if not (valid_space(current_block, grid)):
                        current_block.y -= 1
                if event.key == pygame.K_LEFT:
                    current_block.x -= 1
                    if not (valid_space(current_block, grid)):
                        current_block.x += 1
                if event.key == pygame.K_RIGHT:
                    current_block.x += 1
                    if not (valid_space(current_block, grid)):
                        current_block.x -= 1
                if event.key == pygame.K_UP:
                    current_block.rotation += 1
                    if not (valid_space(current_block, grid)):
                        current_block.rotation -= 1

        block_pos = post_production_block_format(current_block)

        for i in range(len(block_pos)):
            x, y = block_pos[i]
            if y > -1:
                grid[y][x] = current_block.color

        if change_block:
            for pos in block_pos:
                p = (pos[0], pos[1])
                locked_pos[p] = current_block.color
            current_block = next_block
            next_block = get_block()
            change_block = False
            number_cleared = clear_rows(grid, locked_pos)
            if number_cleared == 1:
                game_score += 100
            elif number_cleared == 2:
                game_score += 300
            elif number_cleared == 3:
                game_score += 700
            elif number_cleared == 4:
                game_score += 1500
        if game_score < 100:
            current_level = 1
        elif 300 > game_score >= 100:
            current_level = 2
        elif 1000 > game_score >= 300:
            current_level = 3
        elif 2000 > game_score >= 1000:
            current_level = 4
        else:
            current_level = 5
        fall_speed = fall_speed_levels[current_level - 1]
        draw_window(surface, grid)
        draw_next_block(next_block, surface)
        pygame.display.update()

        if check_lost(locked_pos):
            game_actions = False

    pygame.display.quit()


main_game()
