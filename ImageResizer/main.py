from PIL import Image
import sys


def expand_background_cli(input_path, output_path, width, height):
    """命令行版本的背景扩展函数"""
    try:
        original_image = Image.open(input_path)

        if original_image.mode != 'RGBA':
            original_image = original_image.convert('RGBA')

        new_image = Image.new('RGBA', (width, height), (0, 0, 0, 0))

        x_offset = (width - original_image.width) // 2
        y_offset = (height - original_image.height) // 2

        new_image.paste(original_image, (x_offset, y_offset), original_image)
        new_image.save(output_path, 'PNG')

        print(f"成功将 {input_path} 的背景扩展到 {width}x{height}，保存为 {output_path}")
        return True
    except Exception as e:
        print(f"错误: {e}")
        return False


# 使用示例
if __name__ == "__main__":
    if len(sys.argv) >= 3:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        width = int(sys.argv[3]) if len(sys.argv) > 3 else 1600
        height = int(sys.argv[4]) if len(sys.argv) > 4 else 1600

        expand_background_cli(input_file, output_file, width, height)
    else:
        print("用法: python script.py <输入文件> <输出文件> [宽度] [高度]")
        print("示例: python script.py input.png output.png 2000 2000")