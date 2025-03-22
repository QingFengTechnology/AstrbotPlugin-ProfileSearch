
import random
import time
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os
try:
    import emoji
except ImportError as e:
    logger.error("astrbot_plugin_box依赖的 emoji 库未安装。请在控制台通过命令安装：pip install emoji")
    exit(1)

PLUGIN_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.join(PLUGIN_DIR, "resource", "可爱字体.ttf")
EMOJI_FONT_PATH = os.path.join(PLUGIN_DIR, "resource", "NotoColorEmoji.ttf")
TEMP_DIR = os.path.join(PLUGIN_DIR, "temp")
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)


FONT_SIZE = 35  # 字体大小
TEXT_PADDING = 10  # 文本与边框的间距
AVATAR_SIZE = None  # 头像大小（None 表示与文本高度一致）
BORDER_THICKNESS = 10  # 边框厚度
BORDER_COLOR_RANGE = (64, 255)  # 边框颜色范围
CORNER_RADIUS = 30  # 圆角大小

def create_image(avatar, info_str):
    # 加载字体文件
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    # 创建一个临时图片用于测量文本的大小
    temp_img = Image.new('RGB', (1, 1))
    temp_draw = ImageDraw.Draw(temp_img)
    # 获取文本的边界框（用于计算文本的宽度和高度）
    text_bbox = temp_draw.textbbox((0, 0), info_str, font=font)
    text_width, text_height = int(text_bbox[2] - text_bbox[0]), int(text_bbox[3] - text_bbox[1])
    # 计算最终图片的高度（文本高度加上上下边距）
    img_height = text_height + 2 * TEXT_PADDING
    # 打开头像图片（从二进制数据中加载）
    avatar_img = Image.open(BytesIO(avatar))
    # 将头像调整为与文本高度相同的大小（或自定义大小）
    avatar_size = AVATAR_SIZE if AVATAR_SIZE else text_height
    avatar_img = avatar_img.resize((avatar_size, avatar_size))
    # 计算最终图片的宽度（头像宽度 + 文本宽度 + 左右边距）
    img_width = avatar_img.width + text_width + 2 * TEXT_PADDING
    # 创建一个白色背景的图片
    img = Image.new('RGB', (img_width, img_height), color=(255, 255, 255))

    # 圆角,粘贴头像到图片的左侧,垂直居中
    mask = Image.new('L', (avatar_size, avatar_size), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), (avatar_size, avatar_size)], CORNER_RADIUS, fill=255)
    avatar_img.putalpha(mask)
    img.paste(avatar_img, (0, (img_height - avatar_size) // 2), mask)

    # 绘制文本到图片右侧
    _draw_multi(img, info_str, FONT_SIZE, avatar_img.width + TEXT_PADDING, TEXT_PADDING)

    # 绘制一个随机颜色的边框
    border_color = (
        random.randint(*BORDER_COLOR_RANGE),
        random.randint(*BORDER_COLOR_RANGE),
        random.randint(*BORDER_COLOR_RANGE)
    )
    border_img = Image.new(
        mode='RGB',
        size=(img_width + BORDER_THICKNESS * 2, img_height + BORDER_THICKNESS * 2),
        color=border_color
    )
    border_img.paste(img, (BORDER_THICKNESS, BORDER_THICKNESS))  # 将原图片粘贴到边框内

    # 生成唯一的文件名
    timestamp = int(time.time() * 1000)  # 毫秒级时间戳
    img_name = f"image_{timestamp}.png"
    img_path = os.path.join(TEMP_DIR, img_name)

    # 保存图片到指定路径
    border_img.save(img_path, format='PNG')

    # 返回图片路径
    return img_path



def _draw_multi(img, text, font_size=35, text_x=10, text_y=10):
    """
    在图片上绘制多语言文本（支持中英文、Emoji、符号和换行符）。
    """
    # 加载字体
    cute_font= ImageFont.truetype(FONT_PATH, font_size)
    emoji_font = ImageFont.truetype(EMOJI_FONT_PATH, font_size)

    lines = text.split("\n")  # 按换行符分割文本
    current_y = text_y
    draw = ImageDraw.Draw(img)

    # 遍历每一行文本
    for line in lines:
        line_color = (random.randint(0, 128), random.randint(0, 128), random.randint(0, 128))
        current_x = text_x
        for char in line:
            if char in emoji.EMOJI_DATA:
                draw.text((current_x, current_y + 10), char, font=emoji_font, fill=line_color)
            else:
                draw.text((current_x, current_y), char, font=cute_font, fill=line_color)

            bbox = cute_font.getbbox(char)
            current_x += bbox[2] - bbox[0]
        current_y += 40
    return img
