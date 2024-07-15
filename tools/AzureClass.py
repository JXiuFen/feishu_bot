#   azure模型
from typing import Optional
from openai import AzureOpenAI


class ChatRobot(object):
    def __init__(self) -> None:
        self.AZURE_API_KEY: Optional[str] = None
        self.AZURE_API_VERSION: Optional[str] = None
        self.AZURE_ENDPOINT: Optional[str] = None
        self.AZURE_DEPLOYMENT: Optional[str] = None
        self.MODEL: Optional[str] = 'gpt-3.5-turbo-16k'
        self.MAX_TOKENS: Optional[int] = 4096
        self.TEMPERATURE: Optional[float] = 0.5
        self.client_obj = Optional[object]

    def init_openai(self) -> None:
        self.client_obj = AzureOpenAI(
            api_key=self.AZURE_API_KEY,
            api_version=self.AZURE_API_VERSION,
            azure_endpoint=self.AZURE_ENDPOINT,
            azure_deployment=self.AZURE_DEPLOYMENT
        )

    def completions_stream(self, messages: Optional[list]) -> str:
        """
        流式
        :param messages:
        :return:
        """
        try:
            chat_completion = self.client_obj.chat.completions.create(
                model=self.MODEL,
                messages=messages,
                temperature=self.TEMPERATURE,
                max_tokens=self.MAX_TOKENS,
                stream=True,
            )

            result_string = ""
            for i in chat_completion:
                if i.choices:
                    result_string += i.choices[0].delta.content or ""
                yield result_string
            yield result_string
        except Exception as e:
            print('AzureChatRobot completions_stream', e)
            return ''

    def completions_no_stream(self, messages: Optional[list]) -> tuple:
        """
        非流式
        :param messages:
        :return:
        """
        try:
            chat_completion = self.client_obj.chat.completions.create(
                model=self.MODEL,
                messages=messages,
                temperature=self.TEMPERATURE,
                max_tokens=self.MAX_TOKENS
            )

            if chat_completion:
                if chat_completion.choices[0].message.content:
                    return chat_completion.choices[0].message.content.replace("\n\n", ""), chat_completion.usage.total_tokens
        except Exception as e:
            print('AzureChatRobot completions_no_stream', e)
            return '', 0
