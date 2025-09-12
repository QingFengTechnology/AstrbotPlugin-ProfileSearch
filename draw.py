import io
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import emoji


RESOURCE_DIR: Path = Path(__file__).resolve().parent / "Asset"
FONT_PATH: Path = RESOURCE_DIR / "HarmonyOS_Sans.ttf"
EMOJI_FONT_PATH: Path = RESOURCE_DIR / "NotoColorEmoji.ttf"

FONT_SIZE = 35  # 字体大小
TEXT_PADDING = 10  # 文本与边框的间距
AVATAR_SIZE = None  # 头像大小（None 表示与文本高度一致）
BORDER_THICKNESS = 10  # 边框厚度
BORDER_COLOR_RANGE = (64, 255)  # 边框颜色范围
CORNER_RADIUS = 30  # 圆角大小

# 加载主字体
cute_font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

def get_emoji_font(desired_size):
    """获取适当大小的Emoji字体，确保与主字体大小一致"""
    try:
        # 首先尝试直接设置所需大小
        font = ImageFont.truetype(EMOJI_FONT_PATH, desired_size)
        print(f"成功加载Emoji字体，大小: {desired_size}")
        return font
    except OSError as e:
        print(f"无法加载指定大小的Emoji字体: {e}")
        try:
            # 尝试加载默认字体
            default_font = ImageFont.truetype(EMOJI_FONT_PATH)
            print(f"使用默认大小的Emoji字体: {default_font.size}")
            
            # 如果默认字体大小与期望大小差异较大，尝试重新加载接近的大小
            if abs(default_font.size - desired_size) > 5:
                try:
                    adjusted_font = ImageFont.truetype(EMOJI_FONT_PATH, desired_size)
                    return adjusted_font
                except:
                    pass
            return default_font
        except OSError as e:
            print(f"无法加载Emoji字体，使用主字体替代: {e}")
            # 最终fallback到主字体
            return ImageFont.truetype(FONT_PATH, desired_size)

# 获取Emoji字体
emoji_font = get_emoji_font(FONT_SIZE)


def create_image(avatar: bytes, reply: list) -> bytes:
    reply_str = "\n".join(reply)
    # 创建临时图片计算文本的宽高，得到最图片高度
    temp_img = Image.new("RGBA", (1, 1))
    temp_draw = ImageDraw.Draw(temp_img)
    no_emoji_reply = "".join("一" if emoji.is_emoji(c) else c for c in reply_str)
    text_bbox = temp_draw.textbbox((0, 0), no_emoji_reply, font=cute_font)
    text_width, text_height = (
        int(text_bbox[2] - text_bbox[0]),
        int(text_bbox[3] - text_bbox[1]),
    )
    img_height = text_height + 2 * TEXT_PADDING
    # 调整头像为与文本高度相同的大小，得到图片的宽度
    avatar_img = Image.open(BytesIO(avatar))
    avatar_size = AVATAR_SIZE if AVATAR_SIZE else text_height
    avatar_img = avatar_img.resize((avatar_size, avatar_size))
    img_width = avatar_img.width + text_width + 2 * TEXT_PADDING
    # 直接粘贴头像到图片左侧,垂直居中
    img = Image.new("RGBA", (img_width, img_height), color=(255, 255, 255, 255))
    img.paste(avatar_img, (0, (img_height - avatar_size) // 2))
    # 绘制文本到图片右侧
    _draw_multi(img, reply_str, avatar_img.width + TEXT_PADDING, TEXT_PADDING)
    # 绘制一个随机颜色的边框
    border_color = (38, 38, 38)  # HEX #262626
    border_img = Image.new(
        mode="RGBA",
        size=(img_width + BORDER_THICKNESS * 2, img_height + BORDER_THICKNESS * 2),
        color=border_color,
    )
    border_img.paste(img, (BORDER_THICKNESS, BORDER_THICKNESS))

    img_byte_arr = io.BytesIO()
    border_img.save(img_byte_arr, format="PNG")
    img_byte_arr = img_byte_arr.getvalue()

    return img_byte_arr


def _draw_multi(img, text, text_x=10, text_y=10):
    """
    在图片上绘制多语言文本（支持中英文、Emoji、符号和换行符）。
    如果emoji库不可用，则跳过emoji的特殊处理。
    """
    lines = text.split("\n")  # 按换行符分割文本
    current_y = text_y
    draw = ImageDraw.Draw(img)

    # 遍历每一行文本
    for line in lines:
        line_color = (
            random.randint(0, 128),
            random.randint(0, 128),
            random.randint(0, 128),
            random.randint(240, 255),
        )
        current_x = text_x
        for char in line:
            if char in emoji.EMOJI_DATA:
                # 使用统一的字体大小计算，确保Emoji和文本对齐
                draw.text((current_x, current_y), char, font=emoji_font, fill=line_color)
                # 使用主字体计算bbox以确保一致的间距
                bbox = cute_font.getbbox("中")  # 使用中文字符作为参考
            else:
                draw.text((current_x, current_y), char, font=cute_font, fill=line_color)
                bbox = cute_font.getbbox(char)
            current_x += bbox[2] - bbox[0]
        current_y += FONT_SIZE + 5  # 使用固定的行高，基于字体大小

    return img