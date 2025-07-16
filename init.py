# 初始化操作
from .core.utils import db, file, runtime
import os
from astrbot.api import logger
def init_db(db_path):
    # 执行初始化脚本
    if not os.path.exists(db_path):
        logger.info("初始化数据库")
        db.get_conn(db_path)
        db.executescript(file.read_file(
            runtime.get_resource_path("./resources/sql/init.sql")
        ))
        logger.info("初始化数据库成功")
    else:
        db.get_conn(db_path)
    db.add_column_if_not_exists("message_history", "weight", "integer", 0)