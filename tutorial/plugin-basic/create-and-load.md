---
sidebar_position: 1
description: 01_创建并加载插件
---

# 创建并加载插件

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

## 加载插件

::: danger
请勿在插件被加载前 `import` 插件模块，这会导致 NoneBot2 无法将其转换为插件而损失部分功能。
:::

加载插件通常在机器人的入口文件进行，例如在[创建项目](<!-- TODO: 补充链接 -->)中创建的项目中的 `bot.py` 文件。在 NoneBot2 初始化完成后即可加载插件。

```python title=bot.py {5}
import nonebot

nonebot.init()

# load your plugin here

nonebot.run()
```

加载插件的方式有多种，但在底层的加载逻辑是一致的。以下是为加载插件提供的几种方式：

### `load_plugin`

通过点分割模块名称或使用 [`pathlib`](https://docs.python.org/zh-cn/3.8/library/pathlib.html) 的 `Path` 对象来加载插件。通常用于加载单个插件或者是第三方插件。例如：

```python
from pathlib import Path

nonebot.load_plugin("path.to.your.plugin")
nonebot.load_plugin(Path("./path/to/your/plugin.py"))
```

### `load_plugins`

加载传入插件目录中的所有插件，通常用于加载一系列本地编写的插件。例如：

```python
nonebot.load_plugins("src/plugins", "path/to/your/plugins")
```

::: warning
请注意，插件所在目录应该为相对机器人 **入口文件（通常为 bot.py）** 可导入的，例如与入口文件在 **同一目录** 下。
:::

### `load_all_plugins`

这种加载方式是以上两种方式的混合，加载所有传入的插件模块名称，以及所有给定目录下的插件。例如：

```python
nonebot.load_all_plugins(["path.to.your.plugin"], ["path/to/your/plugins"])
```

### `load_from_json`

通过 JSON 文件加载插件，是 [`load_all_plugins`](#load_all_plugins) 的 JSON 变种。通过读取 JSON 文件中的 `plugins` 字段和 `plugin_dirs` 字段进行加载。例如：

```json title=plugin_config.json
{
  "plugins": ["path.to.your.plugin"],
  "plugin_dirs": ["path/to/your/plugins"]
}
```

```python
nonebot.load_from_json("plugin_config.json", encoding="utf-8")
```

::: tips
如果 JSON 配置文件中的字段无法满足你的需求，可以使用 [`load_all_plugins`](#load_all_plugins) 方法自行读取配置来加载插件。
:::

### `load_from_toml`

通过 TOML 文件加载插件，是 [`load_all_plugins`](#load_all_plugins) 的 TOML 变种。通过读取 TOML 文件中的 `[tool.nonebot]` Table 中的 `plugins` 和 `plugin_dirs` Array 进行加载。例如：

```toml title=plugin_config.toml
[tool.nonebot]
plugins = ["path.to.your.plugin"]
plugin_dirs = ["path/to/your/plugins"]
```

```python
nonebot.load_from_toml("plugin_config.toml", encoding="utf-8")
```

::: tips
如果 TOML 配置文件中的字段无法满足你的需求，可以使用 [`load_all_plugins`](#load_all_plugins) 方法自行读取配置来加载插件。
:::

### `load_builtin_plugin`

加载一个内置插件，传入的插件名必须为 NoneBot2 内置插件。该方法是 [`load_plugin`](#load_plugin) 的封装。例如：

```python
nonebot.load_builtin_plugin("echo")
```

### `load_builtin_plugins`

加载传入插件目录中的所有内置插件

### 其他加载方式

有关其他插件加载的方式，可参考 [跨插件访问](../plugin-advance/require.md) 和 [嵌套插件](../plugin-advance/nested-plugin.md))。
