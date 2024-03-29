---
sidebar_position: 0
description: 内置配置项
---

# 内置配置项

::: warning
本章节为[配置项](../../tutorial/plugin-advance/config)的拓展内容，请务必在阅读并理解之后再阅读本节内容。
:::

## Driver

- **类型**: `str`
- **默认值**: `"~fastapi"`

NoneBot2 运行所使用的驱动器。主要分为 `ForwardDriver`、`ReverseDriver` 即客户端和服务端两类。

配置格式采用特殊语法：`<module>[:<Driver>][+<module>[:<Mixin>]]*`

其中 `<module>` 为驱动器模块名，可以使用 `~` 作为 `nonebot.drivers.` 的简写；`<Driver>` 为驱动器类名，默认为 `Driver`；`<Mixin>` 为驱动器混入的类名，默认为 `Mixin`。

NoneBot2 内置了几个常用驱动器，包括了各类常用功能，常见驱动器配置如下：

```env
DRIVER=~fastapi
DRIVER=~httpx+~websockets
DRIVER=~fastapi+~httpx+~websockets
DRIVER=~fastapi+~aiohttp
```

各驱动器的功能与区别请参考[选择驱动器](./choose-driver.md)。

## Host

- **类型**: `IPvAnyAddress`
- **默认值**: `127.0.0.1`

使用 `ReversedDriver` 时，NoneBot2 监听的 IP/主机名。

```env
HOST=127.0.0.1
```

## Port

- **类型**: `int`
- **默认值**: `8080`

使用 `ReversedDriver` 时，NoneBot2 监听的端口。

```env
PORT=8080
```

## Log Level

- **类型**: `int | str`
- **默认值**: `INFO`

NoneBot2 日志输出等级，可以为 `int` 类型等级或等级名称（日志等级名称应为大写，如 `INFO`）。

参考 [`loguru 日志等级`](https://loguru.readthedocs.io/en/stable/api/logger.html#levels)。

```env
LOG_LEVEL=INFO
```

## API Timeout

- **类型**: `Optional[float]`
- **默认值**: `30.0`

API 请求超时时间，单位为秒。

```env
API_TIMEOUT=30.0
```

## SuperUsers

- **类型**: `Set[str]`
- **默认值**: `set()`

机器人超级用户，可以使用权限 [`SUPERUSER`](../api/permission.md#SUPERUSER)。

```env
SUPERUSERS=["1234567890"]
```

## Nickname

- **类型**: `Set[str]`
- **默认值**: `set()`

机器人昵称，通常协议适配器会根据用户是否 @user 或者是否以机器人昵称开头来判断是否是向机器人发送的消息。

```env
NICKNAME=["bot"]
```

## Command Start

- **类型**: `Set[str]`
- **默认值**:
  - Command Start: `{"/"}`

命令消息的起始符。用于 [`command`](../api/rule.md#command) 规则。

```env
COMMAND_START={"/", "!"}
```

## Command Separator

- **类型**: `Set[str]`
- **默认值**:
  - Command Separator: `{"."}`

命令消息的分割符。用于 [`command`](../api/rule.md#command) 规则。

```env
COMMAND_START={"/", "!"}
COMMAND_SEP={".", "/"}
```

## Session Expire Timeout

- **类型**: `timedelta`
- **默认值**: `timedelta(minutes=2)`

用户会话超时时间，配置格式参考 [Datetime Types](https://pydantic-docs.helpmanual.io/usage/types/#datetime-types)。

```env
SESSION_EXPIRE_TIMEOUT=120
```
