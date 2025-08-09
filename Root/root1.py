def root(degree, value, guess, tolerance=0.00000001, iteration=1, show_process=False):
    """
    使用迭代法(类似牛顿法)计算一个数的n次方根。
    Parameters:
        degree (int): 根的次数(n次方根中的n)。
        value (float): 要开方的数。
        guess (float): 初始猜测值。
        tolerance (float): 结果的精度。
        iteration (int): 当前迭代次数。
        show_process (bool): 是否打印迭代过程。
    Returns:
        float 或 str: 计算得到的根，或失败时返回'error'。
    """
    try:
        # 计算下一个猜测值
        next_guess = (value + (degree - 1) * guess ** degree) / (degree * guess ** (degree - 1))
        # 判断是否满足精度要求
        if abs(next_guess - guess) < tolerance:
            return next_guess
        else:
            # 如果不满足精度要求，则继续迭代
            if show_process:
                # 打印迭代过程
                print(f"{next_guess}     +({next_guess - guess})     Iteration {iteration}")
            return root(degree, value, next_guess, tolerance, iteration + 1, show_process)
    except Exception as e:
        # 如果出现异常，则返回'error'
        return 'error'

if __name__ == "__main__":
    print(root(9, 20, 10, show_process=True))