# 飞书对接ChatGPT(Azure)
- - -
> 飞书机器人对接GPT，群聊和私聊都可以使用
### 效果演示
- - -
![图片](https://github.com/JXiuFen/feishu_bot/blob/main/picgo/20240715142302.png)
![图片](https://github.com/JXiuFen/feishu_bot/blob/main/picgo/20240715142321.png)

### 飞书机器人的创建
- - -
* 1、访问开发者后台，创建一个机器人的应用，获取APPID和Secret 
![图片](https://github.com/JXiuFen/feishu_bot/blob/main/picgo/20240715143151.png)
* 2、开启机器人能力
![图片](https://github.com/JXiuFen/feishu_bot/blob/main/picgo/20240715143321.png)
* 3、开启权限
![图片](https://github.com/JXiuFen/feishu_bot/blob/main/picgo/20240715143419.png)
* 4、配置事件
![图片](https://github.com/JXiuFen/feishu_bot/blob/main/picgo/20240715143655.png)
* 5、发布版本，等待审核
![图片](https://github.com/JXiuFen/feishu_bot/blob/main/picgo/20240715144907.png)


### 项目部署
- - -
> 环境 python3.8以上，centos7.9
> * 安装依赖库
> * pip install -r requirements.txt
> * 运行程序
> * python main.py
> * 修改配置文件
> * vim .env <br>
> 配置文件说明 <br>
> FILE_PATH   *#sqlite文件路径*<br>
> APP_ID   *#飞书机器人ID*<br>
> APP_SECRET   *#飞书机器人SECRET*<br>
> BOT_NAME   *#飞书机器人名称*<br>
> BOT_NAME   *#飞书机器人名称*<br>

![图片](https://github.com/JXiuFen/feishu_bot/blob/main/picgo/20240715150225.png)

### FAQ
- - -
#### 1、飞书机器人支持语音和图片？
目前仅支持文本消息，后续会添加语音和图片功能

#### 2、飞书机器人支持群聊？
支持群聊和私聊，群聊需要@机器人，才会被机器人回复

#### 3、可以使用GPT4？
可以正常使用，只要Azure是gpt4版本的，就可以使用gpt4
