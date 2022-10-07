---
sidebar_position: 1
description: 内置依赖注入
---

# 内置依赖注入

::: warning
本章节为[读取与自定义配置](../../tutorial/plugin-basic/get-data)的拓展内容，请务必在阅读并理解之后再阅读本节内容。
:::

## Bot

获取当前事件的 Bot 对象。

```python {7-9}
from nonebot.adapters import Bot

async def _(bot: Bot): ...
async def _(bot): ...  # 兼容性处理
```

## Event

获取当前事件。

```python {6-8}
from nonebot.adapters import Event

async def _(event: Event): ...
async def _(event): ...  # 兼容性处理
```

## EventType

获取当前事件的类型。

```python {3}
from nonebot.params import EventType

async def _(foo: str = EventType()): ...
```

## EventMessage

获取当前事件的消息。

```python {4}
from nonebot.adapters import Message
from nonebot.params import EventMessage

async def _(foo: str = EventMessage()): ...
```

## EventPlainText

获取当前事件的消息纯文本部分。

```python {3}
from nonebot.params import EventPlainText

async def _(foo: str = EventPlainText()): ...
```

## EventToMe

获取当前事件是否与机器人相关。

```python {3}
from nonebot.params import EventToMe

async def _(foo: bool = EventToMe()): ...
```

## State

获取当前事件处理上下文状态，State 为一个字典，用户可以向 State 中添加数据来保存状态等操作。（请注意不要随意覆盖 State 中 NoneBot 的数据）

```python {4}
from nonebot.typing import T_State

async def _(foo: T_State): ...
```

## Command

获取当前命令型消息的元组形式命令名。

```python {7}
from nonebot import on_command
from nonebot.params import Command

matcher = on_command("cmd")

@matcher.handle()
async def _(foo: Tuple[str, ...] = Command()): ...
```

::: tips
命令详情只能在首次接收到命令型消息时获取，如果在事件处理后续流程中获取，则会获取到不同的值。
:::

## RawCommand

获取当前命令型消息的文本形式命令名。

```python {7}
from nonebot import on_command
from nonebot.params import RawCommand

matcher = on_command("cmd")

@matcher.handle()
async def _(foo: str = RawCommand()): ...
```

::: tips
命令详情只能在首次接收到命令型消息时获取，如果在事件处理后续流程中获取，则会获取到不同的值。
:::

## CommandArg

获取命令型消息命令后跟随的参数。

```python {8}
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg

matcher = on_command("cmd")

@matcher.handle()
async def _(foo: Message = CommandArg()): ...
```

::: tips
命令详情只能在首次接收到命令型消息时获取，如果在事件处理后续流程中获取，则会获取到不同的值。
:::

## CommandStart

获取命令型消息命令前缀。

```python {8}
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandStart

matcher = on_command("cmd")

@matcher.handle()
async def _(foo: str = CommandStart()): ...
```

::: tips
命令详情只能在首次接收到命令型消息时获取，如果在事件处理后续流程中获取，则会获取到不同的值。
:::

## ShellCommandArgs

获取 shell 命令解析后的参数。

::: tips
如果参数解析失败，则为 [`ParserExit`](builtin-exception#ParserExit) 异常，并携带错误码与错误信息。

由于 `ArgumentParser` 在解析到 `--help` 参数时也会抛出异常，这种情况下错误码为 `0` 且错误信息即为帮助信息。
:::

```python {8,12}
from nonebot import on_shell_command
from nonebot.params import ShellCommandArgs

matcher = on_shell_command("cmd", parser)

# 解析失败
@matcher.handle()
async def _(foo: ParserExit = ShellCommandArgs()): ...

# 解析成功
@matcher.handle()
async def _(foo: Dict[str, Any] = ShellCommandArgs()): ...
```

## ShellCommandArgv

获取 shell 命令解析前的参数列表。

```python {7}
from nonebot import on_shell_command
from nonebot.params import ShellCommandArgs

matcher = on_shell_command("cmd")

@matcher.handle()
async def _(foo: List[str] = ShellCommandArgv()): ...
```

## RegexMatched

获取正则匹配结果。

```python {7}
from nonebot import on_regex
from nonebot.params import RegexMatched

matcher = on_regex("regex")

@matcher.handle()
async def _(foo: str = RegexMatched()): ...
```

## RegexGroup

获取正则匹配结果的 group 元组。

```python {7}
from nonebot import on_regex
from nonebot.params import RegexGroup

matcher = on_regex("regex")

@matcher.handle()
async def _(foo: Tuple[Any, ...] = RegexGroup()): ...
```

## RegexDict

获取正则匹配结果的 group 字典。

```python {7}
from nonebot import on_regex
from nonebot.params import RegexDict

matcher = on_regex("regex")

@matcher.handle()
async def _(foo: Dict[str, Any] = RegexDict()): ...
```

## Matcher

获取当前事件响应器实例。

```python {7}
from nonebot import on_message
from nonebot.matcher import Matcher

foo = on_message()

@foo.handle()
async def _(matcher: Matcher): ...
```

## Received

获取某次 `receive` 接收的事件。

```python {8}
from nonebot import on_message
from nonebot.adapters import Event
from nonebot.params import Received

matcher = on_message()

@matcher.receive("id")
async def _(foo: Event = Received("id")): ...
```

## LastReceived

获取最近一次 `receive` 接收的事件。

```python {8}
from nonebot import on_message
from nonebot.adapters import Event
from nonebot.params import LastReceived

matcher = on_message()

@matcher.receive("any")
async def _(foo: Event = LastReceived()): ...
```

## Arg

获取某次 `got` 接收的参数。

```python {8-9}
from nonebot.params import Arg
from nonebot import on_message
from nonebot.adapters import Message

matcher = on_message()

@matcher.got("key")
async def _(key: Message = Arg()): ...
async def _(foo: Message = Arg("key")): ...
```

## ArgStr

获取某次 `got` 接收的参数，并转换为字符串。

```python {7-8}
from nonebot import on_message
from nonebot.params import ArgStr

matcher = on_message()

@matcher.got("key")
async def _(key: str = ArgStr()): ...
async def _(foo: str = ArgStr("key")): ...
```

## ArgPlainText

获取某次 `got` 接收的参数的纯文本部分。

```python {7-8}
from nonebot import on_message
from nonebot.params import ArgPlainText

matcher = on_message()

@matcher.got("key")
async def _(key: str = ArgPlainText()): ...
async def _(foo: str = ArgPlainText("key")): ...
```

## Exception

获取事件响应器运行中抛出的异常。

```python {4}
from nonebot.message import run_postprocessor

@run_postprocessor
async def _(e: Exception): ...
```

## Default

带有默认值的参数，便于复用依赖。

```python {1}
async def _(foo="bar"): ...
```
