# 消息构造

在不同平台中，一条消息可能会有承载有各种不同的表现形式，它可能是一段纯文本、一张图片、一段语音、一篇富文本文章，也有可能是多种类型的组合等等。

在 NoneBot2 中，为确保消息的正常处理与跨平台兼容性，采用了扁平化的消息序列形式，即 `Message` 对象。

## 基础使用

### Message

在 NoneBot2 中，`Message` 的主要作用是用于表达“一串消息”。由于 `Message` 继承自 `List[MessageSegment]`，所以 `Message` 的本质是由若干 `MessageSegment` 所组成的消息序列。因此，`Message` 的使用方法与 `List` 有很多相似之处，例如切片、索引、拼接等。

```python title=weather.py
from nonebot.adapters import Message, MessageSegment
from nonebot.params import CommandArg
from nonebot.plugin import on_command

# 通过此处的函数来获取天气信息
async def get_weather(city: str):
    weather = f"do something to get weather of {city}"
    return weather


matcher = on_command("天气", priority=10)  # 注册事件响应器


@matcher.handle()  # 为事件响应器添加一个处理函数
async def handle_func(args: Message = CommandArg()):
    city = args.extract_plain_text()  # 获取用户发送的命令信息
    if city in ["广州", "上海"]:
        weather_info = Message(f"今天 {city} 的天气是:") + MessageSegment.text(
            await get_weather(city=city)
        )  # 拼接回复消息
        await matcher.finish(weather_info)
    else:
        await matcher.finish(f"您输入的城市 {city} 暂不支持查询，请重试...")
```

如上方示例所示，`Message` 可以将 `str` 类型的信息转化为 `Message` 类型的信息，并进行拼接操作。

`Message` 不仅可以拼接 `Message` 类型的消息，也可以对 `str` 和下文即将提到的 `MessageSegment` 进行拼接。

### MessageSegment

不难发现，`Message` 的功能更多的在于消息序列层面，例如将多段消息进行拼接、排序、切片和模板化构造等功能。这些功能更加倾向于对多段消息的管理，而对于单段复杂消息的构建实际上起不到太大作用。而 `MessageSegment`(消息段)则是针对于 `Message` 中这一问题的解决方案。

顾名思义，`MessageSegment` 是一段消息。由于 `Message` 的本质是由若干 `MessageSegment` 所组成的消息序列。简单来说就是 `Message` 类似于一个自然段，而 `MessageSegment` 则是组成自然段的一句话。也就是说 `MessageSegment` 可以被认为是构成 `Message` 的最小单位。同时，作为特殊消息载体的存在，`MessageSegment` 中绝大多数内容均需要由对应的[协议适配器](<!-- TODO: 这里需要补充协议适配器的文档链接 -->)所提供，以适应不同平台中的消息模式。**这也意味着，你需要导入对应的协议适配器中的 `MessageSegment` 后才能使用其特殊的工厂方法。**

<!-- TODO: 这里需要补充协议适配器部分的地址 -->

::: warning
在使用 `MessageSegment` 前，请务必先导入对应的协议适配器中的 `MessageSegment`，并查询其文档获得其支持的工厂方法及使用方法。
:::

`MessageSegment` 的用法也十分简单，即为 `MessageSegment.func(arg)` ，例如：

```python
MessageSegment.text('hello world')
MessageSegment.image('image.jpg')
```

对于 `MessageSegment` 的具体用法，请参考对应的协议适配器的文档。

## 进阶使用

::: tips
下列使用方法并不属于 `Message` 或 `MessageSegment` 的最基础的应用，如果您无法理解其内容，可以直接跳过下文。
:::

### 使用消息序列

通常情况下，适配器在接收到消息时，会将消息转换为消息序列，可以通过 [`EventMessage`](../../进阶/功能/内置依赖注入.md#eventmessage) 作为依赖注入, 或者使用 `event.get_message()` 获取。

由于它是`List[MessageSegment]`的子类, 所以你总是可以用和操作 List 类似的方式来处理消息序列

```python
>>> message = Message([
    MessageSegment(type='text', data={'text':'hello'}),
    MessageSegment(type='image', data={'url':'http://example.com/image.png'}),
    MessageSegment(type='text', data={'text':'world'}),
])
>>> for segment in message:
...     print(segment.type, segment.data)
...
text {'text': 'hello'}
image {'url': 'http://example.com/image.png'}
text {'text': 'world'}
>>> len(message)
3
```

### 构造消息序列

在使用事件响应器操作发送消息时，既可以使用 `str` 作为消息，也可以使用 `Message`、`MessageSegment` 或者 `MessageTemplate`。那么，我们就需要先构造一个消息序列。

#### 直接构造

`Message` 类可以直接实例化，支持 `str`、`MessageSegment`、`Iterable[MessageSegment]` 或适配器自定义类型的参数。

```python
# str
Message("Hello, world!")
# MessageSegment
Message(MessageSegment.text("Hello, world!"))
# List[MessageSegment]
Message([MessageSegment.text("Hello, world!")])
```

#### 运算构造

`Message` 对象可以通过 `str`、`MessageSegment` 相加构造，详情请参考[拼接消息](#拼接消息)。

#### 从字典数组构造

`Message` 对象支持 Pydantic 自定义类型构造，可以使用 Pydantic 的 `parse_obj_as` (`parse_raw_as`) 方法进行构造。

```python
from pydantic import parse_obj_as

# 由字典构造消息段
parse_obj_as(
    MessageSegment, {"type": "text", "data": {"text": "text"}}
) == MessageSegment.text("text")
# 由字典数组构造消息序列
parse_obj_as(
    Message,
    [MessageSegment.text("text"), {"type": "text", "data": {"text": "text"}}],
) == Message([MessageSegment.text("text"), MessageSegment.text("text")])
```

::: warning
以上示例中的字典数据仅做参考，具体的数据格式由适配器自行定义。
:::

### 获取消息纯文本

由于消息中存在各种类型的消息段，因此 `str(message)` 通常并不能得到消息的纯文本，而是一个消息序列的字符串表示。

NoneBot2 为消息段定义了一个方法 `is_text()` ，可以用于判断消息段是否为纯文本；也可以使用 `message.extract_plain_text()` 方法获取消息纯文本。

```python
# 判断消息段是否为纯文本
MessageSegment.text("text").is_text() == True
# 提取消息纯文本字符串
Message(
    [MessageSegment.text("text"), MessageSegment.at(123)]
).extract_plain_text() == "text"
```

### 遍历

`Message` 继承自 `List[MessageSegment]` ，因此可以使用 `for` 循环遍历消息段。

```python
for segment in message:
    ...
```

### 索引与切片

`Message` 对列表的索引与切片进行了增强，在原有列表 int 索引与切片的基础上，支持 `type` 过滤索引与切片。

```python
message = Message(
    [
        MessageSegment.text("test"),
        MessageSegment.image("test2"),
        MessageSegment.image("test3"),
        MessageSegment.text("test4"),
    ]
)

# 索引
message[0] == MessageSegment.text("test")
# 切片
message[0:2] == Message(
    [MessageSegment.text("test"), MessageSegment.image("test2")]
)

# 类型过滤
message["image"] == Message(
    [MessageSegment.image("test2"), MessageSegment.image("test3")]
)
# 类型索引
message["image", 0] == MessageSegment.image("test2")
# 类型切片
message["image", 0:2] == Message(
    [MessageSegment.image("test2"), MessageSegment.image("test3")]
)
```

同样的，`Message` 对列表的 `index`、`count` 方法也进行了增强，可以用于索引指定类型的消息段。

```python
# 指定类型首个消息段索引
message.index("image") == 1
# 指定类型消息段数量
message.count("image") == 2
```

此外，`Message` 添加了一个 `get` 方法，可以用于获取指定类型指定个数的消息段。

```python
# 获取指定类型指定个数的消息段
message.get("image", 1) == Message([MessageSegment.image("test2")])
```

### 拼接消息

`str`、`Message`、`MessageSegment` 对象之间可以直接相加，相加均会返回一个新的 `Message` 对象。

```python
# 消息序列与消息段相加
Message([MessageSegment.text("text")]) + MessageSegment.text("text")
# 消息序列与字符串相加
Message([MessageSegment.text("text")]) + "text"
# 消息序列与消息序列相加
Message([MessageSegment.text("text")]) + Message([MessageSegment.text("text")])
# 字符串与消息序列相加
"text" + Message([MessageSegment.text("text")])

# 消息段与消息段相加
MessageSegment.text("text") + MessageSegment.text("text")
# 消息段与字符串相加
MessageSegment.text("text") + "text"
# 消息段与消息序列相加
MessageSegment.text("text") + Message([MessageSegment.text("text")])
# 字符串与消息段相加
"text" + MessageSegment.text("text")
```

如果需要在当前消息序列后直接拼接新的消息段，可以使用 `Message.append`、`Message.extend` 方法，或者使用自加。

```python
msg = Message([MessageSegment.text("text")])
# 自加
msg += "text"
msg += MessageSegment.text("text")
msg += Message([MessageSegment.text("text")])
# 附加
msg.append("text")
msg.append(MessageSegment.text("text"))
# 扩展
msg.extend([MessageSegment.text("text")])
```

### 使用消息模板

为了提供安全可靠的跨平台模板字符, 我们提供了一个消息模板功能来构建消息序列

它在以下常见场景中尤其有用:

- 多行富文本编排(包含图片,文字以及表情等)

- 客制化(由 Bot 最终用户提供消息模板时)

在事实上, 它的用法和`str.format`极为相近, 所以你在使用的时候, 总是可以参考[Python 文档](https://docs.python.org/zh-cn/3/library/stdtypes.html#str.format)来达到你想要的效果

这里给出几个简单的例子:

::: warning
这里面所有的 `Message` 均是用对应的[协议适配器](<!-- TODO: 补充链接 -->)实现导入的, 而不是抽象基类
:::

```python title="基础格式化用法"
>>> Message.template("{} {}").format("hello", "world")
Message(
    MessageSegment.text("hello"),
    MessageSegment.text(" "),
    MessageSegment.text("world")
)
```

```python title="对消息段进行安全的拼接"
>>> Message.template("{}{}").format(MessageSegment.image("file:///..."), "world")
Message(
    MessageSegment(type='image', data={'file': 'file:///...'}),
    MessageSegment(type='text', data={'text': 'world'})
)
```

```python title="以消息对象作为模板"
>>> Message.template(
...     MessageSegment.text('{user_id}') + MessageSegment.face(233) +
...     MessageSegment.text('{message}')
... ).format_map({'user_id':123456, 'message':'hello world'}
...
Message(
    MessageSegment(type='text', data={'text': '123456'}),
    MessageSegment(type='face', data={'face': 233}),
    MessageSegment(type='text', data={'text': 'hello world'})
)
```

```python title="使用消息段的拓展控制符"
>>> Message.template("{link:image}").format(link='https://...')
Message(MessageSegment(type='image', data={'file': 'https://...'}))
```
