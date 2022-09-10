---
sidebar_position: 3
description: 03_事件处理流程
---

# 事件处理流程

在我们收到事件，并被某个事件响应器正确响应后，便正式开启了对于这个事件的 **事件处理流程**。

## 认识事件处理流程

就像我们在解决问题时需要遵循流程一样，处理一个事件也需要一套流程。在事件响应器对一个事件进行响应之后，会依次执行 `事件处理函数`，

简单来说，事件处理流程并不是一个函数、一个对象或一个方法，而是一整套由开发者设计的流程。

在这个流程中，我们**目前**只需要了解两个概念——“事件处理函数” 和 “事件响应器操作”。

### 事件处理函数

在事件响应器中，事件处理流程由一个或多个 `事件处理函数` 组成，每个 `事件处理函数` 都是一个 `Dependent`，详情可以参考 [进阶 - 依赖注入](../../进阶/功能/依赖注入.md)。通常我们会采用事件响应器的 `事件处理函数装饰器` 来添加这些 `事件处理函数`。

顾名思义，事件响应器的 `事件处理函数装饰器` 是 [decorator](https://docs.python.org/zh-cn/3/glossary.html#term-decorator)，那么它的使用方法也同[函数定义](https://docs.python.org/zh-cn/3/reference/compound_stmts.html#function-definitions)中所展示的包装用法相同。例如：

```python title=foo.py {6,8}
from nonebot.plugin import on_command

matcher = on_command("ping")


@matcher.handle()
async def handle_func():
    pass  # do something here
```

如上方示例所示，我们使用 `matcher` 响应器的 `handle` 装饰器装饰了一个函数 `handle_func` 。`handle_func` 函数会被自动转换为 `Dependent` 对象，并被添加到 `matcher` 的事件处理流程中。

::: tips
如果这个概念目前仍难以理解，你目前仅需要知道这种方法可以在事件响应器被调起之后自动调用 `handle_func` 来对事件进行处理即可。
:::

目前 NoneBot2 共提供了 `handle`、`receive` 和 `got` 三种依赖处理装饰器，同时也可通过其他手段为事件响应器添加处理依赖，具体内容可参考 [进阶 - 事件处理依赖及事件响应器操作](../../进阶/功能/事件处理依赖及事件响应器操作.md)。

### 事件响应器操作

在事件处理流程中，我们可以使用事件响应器操作来进行一些交互或改变事件处理流程，例如向用户发送消息或提前结束事件处理流程等。

事件响应器操作实际上同依赖处理装饰器一样，也是作为 `Matcher` 类的[类方法](https://docs.python.org/zh-cn/3/library/functions.html?highlight=classmethod#classmethod)存在，因此事件响应器操作的调用方法也是 `Matcher.func()` 的形式。不过不同的是，事件响应器操作并不是装饰器，因此并不需要@进行标注。

```python title=weather.py {8,9}
from nonebot.plugin import on_command

matcher = on_command("天气", priority=10)  # 注册事件响应器


@matcher.handle()  # 为事件响应器添加一个处理函数
async def handle_func():
    # await matcher.send("天气是...")
    await matcher.finish("天气是...")
```

如上方示例所示，我们使用 `matcher` 响应器的 `finish` 事件响应器操作方法向用户回复了 `天气是...` 并结束了事件处理流程。效果如下图所示：

<!-- TODO: 这里放个实例 -->

值得注意的是，在使用了 `finish` 方法之后，NoneBot2 会在向用户回复其中的消息内容后抛出 `FinishedException` 来结束事件事件响应流程的后续操作。也就是说，如果在 `finish` 被执行后，后续的程序是不会被执行的（如果你需要回复用户消息但不想事件处理流程结束，可以使用被注释的部分中展示的 `send` 方法）。

::: danger
由于 `finish` 是通过抛出 `FinishedException` 来结束事件的，因此抛出异常后可能会被未加限制的 `try-except` 捕获，影响事件处理流程正确处理，导致无法正常结束此事件。请务必在异常捕获中指定错误类型，或将 `finish` 移出捕获范围进行使用。
:::

目前 NoneBot2 共提供了多种事件响应器操作，其中包括用于用户交互与流程控制两大类，具体内容可参考 [进阶 - 事件处理依赖及事件响应器操作](../../进阶/功能/事件处理依赖及事件响应器操作.md)。
