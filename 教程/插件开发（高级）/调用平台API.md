# 调用平台API

在 NoneBot2 及对应的协议适配器中，可能存在部分未被收录的API或无法调用依赖注入（如[定时任务](定时任务.md)）的情况。此时可以通过调用平台API的方式来进行信息的获取和发送等操作。

## 获取Bot实例

调用平台API的方法是 Bot 对象的一种方法，因此我们首先需要获得 Bot 实例。

```python
from nonebot import get_bot

bot = get_bot()  # 获取bot列表中的第一个 bot
bot = get_bot("bot_id")  # 获取id为 bot_id 的bot
```

## 调用API

NoneBot 提供了两种方式来调用机器人平台 API。

```python
from nonebot import get_bot

bot = get_bot("bot_id")
# 通过 bot.api_name() 的方法调用API
result = await bot.get_user_info(user_id=12345678)
# 通过 bot.call_api(api_name) 的方法调用API
result = await bot.call_api("get_user_info", user_id=12345678)
```

## 可被调用的API

可参考对应的协议适配器文档或平台开发文档。
