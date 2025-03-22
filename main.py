
from astrbot.api.all import *
from .draw import create_image
from .utils import get_avatar, transform
import astrbot.api.message_components as Comp
from astrbot import logger
from astrbot.api.event import filter




@register("盒", "Zhalslar", "开盒插件", "1.0.0", "https://github.com/Zhalslar/astrbot_plugin_box")
class Box(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("盒", alias={"开盒"})
    async def box(self, event: AstrMessageEvent):
        messages = event.get_messages()
        send_id = event.get_sender_id()
        self_id = event.get_self_id()
        target_user_id = next((str(seg.qq) for seg in messages if (isinstance(seg, Comp.At)) and str(seg.qq) != self_id), send_id)
        group_id = event.get_group_id()
        try:
            if event.get_platform_name() == "aiocqhttp":
                from astrbot.core.platform.sources.aiocqhttp.aiocqhttp_message_event import AiocqhttpMessageEvent
                assert isinstance(event, AiocqhttpMessageEvent)
                client = event.bot
                stranger_payloads = {"user_id": target_user_id}
                member_payloads = {"user_id": target_user_id, "group_id": group_id,}
                stranger_info: dict = await client.api.call_action('get_stranger_info', **stranger_payloads)
                member_info: dict = await client.api.call_action('get_group_member_info', **member_payloads)
                avatar: bytes = await get_avatar(target_user_id)
                reply: list = transform(stranger_info, member_info)
                img_path: str = create_image(avatar, reply)
                yield event.make_result().file_image(img_path)
        except Exception as e:
            logger.error(f"开盒出错: {e}")







