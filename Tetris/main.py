import pygame
import random

# 初始化pygame
pygame.init()

# 设置窗口大小
screen = pygame.display.set_mode((600, 800))#40*15 20*40
# 设置时钟
clock = pygame.time.Clock()
# 设置帧率
TICK = 0.8
score = 0
# 定义常用颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
run = True

data_list = []
block_list = [
    [[0,-2],[0,-1],[0,0],[0,1]],      # I型
    [[0,0],[1,0],[0,1],[1,1]],        # O型
    [[0,0],[-1,0],[0,1],[1,1]],       # S型
    [[0,0],[1,0],[0,1],[-1,1]],       # Z型
    [[0,0],[-1,0],[1,0],[0,1]],       # T型
    [[0,0],[-1,0],[-1,1],[0,1]],      # L型
    [[0,0],[1,0],[1,1],[0,1]]         # J型
]
# 随机返回一个已定义颜色
def random_color():
    colors = [RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA]
    return random.choice(colors)
# 初始化函数
def init():
    global data_list
    data_list = []
    for x in range(15):
        data_list.append([])
        for y in range(20):
            data_list[x].append(BLACK)  # 初始化为黑色
init()
# 打印数据列表
def print_data_list():
    for x in range(15):
        for y in range(20):
            draw(data_list[x][y], x, y)

# 绘制函数
def draw(color, x, y):
    pygame.draw.rect(screen, color, (x*40, y*40, 40, 40))

# 定义方块类
class Block:
    def __init__(self, color, x, y, list=[]):
        self.color = color
        self.x = x
        self.y = y
        self.list = list
        for i in self.list:
            if not (0 <= self.x + i[0] < 15 and 0 <= self.y + i[1] < 20):
                continue  # 如果方块越界，则跳过
            # 检查当前位置是否有方块
            if data_list[self.x + i[0]][self.y + i[1]] != BLACK:
                end_game()
                print("Game Over")
                return
    def drawtoscreen(self):
        for i in self.list:
            if 0 <= self.x + i[0] < 15 and 0 <= self.y + i[1] < 20:
                data_list[self.x+i[0]][self.y+i[1]] = self.color
    def drawdown(self):
        for i in self.list:
            if 0 <= self.x + i[0] < 15 and 0 <= self.y + i[1] < 20:
                data_list[self.x+i[0]][self.y+i[1]] = BLACK
    def hasdown(self):
        for i in self.list:
            new_x = self.x + i[0]
            new_y = self.y + i[1] + 1
            # 如果下方是同一个方块的单元，跳过检测
            if [i[0], i[1]+1] in self.list:
                continue
            # 检查下方是否越界
            if not (0 <= new_x < 15 and 0 <= new_y < 20):
                return False
            # 检查下方是否有方块（只在有效范围内检测）
            if new_y >= 0 and data_list[new_x][new_y] != BLACK:
                return False
        return True
    def hasright(self):
        for i in self.list:
            # 如果右方是同一个方块的单元，跳过检测
            if [i[0]+1, i[1]] in self.list:
                continue
            # 检查右方是否越界（允许上方越界）
            if not (0 <= self.x + i[0]+1 < 15 and self.y + i[1] < 20):
                return False
            # 检查右方是否有方块（只在有效范围内检测）
            if self.y + i[1] >= 0 and data_list[self.x+i[0]+1][self.y+i[1]] != BLACK:
                return False
        return True
    def hasleft(self):
        for i in self.list:
            # 如果左方是同一个方块的单元，跳过检测
            if [i[0]-1, i[1]] in self.list:
                continue
            # 检查左方是否越界（允许上方越界）
            if not (0 <= self.x + i[0]-1 < 15 and self.y + i[1] < 20):
                return False
            # 检查左方是否有方块（只在有效范围内检测）
            if self.y + i[1] >= 0 and data_list[self.x+i[0]-1][self.y+i[1]] != BLACK:
                return False
        return True
    def hasturn(self):
        temp = []
        for i in self.list:
            temp.append([-i[1], i[0]])  # 正确的旋转变换
        for i in temp:
            # 检查旋转后是否越界
            if not (0 <= self.x + i[0] < 15 and 0 <= self.y + i[1] < 20):
                print("旋转后越界")
                return False
            # 检查旋转后位置是否有方块
            if data_list[self.x + i[0]][self.y + i[1]] != BLACK:
                if [i[0], i[1]] not in self.list:
                    return False
        return True
    def haschong(self):
        for i in self.list:
            # 检查下方是否越界（允许上方越界）
            if not (0 <= self.x + i[0] < 15 and self.y + i[1]+1 < 20):
                return False
            # 检查当前位置是否有方块（只在有效范围内检测）
            if self.y + i[1] >= 0 and data_list[self.x+i[0]][self.y+i[1]] != BLACK:
                return False
        return True
    def queren(self):
        # 先锁定方块
        affected_rows = set()
        for i in self.list:
            if self.y + i[1] >= 0:
                data_list[self.x + i[0]][self.y + i[1]] = self.color
                affected_rows.add(self.y + i[1])
        # 检查并消除满行
        rows_to_clear = []
        for y in affected_rows:
            if 0 <= y < 20 and all(data_list[x][y] != BLACK for x in range(15)):
                rows_to_clear.append(y)
        for y in sorted(rows_to_clear, reverse=True):
            print("消除行:", y)
            global score
            score += 10
            for move_y in range(y, 0, -1):
                for x in range(15):
                    data_list[x][move_y] = data_list[x][move_y-1]
            for x in range(15):
                data_list[x][0] = BLACK
        thelist[0] = Block(random_color(), 7, 0, random.choice(block_list))
    
def end_game():
    global run
    run = False
    font = pygame.font.SysFont(None, 72)
    text = font.render('Game Over', True, RED)
    text2 = font.render('Score: '+str(score), True, WHITE)
    screen.fill(BLACK)
    screen.blit(text, (150, 350))
    screen.blit(text2, (150, 450))
    pygame.display.flip()
    pygame.time.wait(2000)

thetick = 0
block = Block(random_color(), 7, 0, random.choice(block_list))
thelist = [block]
while True:
    if run:
        thetick += 1
        #print(thetick%18 == 0)1
        thelist[0].drawtoscreen()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and run:
                if thelist[0].hasleft():
                    thelist[0].drawdown()
                    thelist[0].x -= 1
                    thelist[0].drawtoscreen()
            elif event.key == pygame.K_RIGHT and run:
                if thelist[0].hasright():
                    thelist[0].drawdown()
                    thelist[0].x += 1
                    thelist[0].drawtoscreen()
            elif event.key == pygame.K_DOWN and run:
                if thelist[0].hasdown():
                    thelist[0].drawdown()
                    thelist[0].y += 1
                    thelist[0].drawtoscreen()
                else:
                    thelist[0].queren()
            elif event.key == pygame.K_UP and run:
                if thelist[0].hasturn():
                    thelist[0].drawdown()
                    ztemp = []
                    for i in thelist[0].list:
                        ztemp.append([-i[1], i[0]])
                    thelist[0].list = ztemp
                    thelist[0].drawtoscreen()
    if thetick%18==0 and run:
        if thelist[0].hasdown():
            thelist[0].drawdown()
            thelist[0].y += 1
            thelist[0].drawtoscreen()
        else:
            thelist[0].queren()
            thelist[0] = Block(random_color(), 7, 0, random.choice(block_list))

    screen.fill(BLACK)  # Fill the screen with black
    print_data_list()  # Print the data list
    pygame.display.flip()  # Update the display
    clock.tick(30)  