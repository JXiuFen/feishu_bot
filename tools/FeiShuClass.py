import time
import json
import uuid
import lark_oapi as lark
from lark_oapi.api.im.v1 import ReplyMessageRequest, ReplyMessageRequestBody, ReplyMessageResponse, \
    GetMessageResourceRequest, GetMessageResourceResponse, CreateImageRequest, CreateImageRequestBody, CreateImageResponse


class FeiShu:
    def __init__(self, APP_ID, APP_SECRET):
        self.APP_ID = APP_ID
        self.APP_SECRET = APP_SECRET
        self._constructor()

    def _constructor(self):
        self.client = lark.Client.builder().app_id(self.APP_ID).app_secret(self.APP_SECRET).log_level(lark.LogLevel.INFO).build()

    def assembly_message(self, open_id, message, msg_type='text', chat_type='p2p'):
        if msg_type == 'image':
            message_content = {
                f"{msg_type}_key": f'<at user_id="{open_id}"></at>{message}' if chat_type == 'group' else f'{message}'
            }
        else:
            message_content = {
                f"{msg_type}": f'<at user_id="{open_id}"></at>{message}' if chat_type == 'group' else f'{message}'
            }
        return json.dumps(message_content)

    def reply_message(self, message_id, open_id, message, msg_type='text', chat_type='p2p'):
        # 构造请求对象
        request: ReplyMessageRequest = ReplyMessageRequest.builder().message_id(message_id).request_body(
            ReplyMessageRequestBody
            .builder()
            .content(self.assembly_message(open_id, message, msg_type,  chat_type))
            .msg_type(msg_type)
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

    def reply_image_message(self):
        pass

    def download_image(self, message_id, file_key, file_type):
        # 构造请求对象
        request: GetMessageResourceRequest = GetMessageResourceRequest.builder().message_id(message_id).file_key(file_key).type(file_type).build()

        # 发起请求
        response: GetMessageResourceResponse = self.client.im.v1.message_resource.get(request)

        # 处理失败返回
        if not response.success():
            lark.logger.error(
                f"client.im.v1.message_resource.get failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
            return False
        if file_type == 'image':
            with open(f"/tmp/pycharm_project_149/file/{int(time.time())}.jpg", "wb") as f:
                f.write(response.file.read())
            return True
        elif file_type == 'file':
            file_suffix = response.file_name.split('.')[-1]
            if file_suffix == 'pdf':
                with open(f"/tmp/pycharm_project_149/file/{response.file_name}", "wb") as f:
                    f.write(response.file.read())
                return True
            return False

    def upload_image(self, image_content, image_type='message'):
        # 构造请求对象
        request: CreateImageRequest = CreateImageRequest.builder().request_body(
            CreateImageRequestBody.builder().image_type(image_type).image(image_content).build()
        ).build()

        # 发起请求
        response: CreateImageResponse = self.client.im.v1.image.create(request)

        # 处理失败返回
        if not response.success():
            lark.logger.error(
                f"client.im.v1.image.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
            return False

        # 处理业务结果
        lark.logger.info(lark.JSON.marshal(response.data, indent=4))
        return response.data.image_key


