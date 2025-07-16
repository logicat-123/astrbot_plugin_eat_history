from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register, StarTools
from astrbot.api import logger, AstrBotConfig
from . import init
from .core.utils import db, astr
from .core.filter.source_message_filter import SourceMessageFilter
from datetime import datetime
import pathlib

@register("astrbot_plugin_eat_history", "logicat", "赤石插件", "1.0.1")
class EatHistory(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        init.init_db(pathlib.Path(StarTools.get_data_dir()).joinpath("eat_history.db"))
        self.config = config
        self.source_message_filter = SourceMessageFilter(self.config)
        logger.info("赤石插件加载成功")

    @filter.command("我要赤石", alias={"我要吃屎", "我要吃史", "我要吃石", "我要赤使", "我要赤史"})
    async def eat_history(self, event: AstrMessageEvent):
        """赤石指令"""
        user_id = event.message_obj.sender.user_id
        group_id = event.message_obj.group_id
                
        # 从数据库中随机获取一条历史记录并发送
        history = db.select_random_one("message_history", order_bys=["weight desc"])
        if not history:
            yield event.plain_result("没有历史记录喵")
        else:
            if group_id:
                playload = {
                    "group_id": group_id,
                    "message_id": history["message_id"]
                }
                await event.bot.api.call_action("forward_group_single_msg", **playload)
            else:
                playload = {
                    "user_id": user_id,
                    "message_id": history["message_id"]
                }
                await event.bot.api.call_action("forward_friend_single_msg", **playload)
        # 每次读完消息后，权重降低
        history = db.update_by_entity("message_history", {"message_id": history["message_id"]}, {"weight": history["weight"] - 1})
        event.stop_event()

    @filter.platform_adapter_type(filter.PlatformAdapterType.AIOCQHTTP | filter.PlatformAdapterType.QQOFFICIAL, priority=999)
    async def save_history(self, event: AstrMessageEvent):
        '''只接收 AIOCQHTTP 和 QQOFFICIAL 的消息'''
        # 检查黑白名单
        if not self.source_message_filter.filt(event):
            return
        # 收到转发消息时，保存到数据库中
        group_id = event.message_obj.group_id
        user_id = event.message_obj.sender.user_id
        user_nick = event.message_obj.sender.nickname
        message_id = event.message_obj.message_id
        if astr.is_forward(event.message_obj):
            db.insert_by_entity("message_history", {
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "user_id": user_id,
                "user_nick": user_nick,
                "message_id": message_id,
                "group_id": group_id,
            })

    @filter.command("查看史书")
    async def see_history_info(self, event: AstrMessageEvent):
        """查看历史信息"""
        # 从数据库中随机获取一条历史记录并发送
        total = db.count_by_entity("message_history") or 0
        yield event.plain_result(f"共计 {total} 条历史记录")