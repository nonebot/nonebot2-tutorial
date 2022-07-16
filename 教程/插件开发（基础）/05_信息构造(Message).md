# 信息构造

在不同平台中，一条消息可能会有承载有各种不同的表现形式，它可能是一段纯文本、一张图片、一段语音、一篇富文本文章，也有可能是多种类型的组合等等。

在 NoneBot2 中，为确保消息的正常处理与跨平台兼容性，采用了扁平化的消息序列形式，即 `Message` 对象。

## Message

在 NoneBot2 中，`Message` 的主要作用是用于表达“一串消息”。由于 `Message` 继承自 `List[MessageSegment]`，所以 `Message` 的本质是由若干 `MessageSegment` 所组成的消息序列。因此，`Message` 的使用方法与 `List` 有很多相似之处，例如切片、索引、拼接等。

```python title=weather.py
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.plugin import on_command

# 通过此处的函数来获取天气信息
async def get_weather(city: str):
    weather = 'balabala...' # 此处填写获取到的天气信息
    return weather


matcher = on_command('天气') # 注册事件响应器

@matcher.handle() # 为事件响应器添加一个处理函数
async def handle_func(args: Message = CommandArg()):
    city = args.extract_plain_text() # 获取用户发送的命令信息
    if city in ['广州','上海']:
        weather_info = Message(f'今天 {city} 的天气是:') + MessageSegment.text(await get_weather(city=city)) # 拼接回复消息
        await matcher.finish(weather_info)
    else:
        await matcher.finish(f'您输入的城市 {city} 暂不支持查询，请重试...')
```

如上方示例所示，`Message` 可以将 `str` 类型的信息转化为 `Message` 类型的信息，并进行拼接操作。实际上 `Message` 支持的功能远不止这些，此部分将在将会在 ***（进阶部分的对应内容）*** 中进行介绍。

<!-- TODO: 补充进阶内容的链接 -->

## MessageSegment

不难发现，`Message` 的功能更多的在于消息序列层面，而对于一些非文本类消息的构建实际上起不到太大作用。而 `MessageSegment`(消息段)则是针对于 `Message` 中这一问题的解决方案。

顾名思义，`MessageSegment` 是一段消息。由于 `Message` 的本质是由若干 `MessageSegment` 所组成的消息序列。简单来说就是 `Message` 类似于一个自然段，而 `MessageSegment` 则是组成自然段的一句话。也就是说 `MessageSegment` 可以被认为是 `Message` 的最小单位。同时，作为特殊消息载体的存在，`MessageSegment` 中绝大多数内容均需要由对应的[协议适配器](..)所提供，以适应不同平台中的消息模式。**这也意味着，你需要导入对应的协议适配器中的 `MessageSegment` 后才能使用其特殊的工厂方法。**

<!-- TODO: 这里需要补充协议适配器部分的地址 -->

>Warning
在使用 `MessageSegment` 前，请务必先导入对应的协议适配器中的 `MessageSegment`，并查询其文档获得其支持的工厂方法及使用方法。

`MessageSegment` 的用法也十分简单，即为 `MessageSegment.func(arg)` ，例如：

```python
MessageSegment.text('hello world')
MessageSegment.image('image.jpg')
```

对于 `MessageSegment` 的具体用法，请参考对应的协议适配器的文档。
