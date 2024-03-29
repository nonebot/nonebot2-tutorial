---
sidebar_position: 4
description: 事件响应器进阶
---

# 事件响应器进阶

::: warning
本章节为[事件响应器](../../tutorial/plugin-basic/matcher.md)的拓展内容，请务必在阅读并理解之后再阅读本节内容。
:::

## 事件响应器的参数

### 通用参数

事件响应器的通用参数为任何事件响应器的辅助函数均支持的参数。

#### 事件响应规则-rule

事件响应器的响应规则是一个 `Rule` 对象，它是一系列 `checker` 的集合，当所有的 `checker` 都返回 `True` 时，才会触发该响应器。

```py
from nonebot import on_message

on_message(rule=Rule(_checker))
```

详情请参考[教程 - 自定义规则](../../tutorial/plugin-advance/rule.md)。

#### 事件处理函数列表-handler

事件处理函数列表是一个 `List[Union[T_Handler, Dependent]]` 对象，其中存放着该事件响应器的事件处理函数。通常我们会选择[事件响应器的依赖处理装饰器](../../tutorial/plugin-basic/handler.md#事件处理函数)来添加事件处理函数，而较少直接在事件响应器的注册阶段进行修改。

#### 临时事件响应器-temp

临时事件响应器是一个 `bool` 对象，声明该事件响应器为临时事件响应器，该事件响应器在触发过一次后便会被销毁。在事件响应器被销毁后仍可重新注册响应器。

```py
from nonebot import on_message

on_message(temp=True)
```

#### 有效期-expire_time

有效期是一个 `Union[datetime, timedelta]` 对象，为事件响应器设置有效期（或过期时间），在超出有效期后无法再次触发该响应器并销毁。在事件响应器被销毁后仍可重新注册响应器。

```py
from nonebot import on_message
from datetime import timedelta

on_message(expire_time=timedelta(seconds=300))
```

关于 datetime 模块的用法，请参考[官方文档](https://docs.python.org/3/library/datetime.html)。

#### 优先级-priority

优先级是一个 `int` 对象，事件响应器的优先级代表事件响应器的执行顺序。默认的优先级为 `1`。

同一优先级的事件响应器会**同时执行**，优先级数字**越小**越先响应！优先级请从 `1` 开始排序！

```py
from nonebot import on_message

on_message(priority=10)
```

#### 阻断-block

阻断是一个 `bool` 对象，当有任意事件响应器发出了阻止事件传递信号时，该事件将不再会传递给下一优先级，直接结束处理。

NoneBot 内置的事件响应器中，所有非 `command` 规则的 `message` 类型的事件响应器都会阻断事件传递，其他则不会。

```py
from nonebot import on_message

on_message(block=True)
```

#### 上下文-state

事件响应器的上下文是一个 `T_State` 对象，即 `Dict[Any, Any]` 对象，用于存放一个事件处理流程中的上下文信息。在事件响应器被触发后，会将此处传入的state并入该事件处理流程的上下文信息中。

```py
from nonebot import on_message

on_message(state={'key':'value'})
```

详情请参考[进阶 - 依赖注入](builtin-dependency-injection#State)。

### 特殊参数

事件响应器的特殊参数为部分响应器支持的参数。在使用此部分参数前请务必参考[事件响应器的辅助函数](#事件响应器的辅助函数)中列出的可用范围。

#### 事件类型-type

事件类型即是该响应器所要响应的事件类型，只有在接收到的事件类型与该响应器的类型相同时，才会触发该响应器。如果类型留空，该响应器将会响应所有类型的事件。目前**仅有** [`on`](#on) 含有此参数。

NoneBot 内置了四种主要类型：`meta_event`、`message`、`notice`、`request`。通常情况下，协议适配器会将事件合理地分类至这四种类型中。如果有其他类型的事件需要响应，可以自行定义新的类型。

```py
from nonebot import on

on('message')
on('custom_type')
```

#### 事件响应权限-permission

事件响应器的响应权限是一个 `Permission` 对象，它也是一系列 `checker` 的集合，当其中一个 `checker` 返回 `True` 时，就会触发该响应器。

```py
from nonebot import on_message

on_message(permission=SUPERUSER)
```

详情请参考[教程 - 权限控制](../../tutorial/plugin-basic/permission)。

#### msg

`msg` 是一个 `Union[str, Tuple[str, ...]]` 对象，用于匹配消息事件的内容。在不同的辅助函数中匹配模式也有所不同。如果事件响应器的辅助函数包含此参数，**此参数为必填参数**。

```py
from nonebot import on_command, on_fullmatch

on_fullmatch('msg_arg')
```

### cmd

`cmd` 是一个 `Union[str, Tuple[str, ...]]` 对象，用于匹配消息事件的内容。如果事件响应器的辅助函数包含此参数，**此参数为必填参数**。

`msg` 和 `cmd` 的区别在于，包含 `cmd` 参数的辅助函数所生成的事件响应器为**命令类型**的事件响应器，匹配规则有所不同，详情请参考 [`on_command`](#on_command) 和 [`on_shell_command`](#on_shell_command)。

```py
from nonebot import on_command

## env 中 COMMAND_SEP=["."] COMMAND_START=["/"]

on_command('test')           # 响应 /test
on_command({'test','alpha'}) # 响应 /test.alpha
```

#### keywords

`keywords` 是一个 `Set[str]` 对象，用于存放关键词列表。在被匹配的消息的纯文本部分中如果含哟 `keywords` 中的元素即可响应成功。目前**仅有** [`on_keyword`](#on_keyword) 含有此参数。

```py
from nonebot import on_keyword

on_keyword({'key', 'word', 'keywords'})
```

#### aliases

`aliases` 是一个 `Set[Union[str, Tuple[str, ...]]]` 对象，用于存放*命令别名*，通常和 [`cmd`](#cmd) 同时出现。其中每一个元素的作用均等价于 [`cmd`](#cmd) 的作用。

值得注意的是，我们并不能仅使用 `aliases` 而不填写 [`cmd`](#cmd)，`aliases` 仅作为 [`cmd`](#cmd) 的补充而不是替代。

```py
from nonebot import on_command

on_command('cmd_arg', aliases={'cmd','arg','命令'})
```

#### ignorecase

`ignorecase` 是一个 `bool` 对象，用于声明事件响应器是否可以忽略大小写进行匹配。

```py
from nonebot import on_startswith

on_startswith('msg_arg', ignorecase=True)
```

#### parser

`parser` 是一个 `nonebot.rule.ArgumentParser` 对象，继承自 `argparse.ArgumentParser` ，用于解析 `shell_like` 的参数。具体用法可以参考 [python官方文档](https://docs.python.org/3/library/argparse.html) 的介绍。目前**仅有** [`on_shell_command`](#on_shell_command) 含有此参数。

```py
from nonebot import on_shell_command
from nonebot.rule import ArgumentParser

arg_parser = ArgumentParser()
arg_parser.add_argument('--foo', help='foo help')
on_shell_command('msg_arg', parser=arg_parser)
```

#### pattern

`pattern` 是一个 `str` 对象，用于存放正则表达式。具体用法可以参考 [python官方文档](https://docs.python.org/3/library/re.html) 的介绍。目前**仅有** [`on_regex`](#on_regex) 含有此参数。

```py
from nonebot import on_regex

on_regex(r'^abc$')
```

#### flags

`flags` 是一个 `Union[int, re.RegexFlag]` 对象，用于存放正则匹配标志。具体用法可以参考 [python官方文档](https://docs.python.org/3/library/re.html) 的介绍。目前**仅有** [`on_regex`](#on_regex) 含有此参数。

```py
from nonebot import on_regex

on_regex(r'^abc$', flags=1)
```

## 事件响应器的辅助函数

事件响应器的辅助函数共有12种。其中 `on`、`on_metaevent`、`on_request`、`on_notice`、`on_message` 四种为直接调用 `Matcher.new()` 进行响应器的创建，`on_startswith`、`on_endswith`、`on_fullmatch`、`on_keyword`、`on_command`、`on_shell_command`、`on_regex` 函数都是在 `on_message` 的基础上添加了对应的匹配规则 `rule` 而成的。

### on

注册一个基础事件响应器，可自定义响应的消息类型。

可用参数：

- [type](#事件类型-type)(特殊)
- [rule](#事件响应规则-rule)
- [permission](#事件响应权限-permission)(特殊)
- [handlers](#事件处理函数列表-handler)
- [temp](#临时事件响应器-temp)
- [expire_time](#有效期-expire_time)
- [priority](#优先级-priority)
- [block](#阻断-block)
- [state](#上下文-state)

### on_metaevent

注册一个元事件响应器。

可用参数：

- [rule](#事件响应规则-rule)
- [handlers](#事件处理函数列表-handler)
- [temp](#临时事件响应器-temp)
- [expire_time](#有效期-expire_time)
- [priority](#优先级-priority)
- [block](#阻断-block)
- [state](#上下文-state)

### on_request

注册一个请求事件响应器。

可用参数：

- [rule](#事件响应规则-rule)
- [handlers](#事件处理函数列表-handler)
- [temp](#临时事件响应器-temp)
- [expire_time](#有效期-expire_time)
- [priority](#优先级-priority)
- [block](#阻断-block)
- [state](#上下文-state)

### on_notice

注册一个通知事件响应器。

可用参数：

- [rule](#事件响应规则-rule)
- [handlers](#事件处理函数列表-handler)
- [temp](#临时事件响应器-temp)
- [expire_time](#有效期-expire_time)
- [priority](#优先级-priority)
- [block](#阻断-block)
- [state](#上下文-state)

### on_message

注册一个消息事件响应器。

可用参数：

- [rule](#事件响应规则-rule)
- [permission](#事件响应权限-permission)(特殊)
- [handlers](#事件处理函数列表-handler)
- [temp](#临时事件响应器-temp)
- [expire_time](#有效期-expire_time)
- [priority](#优先级-priority)
- [block](#阻断-block)
- [state](#上下文-state)

### on_startswith

注册一个消息事件响应器，并且当消息的**文本部分**以指定内容开头时响应。

可用参数：

- [msg](#msg)(特殊)(必填)
- [rule](#事件响应规则-rule)
- [ignorecase](#ignorecase)(特殊)
- [permission](#事件响应权限-permission)(特殊)
- [handlers](#事件处理函数列表-handler)
- [temp](#临时事件响应器-temp)
- [expire_time](#有效期-expire_time)
- [priority](#优先级-priority)
- [block](#阻断-block)
- [state](#上下文-state)

### on_endswith

注册一个消息事件响应器，并且当消息的**文本部分**以指定内容结尾时响应。

可用参数：

- [msg](#msg)(特殊)(必填)
- [rule](#事件响应规则-rule)
- [ignorecase](#ignorecase)(特殊)
- [permission](#事件响应权限-permission)(特殊)
- [handlers](#事件处理函数列表-handler)
- [temp](#临时事件响应器-temp)
- [expire_time](#有效期-expire_time)
- [priority](#优先级-priority)
- [block](#阻断-block)
- [state](#上下文-state)

### on_fullmatch

注册一个消息事件响应器，并且当消息的**文本部分**与指定内容完全一致时响应。

可用参数：

- [msg](#msg)(特殊)(必填)
- [rule](#事件响应规则-rule)
- [ignorecase](#ignorecase)(特殊)
- [permission](#事件响应权限-permission)(特殊)
- [handlers](#事件处理函数列表-handler)
- [temp](#临时事件响应器-temp)
- [expire_time](#有效期-expire_time)
- [priority](#优先级-priority)
- [block](#阻断-block)
- [state](#上下文-state)

### on_keyword

注册一个消息事件响应器，并且当消息纯文本部分包含关键词时响应。

可用参数：

- [keywords](#keywords)(特殊)(必填)
- [rule](#事件响应规则-rule)
- [permission](#事件响应权限-permission)(特殊)
- [handlers](#事件处理函数列表-handler)
- [temp](#临时事件响应器-temp)
- [expire_time](#有效期-expire_time)
- [priority](#优先级-priority)
- [block](#阻断-block)
- [state](#上下文-state)

### on_command

注册一个消息事件响应器，并且当消息以指定命令开头时响应。

根据配置里提供的 [`command_start`](builtin-config#command-start), [`command_sep`](builtin-config#command-separator) 判断消息是否为 `command`。

可用参数：

- [cmd](#cmd)(特殊)(必填)
- [rule](#事件响应规则-rule)
- [aliases](#aliases)(特殊)
- [permission](#事件响应权限-permission)(特殊)
- [handlers](#事件处理函数列表-handler)
- [temp](#临时事件响应器-temp)
- [expire_time](#有效期-expire_time)
- [priority](#优先级-priority)
- [block](#阻断-block)
- [state](#上下文-state)

### on_shell_command

注册一个支持 `shell_like` 解析参数的命令消息事件响应器。

与 `on_command` 相同，`on_shell_command` 采用**类似**的方法来判断消息是否为 `shell_command`，但与之不同的是，`shell_command` 会额外检查是否**包含命令以外**的内容，即参数内容。

`on_shell_command` 通常被用于需要多个参数的场景。在添加 `parser` 参数时, 响应器会自动处理消息，并将用户输入的原始参数列表保存在 `state["argv"]`, `parser` 处理的参数保存在 `state["args"]` 中。

可用参数：

- [cmd](#cmd)(特殊)(必填)
- [rule](#事件响应规则-rule)
- [aliases](#aliases)(特殊)
- [parser](#parser)(特殊)
- [permission](#事件响应权限-permission)(特殊)
- [handlers](#事件处理函数列表-handler)
- [temp](#临时事件响应器-temp)
- [expire_time](#有效期-expire_time)
- [priority](#优先级-priority)
- [block](#阻断-block)
- [state](#上下文-state)

使用方法：

```python
from nonebot import on_shell_command
from nonebot.rule import ArgumentParser

## env 中 COMMAND_SEP=["."] COMMAND_START=["/"]

parser = ArgumentParser()
parser.add_argument("--a", action="store")
parser.add_argument("-y" , action="store_true")

rule = on_shell_command("ls", parser=parser)
# /ls --a test -y
# state['a'] == 'test'
# state['y'] == True
```

### on_regex

注册一个消息事件响应器，并且当消息匹配正则表达式时响应。

可用参数：

- [pattern](#pattern)(特殊)(必填)
- [flags](#flags)(特殊)
- [rule](#事件响应规则-rule)
- [permission](#事件响应权限-permission)(特殊)
- [handlers](#事件处理函数列表-handler)
- [temp](#临时事件响应器-temp)
- [expire_time](#有效期-expire_time)
- [priority](#优先级-priority)
- [block](#阻断-block)
- [state](#上下文-state)

## 事件响应器组

事件响应器组是用于批量创建拥有相同参数的响应器所设计的。

在响应器组实例化时，传入的参数将会被作为**默认参数**，后续调用此响应器组所创建的事件响应器中将会被传入这些默认参数，从而避免**重复填写相同参数**。

如果响应器组中某个响应器需要传入**与默认参数不同**的参数时，可以直接在调用方法时传入新的参数，在新参数存在时将会**覆盖**掉默认参数。

### MatcherGroup

事件响应器组合，统一管理。为 `Matcher` 创建提供默认属性。

可用参数：

- **kwargs: [`on`](#on) 的参数默认值，可被其所属命令覆盖

`MatcherGroup` 目前支持全部辅助函数的调用，在用法上与其对应的的辅助函数相同。

```py
from nonebot import MatcherGroup

matcher_group = MatcherGroup(priority=10, block=False)
matcher_cmd   = matcher_group.on_command('cmd')
matcher_start = matcher_group.on_startswith('start', ignorecase=True, temp=True)
matcher_regex = matcher_group.on_regex(r'^regex$', priority=15)
```

上述写法等价于：

```py
from nonebot import on_command, on_startswith, on_regex

matcher_cmd   = on_command('cmd', priority=10)
matcher_start = on_startswith('start', ignorecase=True, temp=True, priority=10, block=False)
matcher_regex = on_regex(r'^regex$', priority=15, block=False)
```

### CommandGroup

注册一个命令组，用于声明一组有相同名称前缀的命令。

可用参数：

- cmd: 命令前缀 **(必填)(不可覆盖)**
- **kwargs: [`on_command`](#on_command) 的参数默认值，可被其所属命令覆盖

`CommandGroup` 目前支持的命令有 [`command`](#on_command) 和 [`shell_command`](#on_shell_command) 两种，在用法上与其对应的的辅助函数相同。

```py
from nonebot import CommandGroup

# env 中 COMMAND_SEP=["."] COMMAND_START=["/"]

cmd_group = CommandGroup('prefix')
matcher_0 = cmd_group.command('0') # 响应 /prefix.0
matcher_1 = cmd_group.command('1') # 响应 /prefix.1
matcher_2 = cmd_group.command('2') # 响应 /prefix.2
```
