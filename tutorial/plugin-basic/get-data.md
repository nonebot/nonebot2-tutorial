---
sidebar_position: 4
description: 04_获取信息
---

# 获取信息

在 NoneBot2 中，获取事件相关信息的途径有很多，而目前最主要的途径有两种：`调用平台API` 和 `依赖注入`。本章节中我们将介绍通过  `依赖注入` 获取信息的方法，`调用平台API`的使用方法将在[调用平台API](../plugin-advance/call-api)中进行介绍。

值得注意的是，`调用平台API` 并不是专职用于获取信息所使用的，其更多是用于提供一些平台特殊功能，在获取信息方面也是作为 `依赖注入` 的补充进行少量使用的。大部分情况下 `依赖注入` 是获取信息的最佳途径。

## 认识依赖注入

在事件处理流程中，事件响应器具有自己独立的上下文，例如：当前的事件、机器人自身的信息或由其他处理依赖或事件处理流程所新增的参数等。在 NoneBot2 中，这些数据可以根据用户的需求，通过依赖注入的方式，被事件响应器的上下文注入到事件处理函数中。

相对于传统的信息获取方法，通过依赖注入获取信息的最大特色在于**按需获取**。如果该事件处理函数不需要任何额外信息即可运行，那么可以不进行依赖注入。如果事件处理函数需要额外的数据，可以通过依赖注入的方式灵活的标注出需要的依赖，在函数运行时便会被按需注入。

## 使用依赖注入获取上下文信息

使用依赖注入获取上下文信息的方法十分简单，我们仅需要在函数的参数中声明所需的依赖，并正确的将函数添加为处理依赖即可。例如：

```python
from nonebot import on_message
from nonebot.params import EventToMe

matcher = on_message()


@matcher.handle()
async def _(foo: bool = EventToMe()):
    return foo
```

在事件响应器被触发后，这个函数便可以通过依赖注入的方式获取到对应的信息。

```python title=weather.py
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.plugin import on_command

matcher = on_command("天气", priority=10)  # 注册事件响应器


@matcher.handle()  # 为事件响应器添加一个处理函数
async def handle_func(args: Message = CommandArg()):
    city = args.extract_plain_text()  # 获取用户发送的命令信息
    if city in ["广州", "上海"]:  #
        await matcher.finish(f"今天 {city} 的天气是...")
    else:
        await matcher.finish(f"您输入的城市 {city} 暂不支持查询，请重试...")
```

如上方示例所示，我们使用了 `args` 作为变量名，获取了注入的 `CommandArg()`，也就是 `命令型消息命令后跟随的参数` 项。在这个示例中，我们获得的参数会被检查是否有效，对无效参数则会结束事件。

<!-- TODO: 这里放个实例，演示带参数和不带参数两种情况 -->

目前 NoneBot2 共提供了多种可供注入的依赖，具体内容可参考 [进阶 - 内置依赖注入](../../advanced/functions/builtin-dependency-injection)。
