def calculate_distance(ax, ay, az, bx, by, bz):
    num4 = float(bx) if bx else 0.0
    num5 = float(by) if by else 0.0
    num6 = float(bz) if bz else 0.0
    num = float(ax) if ax else 0.0
    num2 = float(ay) if ay else 0.0
    num3 = float(az) if az else 0.0

    num9 = ((num4 - num) ** 2 + (num5 - num2) ** 2 + (num6 - num3) ** 2) ** 0.5
    return int(round(num9))

def calculate_pre_time(acc, hspeed, distance):
    num7 = float(hspeed) if hspeed else 0.0
    num8 = float(acc) if acc else 0.0

    num10 = num7 / num8
    num11 = 0.5 * num8 * num10 ** 2

    if num11 > distance / 2:
        return int(round((2 * ((2 * num8 * distance / 2) ** 0.5) / num8) * 1000))
    else:
        return int(round(((num7 / num8) * 2 * 1000) + ((distance - (num11 * 2)) / num7) * 1000))

# 示例用法
ax = input("请输入AX的值：")
ay = input("请输入AY的值：")
az = input("请输入AZ的值：")
bx = input("请输入BX的值：")
by = input("请输入BY的值：")
bz = input("请输入BZ的值：")
hspeed = input("请输入HSpeed的值：")
acc = input("请输入Acc的值：")

distance = calculate_distance(ax, ay, az, bx, by, bz)
print(f"距离为：{distance} 米")

if acc and hspeed:
    pre_time = calculate_pre_time(acc, hspeed, distance)
    print(f"预计时间为：{pre_time} 毫秒")