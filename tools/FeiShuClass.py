import json
import uuid
import lark_oapi as lark
from lark_oapi.api.im.v1 import ReplyMessageRequest, ReplyMessageRequestBody, ReplyMessageResponse


class FeiShu:
    def __init__(self, APP_ID, APP_SECRET):
        self.APP_ID = APP_ID
        self.APP_SECRET = APP_SECRET
        self._constructor()

    def _constructor(self):
        self.client = lark.Client.builder().app_id(self.APP_ID).app_secret(self.APP_SECRET).log_level(lark.LogLevel.DEBUG).build()

    def assembly_message(self, open_id, message, chat_type='p2p'):
        message_content = {
            "text": f'<at user_id="{open_id}"></at>{message}' if chat_type == 'group' else f'{message}'
        }
        return json.dumps(message_content)

    def reply_message(self, message_id, open_id, message, chat_type='p2p'):
        # 构造请求对象
        request: ReplyMessageRequest = ReplyMessageRequest.builder().message_id(message_id).request_body(
            ReplyMessageRequestBody
            .builder()
            .content(self.assembly_message(open_id, message,  chat_type))
            .msg_type("text")
            .uuid(str(uuid.uuid4()))
            .build()
        ).build()

        # 发起请求
        response: ReplyMessageResponse = self.client.im.v1.message.reply(request)

        # 处理失败返回
        if not response.success():
            lark.logger.error(
                f"reply_message failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
            return False

        # 处理业务结果
        lark.logger.info(lark.JSON.marshal(response.data, indent=4))
        return True
