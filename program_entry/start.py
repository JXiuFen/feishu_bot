import json
import lark_oapi as lark
from lark_oapi.api.im.v1 import P2ImMessageReceiveV1
from program_entry import FeiShu, SqliteDB, Chat
from program_entry.config import *

db = SqliteDB(FILE_PATH)
fs = FeiShu(APP_ID, APP_SECRET)


def find_event_id(event_id):
    query_obj = db.get_first(table_name='tb_event', where=f"event_id='{event_id}'")
    if query_obj:
        return True
    db.insert(table_name='tb_event', event_id=event_id)
    return False


def do_p2_im_message_receive_v1(data: P2ImMessageReceiveV1) -> None:
    message_content = json.loads(lark.JSON.marshal(data))
    event_id = message_content['header']['event_id']
    if not find_event_id(event_id):
        event_message = message_content['event']['message']
        event_sender_sender_id = message_content['event']['sender']['sender_id']

        chat_type = event_message.get('chat_type')              # group,p2p
        message_type = event_message.get('message_type')        # text
        content = json.loads(event_message.get('content'))['text']
        message_id = event_message.get('message_id')
        chat_id = event_message.get('chat_id')
        mentions = event_message.get('mentions')
        open_id = event_sender_sender_id.get('open_id')
        sender_id = event_sender_sender_id.get('user_id')

        if message_type != 'text':
            fs.reply_message(message_id, open_id, '目前仅支持文字聊天，暂不支持其他类型的提问')
        elif chat_type == 'group' and (not mentions or mentions[0].get('name') != BOT_NAME):    # 判断是群聊还是私聊
            # fs.reply_message(message_id, open_id, '请@机器人，进行聊天')
            pass
        else:
            try:
                Chat_obj = Chat('gpt-3.5',
                                AZURE_API_KEY,
                                AZURE_API_VERSION,
                                AZURE_ENDPOINT,
                                AZURE_DEPLOYMENT,
                                MODEL,
                                SESSION_ID=f'{chat_id}{sender_id}')
                result = Chat_obj.talk(content)
            except Exception as e:
                lark.logger.info(e)
                result = '问题太多了，我有点眩晕，请稍后再试！'
            fs.reply_message(message_id, open_id, result, chat_type)


def do_customized_event(data: lark.CustomizedEvent) -> None:
    pass
    # print("do_customized_event")
    # print(lark.JSON.marshal(data))


def program_entry():
    handler = lark.EventDispatcherHandler.builder(
        lark.ENCRYPT_KEY,
        lark.VERIFICATION_TOKEN,
        lark.LogLevel.INFO
    ).register_p2_im_message_receive_v1(do_p2_im_message_receive_v1).register_p1_customized_event(
        "message",
        do_customized_event
    ).build()
    cli = lark.ws.Client(
        APP_ID,
        APP_SECRET,
        event_handler=handler,
        log_level=lark.LogLevel.INFO)
    cli.start()


if __name__ == "__main__":
    program_entry()
