import math

def parabolic_question(ground_angle, parabolic_angle, v,step=1, set_tolerance=0.00000001, guess=0, g=9.8):
    # 定义全局变量time
    global time
    # time自增1
    time += 1
    try:
        # 直接解析解：沿斜面的射程
        R = (2 * v**2 * math.cos(parabolic_angle) * math.sin(parabolic_angle - ground_angle)) / (g * math.cos(ground_angle)**2)
        # 返回水平投影距离
        return R * math.cos(ground_angle)
    except Exception as e:
        # 捕获异常并返回异常信息
        return e
