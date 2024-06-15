from lxml import etree as ET
import math
import os
import sys






print("""
***************************
这是一个快速进行每一次移动后的延时计算的程序，专门针对于编程挑战赛，但请注意：
- 因为会直接紧随在每一次移动之后，所以灯的变换需要 放在移动指令之前 / 在运行这个工具之后把灯放前面来 / 先别写
- 请使用那种从头到尾都是直线移动的编写格式，不要用什么标定点什么的
- delay计算直接使用辅助计算的公式（逆向），我个人认为还算是可以用的，另外的话据说无人机不会读百位之后的延时，而且可以增加100延时增加稳定性，所以写了它
- 多次运行会叠加多个delay，所以可以先把delay全部删掉（del_block_delay）之后再一次运行，请注意会删首个解锁后的延时（或者你自然可以多写几个start at把延时代替掉解决这个问题）
- 已实现：输入首个坐标（无需手动计算），精确到百位，统一添加延迟
+++++++++
使用说明
1、请将该文件扔进每一个动作组文件夹（或者你想要进行block_delay计算的动作组）中
2、编写好指定的形式后（无论你用小鸟飞飞还是pyfii）在每个文件夹中运行它
3、根据提示运行
***************************
""")






# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    script_dir = os.path.dirname(sys.executable)
elif __file__:
    script_dir = os.path.dirname(__file__)

# 此函数读取 XML 文件并返回树对象
def read_xml(filename):
    with open(filename, 'rb') as file:
        return ET.parse(file)


# 此函数计算两个坐标之间的延迟
def calculate_delay(previous_coords, current_coords, hspeed, acc,need_accurateTo100th,delay_addTime:int):
    # 获取两个坐标点的值
    ax, ay, az = previous_coords
    bx, by, bz = current_coords

    # 计算两点之间的距离
    distance = math.sqrt((float(bx) - float(ax)) ** 2 + (float(by) - float(ay)) ** 2 + (float(bz) - float(az)) ** 2)

    # 计算预计时间
    num7 = float(hspeed) if hspeed else 0.0
    num8 = float(acc) if acc else 0.0

    num10 = num7 / num8
    num11 = 0.5 * num8 * num10 ** 2

    if num11 > distance / 2:
        pre_time = int(round((2 * ((2 * num8 * distance / 2) ** 0.5) / num8) * 1000))
    else:
        pre_time = int(round(((num7 / num8) * 2 * 1000) + ((distance - (num11 * 2)) / num7) * 1000))

    #精确至百位
    if need_accurateTo100th:
        pre_time = math.ceil(pre_time / 100) * 100

    pre_time += delay_addTime

    return pre_time

# 此函数将格式化后的 XML 树写入到新文件
def write_xml(tree, filename):
    with open(filename, 'wb') as file:
        tree.write(file, pretty_print=True, xml_declaration=False, encoding='UTF-8')




def main(input_file,output_file,hspeed,acc,delay_addTime,first_coords,need_accurateTo100th):



    # 读取 XML 文件
    tree = read_xml(input_file)

    # 获取根节点，适应命名空间
    root = tree.getroot()
    ns = {'default_ns': root.nsmap[None]}

    # 找到所有的 Goertek_MoveToCoord 块
    move_to_coord_blocks = root.xpath('//default_ns:block[@type="Goertek_MoveToCoord"]', namespaces=ns)

    # 上一个坐标的坐标值初始化为first_coords
    previous_coords = first_coords

    # 遍历所有的 Goertek_MoveToCoord 块
    for block in move_to_coord_blocks:
        # 读取当前块下的坐标值
        current_coords = (
            block.find('default_ns:field[@name="X"]', namespaces=ns).text,
            block.find('default_ns:field[@name="Y"]', namespaces=ns).text,
            block.find('default_ns:field[@name="Z"]', namespaces=ns).text
        )

        # 如果存在前一个坐标块，则计算延迟
        if previous_coords:
            delay = calculate_delay(previous_coords, current_coords, hspeed, acc , need_accurateTo100th,delay_addTime)

            # 创建 block_delay 块
            delay_block = ET.Element('{{{}}}block'.format(ns['default_ns']), attrib={'type': 'block_delay'})
            delay_field_time = ET.SubElement(delay_block, '{{{}}}field'.format(ns['default_ns']), attrib={'name': 'time'})
            delay_field_time.text = str(delay)
            delay_field_delay = ET.SubElement(delay_block, '{{{}}}field'.format(ns['default_ns']), attrib={'name': 'delay'})
            delay_field_delay.text = '0'  # 或您计算出的正确值

            # 检查当前块是否有 <next>
            next_tag = block.find('default_ns:next', namespaces=ns)
            if next_tag is not None:
                next_content = next_tag.getchildren()
                delay_next_tag = ET.SubElement(delay_block, '{{{}}}next'.format(ns['default_ns']))
                delay_next_tag.extend(next_content)  # 转移 next 内容
                next_tag.clear()  # 清除原有内容
                next_tag.append(delay_block)  # 插入 block_delay
            else:
                # 直接创建 <next> 且不转移任何内容
                next_tag = ET.SubElement(block, '{{{}}}next'.format(ns['default_ns']))
                next_tag.append(delay_block)  # 插入 block_delay
        # 更新前一个坐标值以供下次循环使用
        previous_coords = current_coords


    # 将修改后的 XML 树写入到新文件
    write_xml(tree, output_file)

    print(f"The modified XML has been saved to {output_file}.")


if __name__ == '__main__':
    # 用户输入原文件路径，默认为 'webCodeAll.xml'
    input_file = input("请输入原文件路径（默认为当前目录下的 'webCodeAll.xml'）：") or 'webCodeAll.xml'

    # 用户输入水平速度（VH）和加速度（AH），默认为 200 和 400
    hspeed = int(input("请输入水平速度（VH），默认为 200：") or 200)
    acc = int(input("请输入加速度（AH），默认为 400：") or 400)
    delay_addTime = int(input("请输入延迟添加值，默认为 100：") or 100)
    first_coords=None
    if input("是否输入起飞后的第一个坐标：y or Y，其他为否").strip().lower() == 'y':
        first_coords= (int(input("第一个坐标的X值（起飞后）：")),int(input("第一个坐标的Y值（起飞后）：")),int(input("第一个坐标的Z值（起飞后）：")))

    need_accurateTo100th = False
    if input("是否需要精确至百位：y or Y，其他为否").strip().lower() == 'y':
        need_accurateTo100th = True

    if input("是否覆盖文件？（输入'y'或'Y'覆盖，其他情况不覆盖）: ").strip().lower() == 'y':
        output_file = input_file
    else:
        # 用户输入输出文件名，默认为 'modified_webCodeAll.xml'
        output_file = os.path.join(script_dir,input("请输入输出文件名（默认为 'modified_webCodeAll.xml'）：") or 'modified_webCodeAll.xml')
    main(input_file,output_file,hspeed,acc,delay_addTime,first_coords,need_accurateTo100th)