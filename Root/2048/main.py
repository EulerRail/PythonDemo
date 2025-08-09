import pygame
import sys
import random

NUM_COLOR_MAP = {
    0: (238, 228, 218),    # 空格，浅米色
    2: (255, 224, 178),    # 浅橙
    4: (255, 204, 128),    # 橙黄
    8: (255, 183, 77),     # 深橙
    16: (255, 167, 38),    # 橙色
    32: (255, 152, 0),     # 橙棕
    64: (255, 138, 101),   # 橙红
    128: (255, 112, 67),   # 深橙红
    256: (255, 87, 34),    # 红橙
    512: (255, 160, 122),  # 浅珊瑚
    1024: (255, 99, 71),   # 番茄红
    2048: (255, 69, 0),    # 橙红色
}

pygame.init()
run = True
data = [[0, 0, 0, 0], 
        [0, 0, 0, 0], 
        [0, 0, 0, 0], 
        [0, 0, 0, 0]]
WIDTH, HEIGHT = 400, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 Game")
clock = pygame.time.Clock()
text_font = pygame.font.Font(None, 36)

def can_move():
    # 检查是否有空格
    for i in range(4):
        for j in range(4):
            if data[i][j] == 0:
                return True
    # 检查是否有可合并的相邻格子
    for i in range(4):
        for j in range(4):
            if i < 3 and data[i][j] == data[i+1][j]:
                return True
            if j < 3 and data[i][j] == data[i][j+1]:
                return True
    return False
def win_game():
    global run
    run = False
    # 游戏胜利后，主循环负责持续显示 You Win!
def lose_game():
    global run
    run = False
    # 游戏结束后，主循环负责持续显示 Game Over
def new_number():
    e_list = []
    for i in range(4):
        for j in range(4):
            if data[i][j] == 0:
                e_list.append((i, j))
    if len(e_list) > 0:
        i, j = random.choice(e_list)
        data[i][j] = random.choice([2, 4])
        # 新数字生成后检查还能否继续
        if not can_move():
            lose_game()
    else:
        if not can_move():
            lose_game()
def draw_grid():
    for i in range(4):
        for j in range(4):
            num = data[i][j]
            color = NUM_COLOR_MAP[num]
            pygame.draw.rect(win, color, (j * 100, i * 100, 100, 100))
            if num != 0:
                text = text_font.render(str(num), True, (255, 255, 255))
                win.blit(text, (j * 100 + 50 - text.get_width() // 2, i * 100 + 50 - text.get_height() // 2))

def move_left():
    global data
    global run
    last_data = [row.copy() for row in data]
    for i in range(4):
        for j in range(1,4):
            if data[i][j] != 0:
                temp = data[i][j]
                k = j
                while k > 0 and data[i][k - 1] == 0:
                    data[i][k - 1] = data[i][k]
                    data[i][k] = 0
                    k -= 1
                if k > 0 and data[i][k - 1] == temp:
                    data[i][k - 1] *= 2
                    data[i][k] = 0
    if last_data != data:
        new_number()
    elif not can_move():
        lose_game()
def move_right():
    global data
    global run
    last_data = [row.copy() for row in data]
    for i in range(4):
        for j in range(2,-1,-1):
            if data[i][j] != 0:
                temp = data[i][j]
                k = j
                while k < 3 and data[i][k + 1] == 0:
                    data[i][k + 1] = data[i][k]
                    data[i][k] = 0
                    k += 1
                if k < 3 and data[i][k + 1] == temp:
                    data[i][k + 1] *= 2
                    data[i][k] = 0
    if last_data != data:
        new_number()
    elif not can_move():
        lose_game()
def move_up():
    global data
    global run
    last_data = [row.copy() for row in data]
    for j in range(4):
        for i in range(1,4):
            if data[i][j] != 0:
                temp = data[i][j]
                k = i
                while k > 0 and data[k - 1][j] == 0:
                    data[k - 1][j] = data[k][j]
                    data[k][j] = 0
                    k -= 1
                if k > 0 and data[k - 1][j] == temp:
                    data[k - 1][j] *= 2
                    data[k][j] = 0
    if last_data != data:
        new_number()
    elif not can_move():
        lose_game()
def move_down():
    global data
    global run
    last_data = [row.copy() for row in data]
    for j in range(4):
        for i in range(2,-1,-1):
            if data[i][j] != 0:
                temp = data[i][j]
                k = i
                while k < 3 and data[k + 1][j] == 0:
                    data[k + 1][j] = data[k][j]
                    data[k][j] = 0
                    k += 1
                if k < 3 and data[k + 1][j] == temp:
                    data[k + 1][j] *= 2
                    data[k][j] = 0
    if last_data != data:
        new_number()
    elif not can_move():
        lose_game()
new_number()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if run:
                if event.key == pygame.K_a:
                    move_left()
                if event.key == pygame.K_d:
                    move_right()
                if event.key == pygame.K_w:
                    move_up()
                if event.key == pygame.K_s:
                    move_down()
    win.fill((0,0,0))
    draw_grid()
    if not run:
        # 判断胜利还是失败
        has_2048 = any(2048 in row for row in data)
        text_font = pygame.font.Font(None, 64)
        if has_2048:
            win_text = text_font.render("You Win!", True, (255, 255, 255))
            win_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            win.blit(win_text, win_rect)
        else:
            lose_text = text_font.render("Game Over!", True, (255, 255, 255))
            lose_rect = lose_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            win.blit(lose_text, lose_rect)
    pygame.display.flip()
    clock.tick(60)
