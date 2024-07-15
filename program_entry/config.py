import os
from dotenv import load_dotenv


# 从当前目录加载.env文件
load_dotenv()

FILE_PATH = os.getenv('FILE_PATH')

APP_ID = os.getenv('APP_ID')
APP_SECRET = os.getenv('APP_SECRET')
BOT_NAME = os.getenv('BOT_NAME')

AZURE_API_KEY = os.getenv('AZURE_API_KEY')
AZURE_ENDPOINT = os.getenv('AZURE_ENDPOINT')
AZURE_DEPLOYMENT = os.getenv('AZURE_DEPLOYMENT')
AZURE_API_VERSION = os.getenv('AZURE_API_VERSION', '2024-02-15-preview')
MODEL = os.getenv('MODEL', 'gpt-3.5-turbo-16k')

status = 0

print('=========加载配置================')
if not APP_ID:
    status += 1
    print(f"{status}、你没有配置飞书应用的 AppID，请检查 & 部署后重试!!!")


if not APP_SECRET:
    status += 1
    print(f"{status}、你没有配置飞书应用的 Secret，请检查 & 部署后重试!!!")


if not BOT_NAME:
    status += 1
    print(f"{status}、你没有配置飞书应用的名称，请检查 & 部署后重试!!!")

if not AZURE_API_KEY:
    status += 1
    print(f"{status}、你没有配置azure的 KEY，请检查 & 部署后重试!!!")


if not AZURE_ENDPOINT:
    status += 1
    print(f"{status}、你没有配置azure的 ENDPOINT，请检查 & 部署后重试!!!")


if not AZURE_DEPLOYMENT:
    status += 1
    print(f"{status}、你没有配置azure的 AZURE_DEPLOYMENT，请检查 & 部署后重试!!!")


# if not AZURE_API_VERSION:
#     status += 1
#     print(f"{status}、你没有配置azure的 AZURE_API_VERSION，请检查 & 部署后重试!")
#
#
# if not MODEL:
#     status += 1
#     print(f"{status}、你没有配置azure的 AZURE_API_VERSION，请检查 & 部署后重试!")

