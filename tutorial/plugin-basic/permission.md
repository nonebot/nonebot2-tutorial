---
sidebar_position: 6
description: 06_权限控制
---

# 权限控制

**权限控制**是机器人在实际应用中需要解决的重点问题之一，NoneBot2 提供了灵活的权限控制机制——`Permission`。

## 基础使用

`Permission` 是由非负整数个 `PermissionChecker` 所共同组成的 **用于筛选事件** 的对象。而相对于 [`Rule`](../plugin-advance/rule) 而言，`Permission` 则更侧重于对于 **发起事件的用户** 的筛选，例如由 NoneBot2 自身提供的 `SUPERUSER`，便是筛选出会话发起者是否为超级用户。它们可以对输入的用户进行鉴别，如果符合要求则会被认为通过并返回 `True`，反之则返回 `False`。

简单来说，`Permission` 是一个用于筛选出符合要求的用户的机制，可以通过 `Permission` 精确的控制响应对象的覆盖范围，从而拒绝掉我们所不希望的事件。

```python
from nonebot import on_command
from nonebot.permission import SUPERUSER


matcher = on_command("测试超管", permission=SUPERUSER)

@matcher.handle()
async def _():
    await matcher.send("超管命令测试成功")
```

如上方示例所示，在注册事件响应器时，我们设置了 `permission` 参数，那么这个事件处理器在触发事件前的检查阶段会对用户身份进行验证，如果不符合我们设置的条件（此处即为 [`超级用户`](../../advanced/functions/builtin-config#superusers)）则会响应失败。

目前，NoneBot2 内置了 `SUPERUSER` 一个针对用户的 `Permission`，和 `METAEVENT` `REQUEST` `NOTICE` `MESSAGE` 四个针对事件类型的 `Permission`，同时也可由协议适配器或用户自行定义更多的权限，并对权限进行 `或运算`。

```python title=weather.py
from nonebot.adapters import Message, MessageSegment
from nonebot.params import CommandArg
from nonebot.plugin import on_command
from nonebot.permission import SUPERUSER

# 通过此处的函数来获取天气信息
async def get_weather(city: str):
    weather = f"do something to get weather of {city}"
    return weather


matcher = on_command("天气", priority=10, permission=SUPERUSER)  # 注册事件响应器


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

如上方示例所示，我们在weather插件中加入了权限控制，目前此插件仅会对bot的 `超级用户` 进行响应，并忽略掉其他用户的请求。

## 进阶使用

::: warning
下列使用方法并不属于 `Permission` 的最基础的应用，如果您无法理解其内容，可以直接跳过下文。
:::

### Permission的连续性以及更新

与 `Rule` 不同的是，`Permission` 不会在会话状态更新时丢失，因此 `Permission` 通常用于会话的响应控制。

并且，当会话状态更新时，会执行 `permission_updater` 以更新 `Permission`。默认情况下，`permission_updater` 会在原有的 `Permission` 基础上添加一个 `USER` 条件，以检查事件的 `session_id` 是否与当前会话一致。

你可以自行定义 `permission_updater` 来控制会话的响应权限更新。`permission_updater` 是一个返回 `Permission` 的函数，可选依赖注入参数参考类型 `T_PermissionUpdater`。

```python {3,5}
matcher = on_message()

@matcher.permission_updater
async def update_type(matcher: Matcher):
    return matcher.permission  # return same without session_id check
```

### 在事件处理流程中调用

`Permission` 除了可以在注册事件响应器时加以应用，还可以在编写事件处理函数 `handler` 时主动调用，我们可以利用这个特性在一个 `handler` 里对不同权限的事件主体进行区别响应，下面我们以 OneBot 适配器中的 `GROUP_ADMIN`（普通管理员非群主）和 `GROUP_OWNER` 为例，说明下怎么进行主动调用。

```python
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from nonebot.adapters.onebot.v11 import GROUP_ADMIN, GROUP_OWNER

matcher = on_command("测试权限")

@matcher.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    if await GROUP_ADMIN(bot, event):
        await matcher.send("管理员测试成功")
    elif await GROUP_OWNER(bot, event):
        await matcher.send("群主测试成功")
    else:
        await matcher.send("群员测试成功")
```

在这段代码里，我们并没有对命令的权限指定，这个命令会响应所有在群聊中的 `测试权限` 命令，但是在 `handler` 里，我们对两个 `Permission` 进行主动调用，从而可以对不同的角色进行不同的响应。

### 自定义权限

如同 `Rule` 一样，`Permission` 也是由非负数个 `PermissionChecker` 组成的，但只需其中一个返回 `True` 时就会匹配成功。下面是自定义 `PermissionChecker` 和 `Permission` 的示例：

```python
from nonebot.adapters import Bot, Event
from nonebot.permission import Permission

async def async_checker(bot: Bot, event: Event) -> bool:
    return True

def sync_checker(bot: Bot, event: Event) -> bool:
    return True

def check(arg1, arg2):

    async def _checker(bot: Bot, event: Event) -> bool:
        return bool(arg1 + arg2)

    return Permission(_checker)
```

`Permission` 和 `PermissionChecker` 之间可以使用 `|`（或符号）互相组合：

```python
from nonebot.permission import Permission

Permission(async_checker1) | sync_checker | async_checker2
```

同样地，如果想用 `Permission(*checkers)` 包裹构造 `Permission`，函数可以是异步的，也可以是同步的。
