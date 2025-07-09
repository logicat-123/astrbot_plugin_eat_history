from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger, AstrBotConfig
from . import init
from .utils import db
from datetime import datetime

@register("astrbot_plugin_eat_history", "logicat", "赤石插件", "1.0.1")
class EatHistory(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        init.init()
        self.config = config

    @filter.command("我要赤石")
    async def eat_history(self, event: AstrMessageEvent):
        """赤石指令"""
        user_id = event.message_obj.sender.user_id
        group_id = event.message_obj.group_id
                
        # 从数据库中随机获取一条历史记录并发送
        history = db.select_random_one("message_history")
        
        playload = {
            "group_id": group_id,
            "message_id": history["message_id"]
        }
        await event.bot.api.call_action("forward_group_single_msg", **playload)
        event.stop_event()

    @filter.platform_adapter_type(filter.PlatformAdapterType.AIOCQHTTP | filter.PlatformAdapterType.QQOFFICIAL)
    async def on_aiocqhttp(self, event: AstrMessageEvent):
        '''只接收 AIOCQHTTP 和 QQOFFICIAL 的消息'''
        print("received")
        group_id = event.message_obj.group_id
        user_id = event.message_obj.sender.user_id
        user_nick = event.message_obj.sender.nickname
        message_id = event.message_obj.message_id
        if self.config["gather_mode"] == "黑名单":
            if user_id in self.config["source_blacklist"] or group_id in self.config["source_blacklist"]:
                return
        else:
            if user_id not in self.config["source_whitelist"] and group_id not in self.config["source_whitelist"]:
                return
        # 收到转发消息时，保存到数据库中
        raw_message = event.message_obj.raw_message
        message_list = raw_message.get("message") if isinstance(raw_message, dict) else None
        is_forward = (message_list is not None and 
                     isinstance(message_list, list) and 
                     message_list and
                     isinstance(message_list[0], dict) and
                     message_list[0].get("type") == "forward")
        if is_forward:
            db.insert_by_entity("message_history", {
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "user_id": user_id,
                "user_nick": user_nick,
                "message_id": message_id,
                "group_id": group_id,
            })