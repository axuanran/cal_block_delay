from lxml import etree as ET
import os

# 获取当前脚本所在的目录路径
script_dir = os.path.dirname(os.path.abspath(__file__))

# 切换到脚本所在的目录
os.chdir(script_dir)

def remove_and_relocate_next_blocks(xml_document, namespace):
    """
    Remove 'block_delay' blocks and relocate their 'next' blocks (if any) to their parent element.

    Args:
    - xml_document: Path to the XML document.
    - namespace: The namespace as a dictionary, e.g., {'ns': 'http://www.w3.org/1999/xhtml'}
    """
    # Parse the XML document
    tree = ET.parse(xml_document)
    root = tree.getroot()

    # Find all 'block_delay' blocks considering the namespace
    block_delays = root.xpath('//ns:block[@type="block_delay"]', namespaces=namespace)

    for block_delay in block_delays:
        # Find 'next' block within block_delay
        next_block = block_delay.find('ns:next', namespaces=namespace)

        if next_block is not None:
            # Temporarily store the contents of the 'next' block
            temp_content = list(next_block)

            # Remove the entire 'block_delay' block
            parent = block_delay.getparent()
            parent.remove(block_delay)

            # Append temporarily stored content to the parent of 'block_delay' block
            for elem in temp_content:
                parent.append(elem)
        else:
            # If there is no 'next' block, remove the 'block_delay' block
            parent = block_delay.getparent()
            parent.remove(block_delay)

    # Return the modified XML tree
    return tree

# Specify your XML document path and namespace
# 用户输入原文件路径，默认为 'webCodeAll.xml'
input_file = input("请输入原文件路径（默认为 'webCodeAll.xml'）：") or 'webCodeAll.xml'
namespace = {'ns': 'http://www.w3.org/1999/xhtml'}  # Replace with the actual namespace if different

# Call the function and save the result
modified_tree = remove_and_relocate_next_blocks(input_file, namespace)



if input("是否覆盖文件？（输入'y'或'Y'覆盖，其他情况不覆盖）: ").strip().lower() == 'y':
    output_file = input_file
else:
    # 用户输入输出文件名，默认为 'modified_webCodeAll.xml'
    output_file = input("请输入输出文件名（默认为 'modified_webCodeAll.xml'）：") or 'modified_webCodeAll.xml'


modified_tree.write(output_file, pretty_print=True, xml_declaration=False, encoding='UTF-8')