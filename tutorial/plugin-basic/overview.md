---
sidebar_position: 0
description: 00_概览
---

# 插件入门

插件(`Plugin`)是 NoneBot2 中实现具体功能的最小单位，也是用户对事件进行处理的基础单位。

::: tips
假如说使用 NoneBot2 搭建的机器人是一个人的话，NoneBot2 框架可以理解为这个机器人的身体，能够做出各种各样的行为（例如发送消息），但必须依赖于大脑产生的指令来活动，而自身并不会自主产生任意活动。而插件则是这个机器人的“大脑”，虽然自身并不能独立活动，但可以通过向身体发出指令来执行其功能。
:::

## 插件结构

在正式编写插件之前，首先我们需要了解一下插件的概念。

在 NoneBot2 中，插件可以是 Python 的一个[模块](https://docs.python.org/zh-cn/3/tutorial/modules.html) `module`，也可以是一个[包](https://docs.python.org/zh-cn/3/tutorial/modules.html#packages) `package` 。NoneBot2 会在导入时对这些模块或包做一些特殊的处理使得他们成为一个插件。插件间应尽量减少耦合，可以进行有限制的插件间调用，NoneBot2 能够正确解析插件间的依赖关系。

### 模块插件（单文件形式）

一个 `.py` 文件即可被称为模块插件了，例如：

```tree title=Project
📂 plugins
└── 📜 foo.py
```

这个时候 `foo.py` 已经可以被称为一个插件了，尽管它还什么都没做。

### 包插件（文件夹形式）

一个包含了 `__init__.py` 文件的文件夹即可被称为包插件了，例如：

```tree title=Project
📂 plugins
└── 📂 foo
    └── 📜 __init__.py
```

这个时候 `foo` 就是一个合法的 Python 包了，同时也是合法的 NoneBot2 插件，插件内容可以在 `__init__.py` 中编写。

## 插件示例

这里我们将展示 NoneBot2 内置插件 `echo` 的内容以及其实际效果：

```python title=echo.py
from nonebot.rule import to_me
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.plugin import on_command

echo = on_command("echo", to_me())


@echo.handle()
async def echo_escape(message: Message = CommandArg()):
    await echo.send(message=message)
```

在[配置项](../plugin-advance/config)中存在 `COMMAND_START=["/", "!!"]` 的情况下，我们私聊机器人可见：

<!-- TODO: 这里放个echo插件的示例图片 -->
