import pygame
import sys
import random

# 初始化蛇和苹果的位置
snack = [[5, 4], [5, 5], [5, 6]]  # 蛇的每一节坐标
apple = [[10, 5]]  # 苹果坐标
forward = 1  # 初始方向，1为下
second = 0.3  # 移动间隔（秒）

# 初始化pygame窗口
pygame.init()
w = 1200  # 窗口宽度，60格*20像素
h = 900   # 窗口高度，45格*20像素
screen = pygame.display.set_mode((w, h))

# 游戏运行标志和时钟

run = 1
clock = pygame.time.Clock()
frame = 0
next_forward = forward

def turn(screen,x,y,color):
    """
    在指定位置绘制一个方块
    :param screen: pygame窗口对象
    :param x: 方块x坐标(格)
    :param y: 方块y坐标(格)
    :param color: 方块颜色
    """
    pygame.draw.rect(screen, color, (x * 20, y * 20, 20, 20))

def display(snack,apple):
    """
    绘制蛇和苹果
    :param snack: 蛇的坐标列表
    :param apple: 苹果的坐标列表
    """
    screen.fill((0, 0, 0))  # 清屏
    for a_snack in snack:
        turn(screen, a_snack[0], a_snack[1], [255, 255, 255])  # 白色蛇身
    if len(apple) != 0:
        for a_apple in apple:
            turn(screen, a_apple[0], a_apple[1], [255, 0, 0])  # 红色苹果
def stop():
    global run
    run = 0
def new_apple():
    global snack, apple
    x_min = max(0, snack[-1][0] - 10)
    x_max = min(59, snack[-1][0] + 10)
    y_min = max(0, snack[-1][1] - 10)
    y_max = min(44, snack[-1][1] + 10)
    new_apple = [random.randint(x_min, x_max), random.randint(y_min, y_max)]
    while (new_apple in snack) or (new_apple in apple):
        new_apple = [random.randint(x_min, x_max), random.randint(y_min, y_max)]
    apple.append(new_apple)  # 生成新的苹果

def move(snack, apple, forward):
    """
    移动蛇
    :param snack: 蛇的坐标列表
    :param apple: 苹果的坐标列表
    :param forward: 方向(0:上, 1:下, 2:左, 3:右)
    :return: 移动后的蛇坐标列表
    """
    head = snack[-1]
    # 根据forward的值来决定蛇头的移动方向
    if forward == 0:  # 上
        last = [head[0], head[1] - 1]
    elif forward == 1:  # 下
        last = [head[0], head[1] + 1]
    elif forward == 2:  # 左
        last = [head[0] - 1, head[1]]
    elif forward == 3:  # 右
        last = [head[0] + 1, head[1]]

    # 如果蛇头碰到自己，游戏结束
    if last in snack:
        if last == snack[-1]:
            pass  # 蛇头和尾巴重合，允许
        else:
            stop()
            return snack, apple

    # 如果蛇头碰到边界，游戏结束
    if last[0] < 0 or last[0] >= 60 or last[1] < 0 or last[1] >= 45:
        stop()
        return snack, apple

    snack.append(last)  # 添加新的蛇头
    if last in apple:   # 如果蛇头吃到苹果
        apple.remove(last)  # 移除苹果
        new_apple()
    else:
        snack.pop(0)  # 移除蛇尾
    return snack, apple
while True:
    # 主循环，每帧刷新一次
    pygame.display.get_active()  # 检查窗口激活状态（可选）
    for event in pygame.event.get():
        # 处理退出事件
        if event.type == pygame.QUIT:
            sys.exit()
        # 处理键盘事件，改变蛇的方向（只修改next_forward）
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if forward != 1:
                    next_forward = 0
            if event.key == pygame.K_DOWN:
                if forward != 0:
                    next_forward = 1
            if event.key == pygame.K_LEFT:
                if forward != 3:
                    next_forward = 2
            if event.key == pygame.K_RIGHT:
                if forward != 2:
                    next_forward = 3
    frame += 1
    # 每30帧移动一次蛇
    if frame % (30 * second) == 0 and run == 1:
        forward = next_forward
        snack, apple = move(snack, apple, forward)

    # 绘制界面
    screen.fill((0, 0, 0))
    display(snack, apple)
    if run == 0:
        font = pygame.font.SysFont(None, 72)
        text1 = font.render('END', True, (255, 0, 0))
        text2 = font.render('score: {}'.format(len(snack) - 3), True, (255, 0, 0))
        rect1 = text1.get_rect(center=(w // 2, h // 2 - 40))
        rect2 = text2.get_rect(center=(w // 2, h // 2 + 40))
        screen.blit(text1, rect1)
        screen.blit(text2, rect2)
    pygame.display.update()
    clock.tick(30)  # 控制帧率为30FPS
##################################################################
#================不要报错求求了+++++++++++++++++++++++++++++++
#+++++++++++++++++再出问题就tm把你删了