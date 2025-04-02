from datetime import datetime
import aiohttp
from astrbot import logger


def timestamp_to_date(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp).strftime('%Y年')


def qqLevel_to_icon(level: int) -> str:
    icons = ['👑', '☀️', '🌙', '⭐']
    levels = [64, 16, 4, 1]
    result = ''
    original_level = level
    for icon, lvl in zip(icons, levels):
        count, level = divmod(level, lvl)
        result += icon * count
    result += f"({original_level}级)"
    return result


async def get_avatar(user_id: str) -> bytes:
    avatar_url = f"https://q4.qlogo.cn/headimg_dl?dst_uin={user_id}&spec=640"
    try:
        async with aiohttp.ClientSession() as client:
            response = await client.get(avatar_url, timeout=10)
            response.raise_for_status()
            return await response.read()
    except Exception as e:
        logger.error(f"下载头像失败: {e}")
        return b''


def get_constellation(month: int, day: int) -> str:
    constellations = {
        '白羊座': ((3, 21), (4, 19)),
        '金牛座': ((4, 20), (5, 20)),
        '双子座': ((5, 21), (6, 20)),
        '巨蟹座': ((6, 21), (7, 22)),
        '狮子座': ((7, 23), (8, 22)),
        '处女座': ((8, 23), (9, 22)),
        '天秤座': ((9, 23), (10, 22)),
        '天蝎座': ((10, 23), (11, 21)),
        '射手座': ((11, 22), (12, 21)),
        '摩羯座': ((12, 22), (1, 19)),
        '水瓶座': ((1, 20), (2, 18)),
        '双鱼座': ((2, 19), (3, 20))
    }

    for constellation, ((start_month, start_day), (end_month, end_day)) in constellations.items():
        if (month == start_month and day >= start_day) or (month == end_month and day <= end_day):
            return constellation
        # 特别处理跨年星座
        if start_month > end_month:
            if (month == start_month and day >= start_day) or (month == end_month + 12 and day <= end_day):
                return constellation
    return f"星座{month}-{day}"


def get_zodiac(year: int, month: int, day: int) -> str:
    # 2024年是龙年，以此为基准
    base_year = 2024
    zodiacs = ['龙🐉', '蛇🐍', '马🐎', '羊🐏', '猴🐒', '鸡🐔', '狗🐕', '猪🐖', '鼠🐀', '牛🐂', '虎🐅', '兔🐇']
    # 如果输入的日期在2月4日之前，生肖年份应该是上一年
    if (month == 1) or (month == 2 and day < 4):
        zodiac_year = year - 1
    else:
        zodiac_year = year

    zodiac_index = (zodiac_year - base_year) % 12
    return zodiacs[zodiac_index]


def get_career(num: int) -> str:
    career = {
        1: '计算机/互联网/通信',
        2: '生产/工艺/制造',
        3: '医疗/护理/制药',
        4: '金融/银行/投资/保险',
        5: '商业/服务业/个体经营',
        6: '文化/广告/传媒',
        7: '娱乐/艺术/表演',
        8: '律师/法务',
        9: '教育/培训',
        10: '公务员/行政/事业单位',
        11: '模特',
        12: '空姐',
        13: '学生',
        14: '其他职业'
    }
    return career.get(num, f"职业{num}")


def get_blood_type(num: int) -> str:
    blood_types = {
        1: 'A型',
        2: 'B型',
        3: 'O型',
        4: 'AB型',
        5: '其他血型'
    }
    return blood_types.get(num, f"血型{num}")


def parse_home_town(home_town_code: str) -> str:
    # 中国省份（包括直辖市）代码映射表，还没完善 TODO
    province_map = {
        '0': '某省',
        '98': '北京', '99': '天津', '100': '上海', '101': '重庆', '05': '河北',
        '06': '山西', '07': '内蒙古', '08': '辽宁', '09': '吉林', '10': '黑龙江',
        '04': '江苏', '12': '浙江', '103': '安徽', '104': '福建', '15': '江西',
        '106': '山东', '107': '河南', '108': '湖北', '109': '湖南', '20': '广东',
        '105': '广西', '22': '海南', '102': '四川', '24': '贵州', '25': '云南',
        '26': '西藏', '27': '陕西', '28': '甘肃', '29': '青海', '30': '宁夏', '31': '新疆'
    }
    # 处理国家代码
    country_map = {
        '49': '中国', '250': '俄罗斯', '222': '特里尔',
        '217': '法国', '233': '美国'
    }
    country_code, province_code, _ = home_town_code.split('-')
    country = country_map.get(country_code, f"外国{country_code}")
    if country_code == "49":
        province = province_map.get(province_code, f"{province_code}省")
        return f"{country}-{province_code}省"
    else:
        return country


def get_status(status_code: int) -> str:
    # 在线状态代码映射表，还没完善 TODO
    status_map = {
        1: "在线", 2: "Q我吧", 3: "离开", 4: "忙碌", 5: "请勿打扰",
        6: "隐身", 7: "我的电量", 8: "听歌中", 9: "有亿点冷", 10: "出去浪",
        11: "去旅行", 12: "被掏空", 13: "今日步数", 14: "今日天气", 15: "我crush了",
        16: "爱你", 17: "恋爱中", 18: "嗨到飞起", 19: "水逆退散", 20: "好运锦鲤",
        21: "元气满满", 22: "一言难尽", 23: "难得糊涂", 24: "emo中", 25: "我太难了",
        26: "我想开了", 27: "我没事", 28: "想静静", 29: "悠哉哉", 30: "信号弱",
        31: "睡觉中", 32: "肝作业", 33: "学习中", 34: "搬砖中", 35: "摸鱼中",
        36: "无聊中", 37: "TiMi中", 38: "一起元梦", 39: "求星搭子", 40: "熬夜中", 41: "追剧中"
    }
    return status_map.get(status_code, f"状态{status_code}")


def transform(info: dict, info2: dict) -> list:
    replay = []

    replay.append(f"Q号：{info['uin']}")
    replay.append(f"昵称：{info['nickname']}")

    if info2.get('card', False):
        replay.append(f"群昵称：{(info2['card'])}")
    if info2.get('title', False):
        replay.append(f"头衔：{(info2['title'])}")

    if info.get('status', False) and int(info['status']) != 20:
        replay.append(f"状态：{get_status(int(info['status']))}")

    if info['sex'] == "male":
        replay.append(f"性别：男孩纸")
    elif info['sex'] == "female":
        replay.append(f"性别：女孩纸")

    if info.get('birthday_year', False) and info.get('birthday_month', False) and info.get('birthday_day', False):
        replay.append(f"诞辰：{info['birthday_year']}-{info['birthday_month']}-{info['birthday_day']}")
        replay.append(f"星座：{get_constellation(int(info['birthday_month']), int(info['birthday_day']))}")
        replay.append(
            f"生肖：{get_zodiac(int(info['birthday_year']), int(info['birthday_month']), int(info['birthday_day']))}")
    if info.get('age', False) and 3 < int(info['age']) < 60:
        replay.append(f"年龄：{info['age']}岁")

    if info.get('phoneNum', '-') != "-":
        replay.append(f"电话：{info['phoneNum']}")
    if info.get('eMail', False):
        replay.append(f"邮箱：{info['eMail']}")
    if info.get('postCode', False):
        replay.append(f"邮编：{info['postCode']}")

    if info.get('country', False):
        replay.append(f"现居：{info['country']}")
    if info.get('city', False):
        replay[-1] += f"-{info['city']}"
    if info.get('homeTown', "0-0-0") != "0-0-0":
        replay.append(f"来自：{parse_home_town(info['homeTown'])}")
    if info.get('address', False):
        replay.append(f"地址：{info['address']}")

    if info.get('kBloodType', False):
        replay.append(f"血型：{get_blood_type(int(info['kBloodType']))}")
    if int(info.get('makeFriendCareer', 0)) != 0:
        replay.append(f"职业：{get_career(int(info['makeFriendCareer']))}")

    if info.get('remark', False):
        replay.append(f"备注：{info['remark']}")
    if info.get('labels', False):
        replay.append(f"标签：{info['labels']}")

    if info2.get('unfriendly', False):
        replay.append(f"不良记录：有")

    if info2.get('is_robot', False):
        replay.append(f"是否为bot: 是")

    if info.get('is_vip', False):
        replay.append(f"VIP：已开")
    if info.get('is_years_vip', False):
        replay.append(f"年费VIP：已开")
    if int(info.get('vip_level', 0)) != 0:
        replay.append(f"VIP等级：{info['vip_level']}")

    if int(info.get('login_days', 0)) != 0:
        replay.append(f"连续登录天数：{info['login_days']}")

    if info2.get('level', False):
        replay.append(f"群等级：{int(info2['level'])}级")
    if info2.get('join_time', False):
        replay.append(f"加群时间：{datetime.fromtimestamp(info2['join_time']).strftime('%Y-%m-%d')}")

    if info.get('qqLevel', False):
        replay.append(f"QQ等级：{int(info['qqLevel'])}级")
    if info.get('reg_time', False):
        replay.append(f"注册时间：{datetime.fromtimestamp(info['reg_time']).strftime('%Y年')}")

    if info.get('long_nick', False):
        long_nick_lines = [info['long_nick'][i:i + 15] for i in range(0, len(info['long_nick']), 15)]
        replay.append(f"签名：{long_nick_lines[0]}")
        for line in long_nick_lines[1:]:
            replay.append(line)

    return replay
