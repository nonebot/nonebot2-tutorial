---
sidebar_position: 1
description: 定时任务
---

# 定时任务

[APScheduler](https://apscheduler.readthedocs.io/en/3.x/) 是一个Python第三方库，其强大的定时任务功能被广泛应用于各个场景。在 NoneBot2 中，定时任务作为一个额外功能，依赖于基于 APScheduler 开发的 [`nonebot_plugin_apscheduler`](https://github.com/nonebot/plugin-apscheduler) 插件进行支持。

## 安装 nonebot_plugin_apscheduler

由于 `nonebot_plugin_apscheduler` 并不作为 NoneBot2 的标准功能，并不会随之一并安装。使用前请先自行安装 `nonebot_plugin_apscheduler` 插件。可参考 ***这里*** 来了解并选择安装插件的方式。

<!-- TODO: 补充安装插件部分的链接 -->

```bash
# 使用 nb-cli (推荐)
nb plugin install nonebot-plugin-apscheduler
# 使用 poetry
poetry add nonebot-plugin-apscheduler
# 使用 pip
pip install nonebot-plugin-apscheduler
```

## 使用 nonebot_plugin_apscheduler

`nonebot_plugin_apscheduler` 本质上是对 [APScheduler](https://apscheduler.readthedocs.io/en/3.x/) 进行了封装以适用于 NoneBot2 开发，因此其使用方式与 APScheduler 本身并无显著区别。在此我们会简要介绍其调用方法，更多的使用方面的功能请参考[APScheduler 官方文档](https://apscheduler.readthedocs.io/en/3.x/userguide.html)。

### 导入 scheduler 对象

由于 `nonebot_plugin_apscheduler` 作为插件，引起需要在使用前对其进行**加载**并**调用**其中的 `scheduler` 对象来创建定时任务。使用 `require` 方法可轻松完成这一过程。可参考 [跨插件访问](require) 一节进行了解。

首先我们先来演示一种较老的写法：

```python
from nonebot import require

scheduler = require("nonebot_plugin_apscheduler").scheduler
```

在上述示例中获取的 `scheduler` 即为 [AsyncIOScheduler](https://apscheduler.readthedocs.io/en/3.x/modules/schedulers/asyncio.html#apscheduler.schedulers.asyncio.AsyncIOScheduler) 对象。但遗憾的是，此方法引入的 `scheduler` 对象无法正确的被编辑器识别，因此无法直接获取类型提示等信息。

同时，我们也可以使用另一种在 NoneBot2-beta 版**新引入**的方法方法来获取 `scheduler` 对象。

```python
from nonebot import require

require("nonebot_plugin_apscheduler")

from nonebot_plugin_apscheduler import scheduler
```

相对第一种方法，在使用第二种方法时可以在编辑器（例如 VSCode）中获得类型提示等信息，可以帮助我们更轻松的编写代码，是较为推荐的引入方式。

### 添加定时任务

在 [APScheduler 官方文档](https://apscheduler.readthedocs.io/en/3.x/userguide.html#adding-jobs) 中提供了以下两种直接添加任务的方式：

```python
from nonebot import require

require("nonebot_plugin_apscheduler")

from nonebot_plugin_apscheduler import scheduler

# 基于装饰器的方式（推荐）
@scheduler.scheduled_job("cron", hour="*/2", id="job_0", args=[1], kwargs={arg2: 2})
async def run_every_2_hour(arg1, arg2):
    pass


# 基于add_job方法的方式
def run_every_day(arg1, arg2):
    pass


scheduler.add_job(
    run_every_day, "interval", days=1, id="job_1", args=[1], kwargs={arg2: 2}
)
```

::: warning
由 APScheduler 的定时任务并不是 **由事件响应器所触发的事件**，因此其处理函数无法同[事件处理依赖](../plugin-basic/handler#事件处理函数)一样通过[依赖注入](../plugin-basic/get-data#认识依赖注入)获取上下文信息，也无法通过事件响应器对象的方法进行任何操作，因此我们需要使用[调用平台API](call-api)的方式来获取信息或收发消息。
相对于事件处理依赖而言，编写定时任务更像是编写普通的函数，需要我们自行获取信息以及发送信息，请务必**不要**将事件处理依赖的特殊语法用于定时任务！
:::

关于 APScheduler 的更多使用方法，可以参考 [APScheduler 官方文档](https://apscheduler.readthedocs.io/en/3.x/index.html) 进行了解。

### 配置项

#### apscheduler_autostart

- **类型**: `bool`
- **默认值**: `True`

是否自动启动 `scheduler` ，若不启动需要自行调用 `scheduler.start()`。

#### apscheduler_log_level

- **类型**: `int`
- **默认值**: `30`

apscheduler 输出的日志等级

- `WARNING` = `30` (默认)
- `INFO` = `20`
- `DEBUG` = `10` (只有在开启 nonebot 的 debug 模式才会显示 debug 日志)

#### apscheduler_config

- **类型**: `dict`
- **默认值**: `{ "apscheduler.timezone": "Asia/Shanghai" }`

`apscheduler` 的相关配置。参考 [配置 scheduler](https://apscheduler.readthedocs.io/en/latest/userguide.html#scheduler-config), [配置参数](https://apscheduler.readthedocs.io/en/latest/modules/schedulers/base.html#apscheduler.schedulers.base.BaseScheduler)

配置需要包含 `apscheduler.` 作为前缀，例如 `apscheduler.timezone`。
