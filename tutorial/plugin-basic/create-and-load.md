---
sidebar_position: 1
description: 01_创建并加载插件
---

# 创建并加载插件

## 创建插件

在[插件入门](overview.md#插件结构)中，我们介绍了插件的基本格式——模块插件与包插件。那么创建插件自然也就是创建一个符合以上两种格式的插件即可。

同样，我们也可以使用 nb-cli 来方便快捷的创建一个插件。

<!-- TODO: 补充 nb-cli 创建插件的方法 -->

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

有关其他插件加载的方式，可参考 [跨插件访问](../插件开发（高级）/跨插件访问.md) 和 [嵌套插件](../插件开发（高级）/嵌套插件.md)。
