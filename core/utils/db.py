import sqlite3
import threading
from astrbot.api import logger

local_data = threading.local()

def set_enable_sql_log(enable_sql_log: bool):
    if not enable_sql_log: return
    def sql_trace_callback(log_message):
        logger.info(f"SQL执行: {log_message}")

    get_conn().set_trace_callback(sql_trace_callback)
def get_conn(db_path=None):
    """获取数据库连接，初始化连接"""
    if not hasattr(local_data, "conn") and db_path:
        local_data.conn = sqlite3.connect(db_path)
        # 设置row_factory为sqlite3.Row
        local_data.conn.row_factory = sqlite3.Row
    return local_data.conn

def execute(sql, params=()):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    conn.commit()
    return cursor

def executes(sqls):
    conn = get_conn()
    cursor = conn.cursor()
    for sql in sqls:
        cursor.execute(sql)
    conn.commit()
    return cursor

def executescript(script):
    conn = get_conn()
    conn.executescript(script)
    conn.commit()

def select_one(sql, params=()):
    return execute(sql, params).fetchone()

def select_all(sql, params=()):
    return execute(sql, params).fetchall()

def select_one_by_entity(table_name, data={}):
    sql = f"""
    select
    *
    from {table_name}
    """
    if data:
        sql += " where " + " and ".join([f"{key}=:{key}" for key in data])
    sql += " limit 1"
    return execute(sql, data).fetchone()

def select_list_by_entity(table_name, data={}):
    sql = f"""
    select
    *
    from {table_name}
    """
    if data:
        sql += " where " + " and ".join([f"{key}=?" for key in data])
    return execute(sql, tuple(data.values())).fetchall()

def insert_by_entity(table_name, data):
    
    if not data: return
    sql = f"""
    insert into {table_name} ({
            ','.join(data.keys())
        }) values ({
            ','.join([f":{col}" for col in data.keys()])
        })
    """
    return execute(sql, data)

def update_by_entity(table_name, search_data, update_data):
    sql = f"""
    update {table_name}
    """ + f"""
    set {','.join([f"{col}=:{col}" for col in update_data.keys()])}
    """ + (f"""
    where {','.join([f"{col}=:{col}" for col in search_data.keys()])}
    """ if search_data else "") 
    return execute(sql, {**search_data, **update_data})

def upsert_by_entity(table_name, search_entity, update_entity):
    """插入或更新数据"""
    db_entity = select_one_by_entity(table_name, search_entity)
    if db_entity:
        return update_by_entity(table_name, search_entity, update_entity)
    else:
        return insert_by_entity(table_name, update_entity)

def delete_by_entity(table_name, search_entity={}, delete_when_empty=True):
    if (not search_entity) and (not delete_when_empty):
        return
    sql = f"""
    delete from
    {table_name}
    """ + (f"""
    where {','.join([f"{col}=:{col}" for col in search_entity.keys()])}
    """ if search_entity else "")
    return execute(sql, search_entity)

def select_random_one(table_name):
    return select_one(f"""
                      select
                      *
                      from {table_name}
                      order by random()
                      limit 1
                      """)

def count_by_entity(table_name, entity={}):
    sql = f"""
    select
        count(0) as total
    from {table_name}
    """
    if entity:
        sql += " where " + " and ".join([f"{key}=:{key}" for key in entity])
    result = execute(sql, entity).fetchone()
    return result["total"] if result else 0
def worker():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT ...")
    # 处理数据...
