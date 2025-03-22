
import random
import os
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

from astrbot import logger

# 尝试导入emoji模块，如果不存在，则设置一个标志
try:
    import emoji
    EMOJI_AVAILABLE = True
except ImportError:
    EMOJI_AVAILABLE = False
    logger.error("警告: astrbot_plugin_box依赖的 emoji 库未安装。请在控制台运行以下命令进行安装:\n\tpip install emoji")

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

font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

def create_image(avatar: bytes, reply: list):
    reply_str = "\n".join(reply)
    # 创建临时图片计算文本的宽高，得到最图片高度
    temp_img = Image.new('RGB', (1, 1))
    temp_draw = ImageDraw.Draw(temp_img)
    text_bbox = temp_draw.textbbox((0, 0), reply_str, font=font)
    text_width, text_height = int(text_bbox[2] - text_bbox[0]), int(text_bbox[3] - text_bbox[1])
    img_height = text_height + 2 * TEXT_PADDING
    # 调整头像为与文本高度相同的大小，得到图片的宽度
    avatar_img = Image.open(BytesIO(avatar))
    avatar_size = AVATAR_SIZE if AVATAR_SIZE else text_height
    avatar_img = avatar_img.resize((avatar_size, avatar_size))
    img_width = avatar_img.width + text_width + 2 * TEXT_PADDING
    # 头像圆角后粘贴到图片左侧,垂直居中
    img = Image.new('RGB', (img_width, img_height), color=(255, 255, 255))
    mask = Image.new('L', (avatar_size, avatar_size), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), (avatar_size, avatar_size)], CORNER_RADIUS, fill=255)
    avatar_img.putalpha(mask)
    img.paste(avatar_img, (0, (img_height - avatar_size) // 2), mask)
    # 绘制文本到图片右侧
    _draw_multi(img, reply_str, FONT_SIZE, avatar_img.width + TEXT_PADDING, TEXT_PADDING)
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
    border_img.paste(img, (BORDER_THICKNESS, BORDER_THICKNESS))

    # 保存图片到缓存路径
    target_id = reply[0].split("：")[1]
    img_name = f"info_{target_id}.png"
    img_path = os.path.join(TEMP_DIR, img_name)
    border_img.save(img_path, format='PNG')
    return img_path




def _draw_multi(img, text, font_size=35, text_x=10, text_y=10):
    """
    在图片上绘制多语言文本（支持中英文、Emoji、符号和换行符）。
    如果emoji库不可用，则跳过emoji的特殊处理。
    """
    # 加载字体
    cute_font = ImageFont.truetype(FONT_PATH, font_size)
    # 仅当emoji库可用时加载emoji字体
    if EMOJI_AVAILABLE:
        try:
            emoji_font = ImageFont.truetype(EMOJI_FONT_PATH, font_size)
        except IOError:
            # 如果指定的emoji字体路径无效，仍继续使用普通字体
            emoji_font = cute_font
    else:
        emoji_font = cute_font  # 当emoji不可用时，使用普通字体代替

    lines = text.split("\n")  # 按换行符分割文本
    current_y = text_y
    draw = ImageDraw.Draw(img)

    # 遍历每一行文本
    for line in lines:
        line_color = (random.randint(0, 128), random.randint(0, 128), random.randint(0, 128))
        current_x = text_x
        for char in line:
            if EMOJI_AVAILABLE and char in emoji.EMOJI_DATA:
                draw.text((current_x, current_y + 10), char, font=emoji_font, fill=line_color)
            else:
                draw.text((current_x, current_y), char, font=cute_font, fill=line_color)
            bbox = cute_font.getbbox(char)
            current_x += bbox[2] - bbox[0]
        current_y += 40
    return img

# 确保在调用_draw_multi前已经尝试了导入emoji
if not EMOJI_AVAILABLE:
    print("警告: emoji库未安装。将不支持emoji的特殊处理。")
