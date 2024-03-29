---
sidebar_position: 2
description: 配置项
---

# 配置项

NoneBot2 使用 [`pydantic`](https://pydantic-docs.helpmanual.io/) 以及 [`python-dotenv`](https://saurabh-kumar.com/python-dotenv/) 来读取配置。配置项需符合特殊格式或 json 序列化格式。详情见 [`pydantic Field Type`](https://pydantic-docs.helpmanual.io/usage/types/) 文档。

## 配置项的加载

在 NoneBot2 中，我们可以把配置项通过来源简单分为 `直接传入`、`系统环境变量`、`dotenv` 三个，其加载优先级依次从高到低。

### 直接传入

在 NoneBot2 初始化的过程中，可以通过 `nonebot.init()` 传入任意合法的 Python 变量，也可以通过 `config` 在初始化完成后传入。

通常，在初始化前的传参会在 bot 的入口文件（通常为 `bot.py`）中进行，而初始化后的传参通常会在插件中进行。

```python
import nonebot

# 初始化前
nonebot.init(custom_config3="config on init")

# 初始化后
config = nonebot.get_driver().config
config.custom_config3 = "changed after init"
config.custom_config4 = "new config after init"
```

### 系统环境变量

在 `env` 中定义的配置项，也会在环境变量中进行寻找，如果发现同名配置项，将会覆盖 `env` 中所填入的值。例如在环境变量中 `CUSTOM_CONFIG="config in system environment variables"`，`env` 中 `USTOM_CONFIG="config in env file"`，那么在 NoneBot2 的配置中最终会被读取的为环境变量中的内容，即 `"config in system environment variables"`。

值得注意是，NoneBot2 不会自发读取未被定义的环境变量，如果需要读取某一环境变量需要在 `dotenv` 进行声明。

### dotenv

作为专门用配置项加载的功能，[`dotenv`](https://saurabh-kumar.com/python-dotenv/) 可以高效、统一的管理大量配置项，是我们最推荐的配置存放及加载的方式。

NoneBot2 在启动时将会从系统环境变量或者 `.env` 文件中寻找变量 `ENVIRONMENT`（大小写不敏感），默认值为 `prod`。这将引导 NoneBot2 从系统环境变量或者 `.env.{ENVIRONMENT}` 文件中进一步加载具体配置。

#### 配置项解析

`.env` 相关文件的加载使用 [`dotenv`](https://saurabh-kumar.com/python-dotenv/) 语法，并使用 [Pydantic](https://pydantic-docs.helpmanual.io/) 以 JSON 格式进行配置处理。例如：

```bash
# Default Configs
HOST=0.0.0.0  # 配置 NoneBot2 监听的 IP/主机名
PORT=8080  # 配置 NoneBot2 监听的端口
SUPERUSERS=["123456789", "987654321"]  # 配置 NoneBot 超级用户
NICKNAME=["awesome", "bot"]  # 配置机器人的昵称
COMMAND_START=["/", ""]  # 配置命令起始字符
COMMAND_SEP=["."]  # 配置命令分割字符

# Custom Configs
CUSTOM_CONFIG_STR="config in env file"
CUSTOM_CONFIG_EMPTY_STR=
CUSTOM_CONFIG_NONE
```

其中包含的默认配置项可在[进阶 - 内置配置项](../../advanced/functions/builtin-config.md)中查看。

如果配置项值无法被解析为 JSON 元素（例如 `HOST=0.0.0.0`）将作为**字符串**处理。如果配置项取值为空（例如 `CUSTOM_CONFIG_EMPTY_STR=`）会被解析为**空字符串**。如果配置项没有取值（例如 `CUSTOM_CONFIG_NONE`）则会被解析为**空值**。

#### .env 文件

`.env` 文件是基础环境配置文件，该文件中的配置项在不同环境下都会被加载，但会被 `.env.{ENVIRONMENT}` 文件中的配置所**覆盖**。

现在，我们在 `.env` 文件中写入当前环境信息：

```bash
# .env
ENVIRONMENT=dev
CUSTOM_CONFIG=common config  # 这个配置项在任何环境中都会被加载
```

如你所想，之后 NoneBot2 就会从 `.env.dev` 文件中加载环境变量。

#### .env.* 文件

`.env.*` 类似于预设，可以让用户在多套不同的配置方案中灵活切换，默认含有两套预设配置：`.env.dev`、`.env.prod`。

NoneBot 默认会从 `.env.{ENVIRONMENT}` 文件加载配置，其中 `ENVIRONMENT` 来自于 `.env` 文件中的配置项，若无此配置则会采用默认值 `prod`。同时，在 NoneBot2 初始化时可以指定加载某个环境配置文件：`nonebot.init(_env_file=".env.dev")`，这将忽略你在 `.env` 中设置的 `ENVIRONMENT`。

## 读取配置项

配置项可以通过三种类型的对象获取：`driver`、`adapter`、`bot`。

```python
import nonebot

# 已有配置 custom_config = 'custom_config_info'

# driver
nonebot.get_driver().config.custom_config
# bot
nonebot.get_bot().config.custom_config
# adapter
nonebot.get_driver()._adapters["adapter_name"].config.custom_config
```

以上三种方式均可读取配置项，任选其一即可。

例如，我们在配置项中含有 `SUPERUSERS=["1234567890","0987654321"]` 项，那么我们可以通过以下方式获取此项的内容:

```python
import nonebot

su_list = nonebot.get_driver().config.superusers
# su_list == set(["1234567890", "0987654321"])
```

## 使用配置模型

在一个涉及大量配置项的插件中，通过直接读取配置项的方式显然并不高效，同时由于额外的全局配置项没有预先定义的问题，导致开发时编辑器无法提示字段与类型，以及运行时没有对配置项直接进行检查。那么就需要一种方式来规范定义插件配置项。

在 NoneBot2 中，我们使用强大高效的 `Pydantic` 来定义配置模型，这个模型可以被用于配置的读取和类型检查等。例如在插件目录中新建 `config.py` 来定义一个模型：

```python title=config.py
from typing import Optional

from pydantic import BaseSettings


class Config(BaseSettings):

    custom_config_int: Optional[int] = 123456
    custom_config_str: Optional[str] = None
    custom_config_bool: bool = True
    custom_config_dict: dict = {"key": "value"}
```

定义完成配置模型后，我们可以在插件加载时获取全局配置，导入插件自身的配置模型：

```python title=__init__.py
from nonebot import get_driver

from .config import Config

plugin_config = Config.parse_obj(get_driver().config)
```

然后，我们便可以从 `plugin_config` 中读取配置了，例如 `plugin_config.custom_config_int`。

这种方式可以简洁、高效、统一的定义大量配置信息，并可以设置默认取值，防止由于配置项丢失所造成的插件崩溃。
