from typing import Optional

from tools.DBClass import SqliteDB
from tools.AzureClass import ChatRobot
from program_entry.config import *


db = SqliteDB(FILE_PATH)


class Chat(ChatRobot):
    def __init__(self,
                 MODEL_TYPE,
                 AZURE_API_KEY,
                 AZURE_API_VERSION,
                 AZURE_ENDPOINT,
                 AZURE_DEPLOYMENT,
                 MODEL,
                 SESSION_ID,
                 MAX_TOKENS=4096,
                 TEMPERATURE=0.5,
                 ) -> None:
        super().__init__()
        self.AZURE_API_KEY = AZURE_API_KEY
        self.AZURE_API_VERSION = AZURE_API_VERSION
        self.AZURE_ENDPOINT = AZURE_ENDPOINT
        self.AZURE_DEPLOYMENT = AZURE_DEPLOYMENT
        self.MODEL = MODEL
        self.MAX_TOKENS = MAX_TOKENS
        self.TEMPERATURE = TEMPERATURE
        self.MODEL_TYPE = MODEL_TYPE
        self.SESSION_ID = SESSION_ID
        self.history_list = []
        self.init_openai()
        self._history_msgs()

    def _history_msgs(self) -> None:
        """
        构造用户会话
        :return:
        """
        query_obj = db.get_all(
            table_name="tb_msg",
            field=['question', 'answer'],
            where=f"session_id='{self.SESSION_ID}'",
            order="id desc limit 10"
        )
        if query_obj:
            for item in query_obj[::-1]:
                self.history_list.append({"role": "user", "content": item['question']})
                self.history_list.append({"role": "assistant", "content": item['answer']})

    def _save_msgs(self, data: Optional[dict]) -> None:
        """
        保存会话
        :return:
        """
        if data['answer'] and data['token']:
            db.insert(
                table_name="tb_msg",
                session_id=self.SESSION_ID,
                question=data['question'],
                answer=data['answer'],
                token=data['token']
            )

    def _delete_msgs(self) -> None:
        """
        清空会话
        :return:
        """
        # self.history_list = []

    def talk(self, content: Optional[str]) -> str:
        """
        交谈
        :param content:
        :return:
        """
        try:
            self.history_list.append({"role": "user", "content": content})
            result, token = self.completions_no_stream(messages=self.history_list)
        except Exception as e:
            print(f"open ai talk error:{e}")
            return ''
        self._save_msgs({"question": content, "answer": result, "token": token})
        return result


if __name__ == '__main__':
    # chat_bak()
    messages = "那你不会觉得生活，单调了些麻？"
    Chat_obj = Chat('gpt-3.5', AZURE_API_KEY, AZURE_API_VERSION, AZURE_ENDPOINT, AZURE_DEPLOYMENT, MODEL, SESSION_ID='123')
    result = Chat_obj.talk(messages)
    print(result)
