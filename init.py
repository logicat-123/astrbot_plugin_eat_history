# 初始化操作
from .utils import db, file, runtime
from . import config
import os
from astrbot.api import logger
def init_db():
    # 运行环境下的db路径
    db_path = runtime.get_resource_path("./data", config.DB_PATH)
    
    if not os.path.exists(db_path):
        logger.info("初始化数据库")
        os.makedirs(os.path.dirname(db_path))
        conn = db.get_conn(db_path)
        db.executescript(file.read_file(
            runtime.get_resource_path("./resources/sql/init.sql")
        ))
        logger.info("初始化数据库成功")

    # 连接到SQLite数据库
    conn = db.get_conn(db_path)

    # 设置回调函数以记录SQL语句
    def sql_trace_callback(log_message):
        logger.info(f"SQL执行: {log_message}")

    conn.set_trace_callback(sql_trace_callback)

def init():
    init_db()

init()