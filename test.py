import random
from tools.DBClass import SqliteDB
from program_entry.config import *


def demo(a, **kwargs):
    print(a)
    print(kwargs)
    convert_to_string = lambda d: 'and '.join([f"{k}='{v}'" for k, v in d.items()])
    result = convert_to_string(kwargs)
    print(result)


def init_databases():
    db = SqliteDB(FILE_PATH)
    res = db.insert(table_name='tb_event', event_id='a4bd1a414488cf3e9b1f82e6178c3213')
    query_obj = db.get_all(table_name='tb_event', field=['event_id', 'create_time'])
    for item in query_obj:
        print(item)
    # sql = """CREATE TABLE IF NOT EXISTS tb_msg(
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     session_id VARCHAR (100) NOT NULL,
    #     question TEXT,
    #     answer TEXT,
    #     token INTEGER,
    #     create_time TIMESTAMP DEFAULT (datetime('now','localtime'))
    #   )
    # """
    # db.create_table(sql=sql, table_name='tb_msg')
    # print(db.insert(table_name="tb_msg", session_id="123456", question="黑佬，土狗", answer='你才是土狗，你全家都是土狗', token=666))

    # db.delete(table_name="tb_msg", where="token=666")
    # cs = db.get_all(table_name="tb_msg", field=['session_id', 'question', 'answer', 'token'])
    # print(cs)

    # sql = """
    # CREATE TABLE if not exists tb_event(
    #     id INTEGER PRIMARY KEY,
    #     event_id VARCHAR (40) NOT NULL,
    #     content TEXT
    #   )
    # """
    # db.create_table(sql=sql, table_name='tb_event')


class abc:
    def __init__(self):
        self.sbc_list = []

    def erdr(self):
        self.sbc_list.append(random.randint(1,100))


if __name__ == '__main__':
    init_databases()
