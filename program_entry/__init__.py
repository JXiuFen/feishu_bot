import sys

from tools.AzureClass import ChatRobot
from tools.FeiShuClass import FeiShu
from tools.DBClass import SqliteDB
from .azure_openai import Chat
from .config import *


if status != 0:
    print('=========加载配置失败============')
    sys.exit(0)


db = SqliteDB(FILE_PATH)
tb_msg_sql = """CREATE TABLE IF NOT EXISTS tb_msg(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id VARCHAR (100) NOT NULL,
        question TEXT,
        answer TEXT,
        token INTEGER,
        create_time TIMESTAMP DEFAULT (datetime('now','localtime'))
      )
    """
tb_event_sql = """
    CREATE TABLE if not exists tb_event(
        id INTEGER PRIMARY KEY,
        event_id VARCHAR (40) NOT NULL,
        create_time TIMESTAMP DEFAULT (datetime('now','localtime'))
      )
    """
if db.create_table(sql=tb_msg_sql, table_name='tb_msg'):
    print('****创建数据表【tb_msg】，成功****')
if db.create_table(sql=tb_event_sql, table_name='tb_event'):
    print('****创建数据表【tb_event】，成功****')

print('=========加载配置成功============')
