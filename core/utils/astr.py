from astrbot.api.platform import AstrBotMessage
def is_forward(message_obj: AstrBotMessage) -> bool:
    raw_message = message_obj.raw_message
    message_list = raw_message.get("message") if isinstance(raw_message, dict) else None
    return (message_list is not None and 
                 isinstance(message_list, list) and 
                 message_list and
                 isinstance(message_list[0], dict) and
                 message_list[0].get("type") == "forward")