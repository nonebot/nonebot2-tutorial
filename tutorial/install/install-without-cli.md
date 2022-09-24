---
sidebar_position: 1
description: 不使用 nb-cli 安装创建机器人
---

# 不使用 nb-cli 安装创建机器人

::: warning
我们十分不推荐直接创建机器人项目，请您优先考虑使用 nb-cli 进行项目创建。
:::

在本节中，我们将简要介绍如何在不使用 nb-cli 的方式创建一个机器人项目的**最小实例**，但我们十分不建议对于长期运行的或需要发布的项目使用此类方法进行部署，如果您需要在不使用 nb-cli 的情况下部署此类型的项目，请考虑使用 poetry 或其他项目管理工具。

一个机器人项目的**最小实例**中**至少**需要包含以下内容:

- 入口文件：初始化并运行机器人
- 配置项文件：存储机器人启动所需的参数
- 插件：为机器人提供具体的功能

## 安装依赖

在创建项目前，我们首先需要将项目所需依赖安装至环境中。详情请参考[这里](<!-- TODO: 补充链接 -->)。

同时，如果你使用了第三方插件，你也需要在**运行之前**将插件安装到环境或项目中。详情见[加载插件](#加载插件)

## 创建配置项文件

配置项文件是用于存放 NoneBot2 运行所需要的必备及额外配置项目的文件，使用 [`pydantic`](https://pydantic-docs.helpmanual.io/) 以及 [`python-dotenv`](https://saurabh-kumar.com/python-dotenv/) 来读取配置。配置项需符合特殊格式或 json 序列化格式。详情可见[配置项](../plugin-advance/config#dotenv)

在**项目的根目录**中创建一个 `.env` 文件，并写入以下内容:

```python title=bot.py
HOST=0.0.0.0  # 配置 NoneBot2 监听的 IP/主机名
PORT=8080  # 配置 NoneBot2 监听的端口
SUPERUSERS=["123456789", "987654321"]  # 配置 NoneBot 超级用户
NICKNAME=["awesome", "bot"]  # 配置机器人的昵称
COMMAND_START=["/", ""]  # 配置命令起始字符
COMMAND_SEP=["."]  # 配置命令分割字符
```

关于其中配置项的详细信息，可参考[配置项](../plugin-advance/config#dotenv)

## 加载插件

插件(`Plugin`)是 NoneBot2 中实现具体功能的最小单位，也是用户对事件进行处理的基础单位。如果在不加载任何插件的情况下启动项目，那么机器人是无法对你的任何输入做出响应的。

可参考[这里](../plugin-basic/create-and-load#加载插件)了解如何加载插件。

可参考[这里](<!-- TODO: 补充链接 -->)了解如何安装并加载第三方插件。

在不使用 nb-cli 时，我们将会介绍如何在入口文件中加载插件。

## 创建入口文件

入口文件（`ENTRYPOINT`）顾名思义，是用来初始化并启动此项目的文件。

::: tips
在使用 nb-cli 时入口文件的功能将会被 `nb run` 命令所替代，所以并不需要额外准备入口文件
:::

在**项目的根目录**中创建一个入口文件，例如 `bot.py`，并写入以下内容:

```python title=bot.py
import nonebot
from nonebot.adapters.YOUR_ADAPTER_NAME import Adapter as YOUR_ADAPTER_NAME


nonebot.init()
app = nonebot.get_asgi()

# load plugins here
nonebot.load_plugin('your_plugin')

driver = nonebot.get_driver()
driver.register_adapter(YOUR_ADAPTER_NAME)

if __name__ == "__main__":
    nonebot.run(app="__mp_main__:app")
```

::: danger
请将示例中的 `YOUR_ADAPTER_NAME` 替换为你所需要的适配器名！可参考[这里](<!-- TODO: 补充链接 -->)进行适配器的选择。
请根据你的需要修改**加载插件部分**(`nonebot.load_plugin('your_plugin')`)的代码，不要直接运行！可参考[这里](#加载插件)加载插件。
:::

在创建完毕并修改好适配器及插件后，我们便完成了入口文件部分的创建。

## 运行bot

在**项目的根目录**中，使用配置好环境的 Python 解释器执行入口文件，例如 `python bot.py`，便可在不使用 nb-cli 的情况下运行机器人了。
