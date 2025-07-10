from astrbot.api import AstrBotConfig
from astrbot.api.event import AstrMessageEvent

class SourceMessageFilter:
    def __init__(self, config: AstrBotConfig):
        self.config = config
    
    def filt(self, event: AstrMessageEvent) -> bool:
        """检查消息事件是否满足黑白名单配置"""
        group_id = event.message_obj.group_id
        user_id = event.message_obj.sender.user_id
        if self.config["gather_mode"] == "黑名单":
            if user_id in self.config["source_blacklist"] or group_id in self.config["source_blacklist"]:
                return False
        else:
            if user_id not in self.config["source_whitelist"] and group_id not in self.config["source_whitelist"]:
                return False
        return True