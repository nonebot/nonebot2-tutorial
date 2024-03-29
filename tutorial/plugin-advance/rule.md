---
sidebar_position: 5
description: 自定义响应规则
---

# 自定义响应规则

机器人在实际应用中，往往会接收到多种多样的事件类型，NoneBot2 提供了可自定义的响应规则 ── `Rule`。

在 [进阶 - 事件响应器及辅助函数](../../advanced/functions/matcher-advanced.md#事件响应规则-rule) 中，我们提到了响应规则是一个 `Rule` 对象。类似于 `Message` 与 `MessageSegement` 的关系，`Rule` 也有自己的子项 `RuleChecker`。

## `RuleChecker`

`RuleChecker` 是一个返回值为 `Bool` 类型的依赖函数，即 `RuleChecker` 支持依赖注入。例如：

```python {4-5}
from nonebot import on_message
from nonebot.adapters import Event


async def user_checker(event: Event) -> bool:
    return event.get_user_id() == "123123"


matcher = on_message(rule=user_checker)
```

在上面的代码中，我们定义了一个函数 `user_checker`，它检查事件的用户 ID 是否等于 `"123123"`。这个函数 `user_checker` 即为一个 `RuleChecker`。

## `Rule`

`Rule` 是若干个 `RuleChecker` 的集合，只有当所有 `RuleChecker` 检查通过时匹配成功。

```python {4-5,7-8,10}
from nonebot import on_message
from nonebot.adapters import Event


async def user_checker(event: Event) -> bool:
    return event.get_user_id() == "123123"


async def message_checker(event: Event) -> bool:
    return event.get_plaintext() == "hello"


rule = Rule(user_checker, message_checker)
matcher = on_message(rule=rule)
```

在上面的代码中，我们定义了两个函数 `user_checker` 和 `message_checker`，它们检查事件的用户 ID 是否等于 `"123123"`，以及消息的内容是否等于 `"hello"`。随后，我们定义了一个 `Rule` 对象，它包含了这两个函数。

## 合并响应规则

在定义响应规则时，我们可以将规则进行细分，来更好地复用规则。而在使用时，我们需要合并多个规则。除了使用 `Rule` 对象来组合多个 `RuleChecker` 外，我们还可以对 `Rule` 对象进行合并。

```python {4-6}
rule1 = Rule(foo_checker)
rule2 = Rule(bar_checker)

rule = rule1 & rule2
rule = rule1 & bar_checker
rule = foo_checker & rule2
```

同时，你也无需担心合并了一个 `None` 值，`Rule` 会忽略 `None` 值。

```python
assert (rule & None) is rule
```
