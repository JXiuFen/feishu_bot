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
        lark.logger.info(message_content)
        event_message = message_content['event']['message']
        event_sender_sender_id = message_content['event']['sender']['sender_id']

        chat_type = event_message.get('chat_type')              # group,p2p
        message_type = event_message.get('message_type')        # text, image:image_key, file:file_key
        message_id = event_message.get('message_id')
        chat_id = event_message.get('chat_id')
        mentions = event_message.get('mentions')
        open_id = event_sender_sender_id.get('open_id')
        sender_id = event_sender_sender_id.get('user_id')

        # if message_type not in ['text', 'image', 'file']:
        #     fs.reply_message(message_id, open_id, '目前仅支持文字,图片和PDF文件，暂不支持其他类型的提问')
        if message_type != 'text':
            fs.reply_message(message_id, open_id, '目前仅支持文字聊天，暂不支持其他类型的提问')
        elif chat_type == 'group' and (not mentions or mentions[0].get('name') != BOT_NAME):    # 判断是群聊还是私聊
            pass
        else:
            Chat_obj = Chat('gpt-3.5',
                            AZURE_API_KEY,
                            AZURE_API_VERSION,
                            AZURE_ENDPOINT,
                            AZURE_DEPLOYMENT,
                            MODEL,
                            SESSION_ID=f'{chat_id}{sender_id}')

            if message_type == 'text':
                content = json.loads(event_message.get('content'))['text']
                result = Chat_obj.talk(content)
                fs.reply_message(message_id, open_id, result, chat_type=chat_type)
            # todo 发送文件和图片逻辑
            # elif message_type == 'image':
            #     content = json.loads(event_message.get('content'))['image_key']
            #     # fs.download_image(message_id, content, "image")
            #     with open('./file/abc.png', 'rb') as f:
            #         image_key = fs.upload_image(f)
            #     fs.reply_message(message_id, open_id, image_key, msg_type='image', chat_type=chat_type)
            # elif message_type == 'file':
            #     content = json.loads(event_message.get('content'))['file_key']
            #     if not fs.download_image(message_id, content, "file"):
            #         fs.reply_message(message_id, open_id, '文件类型格式错误，目前只支持PDF')
            #     else:
            #         fs.reply_message(message_id, open_id, 'hello world!')


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
