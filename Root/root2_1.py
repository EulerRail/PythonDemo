import math

def parabolic_question(ground_angle, parabolic_angle, v, step=1, set_tolerance=0.00001, guess=0, g=9.8):
    """
    计算抛物线问题水平距离.
    Parameters:
        ground_angle (float): 地面的角度（弧度）。
        parabolic_angle (float): 抛物线的角度（弧度）。
        v (float): 初始速度。
        g (float): 重力加速度,默认为9.8 m/s².
    Returns:
        float: 抛物线落点距离.
    """
    # 判断角度是否在0到90度之间
    if not (0 <= ground_angle < math.pi/2) or not (0 <= parabolic_angle < math.pi/2) or ground_angle >= parabolic_angle:
        return '角度必须在0到90度之间'
    # 判断速度是否大于0
    if v <= 0:
        return '速度必须大于0'
    try:
        guess += step
        # 计算抛物线在水平方向上的距离
        y1 = guess * math.tan(parabolic_angle) - (g * guess ** 2) / (2 * v * v * math.cos(parabolic_angle) ** 2)
        # 计算地面在水平方向上的距离
        y2 = guess * math.tan(ground_angle)
        # 计算两者之间的差值
        y = y1 - y2
        # 如果差值大于0，说明地面距离大于抛物线距离，需要增大猜测值
        if y > 0:
            return parabolic_question(ground_angle, parabolic_angle, v, step, set_tolerance, guess, g=g)
        # 如果差值等于0，说明地面距离等于抛物线距离，返回猜测值
        if y == 0:
            return guess
        # 如果差值小于0，说明地面距离小于抛物线距离，需要减小猜测值
        if y < 0:
            # 如果步长小于容忍度，说明已经找到最接近的值，返回猜测值
            if step <= set_tolerance:
                return guess
            # 否则，减小步长，继续猜测
            else:
                newstep = step / 10
                return parabolic_question(ground_angle, parabolic_angle, v, newstep, set_tolerance, guess - step, g=g)
    except Exception as e:
        return 'error'

#，初始速度为10，计算抛物线落点距离
for g in range(1, 400):
    a = []
    for d in range(g+1, 899):
        # 计算抛物线落点距离
        new = parabolic_question(math.radians(g / 10), math.radians(d / 10), 2)  # 将初始速度改为20
        # 将结果添加到列表中
        a.append(new)
    # 找到列表中最大的值
    idx = a.index(max(a))
    # 打印结果
    print(str(g / 10), str(idx / 10 + g / 10), str(45 + 0.05 * g), str(max(a)))


