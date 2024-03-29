---
sidebar_position: 4
description: 跨插件访问
---

# 跨插件访问

`require` 是 NoneBot2 中用于获取其他插件中对象的一种函数。同时，此函数也可保证加载正确的顺序，被广泛用于需要依赖于其他插件中对象的场景中。

::: tips
在 NoneBot2-alpha 版中，该函数需要搭配 `export` 进行使用，这一特性在 NoneBot2-beta 及之后的版本中被移除。关于在旧版本中 `export` 的使用可以参考 [NoneBot2-a16 文档](https://61d3d9dbcadf413fd3238e89--nonebot2.netlify.app/advanced/export-and-require.html)。
:::

## 基础使用

假设，在 `plugin_a` 中存在一个常量 `PLUGIN_NAME`、函数 `add_a_and_b` 和类 `foo`。

```python title=plugin_a.py
PLUGIN_NAME = "plugin a"


def add_a_and_b(a: int, b: int) -> int:
    return a + b


class Foo:
    def sub_a_and_b(a: int, b: int) -> int:
        return a - b
```

我们需要在 `plugin_b` 插件中使用 `plugin_a` 中的对象时，便可用 `require` 进行获取。

```python title=plugin_b.py
from nonebot import require

require("plugin_a")

from plugin_a import PLUGIN_NAME, add_a_and_b, Foo


print(PLUGIN_NAME)
print(add_a_and_b(114, 514))
print(Foo.sub_a_and_b(1919, 810))
```

在 `plugin_b` 载入时，NoneBot2 会尝试在已加载的插件中搜索 `plugin_a`。若 `plugin_a` 未被加载则对其进行载入。确保其正确载入后便返回对应插件的 `plugin.module` 以供 `plugin_b` 调用。

由于 `require` 的返回值是目标插件的 `plugin.module`，因此函数、变量和类等 `一级对象` 是可以直接调用的，但对于闭包中的方法、类的方法等 `二级对象` 是无法直接引用的，需要引入其对于的 `一级对象` 并进行调用。

```python title=plugin_b.py
from nonebot import require

# 正确
add_a_and_b = require("plugin_a").add_a_and_b

# 错误
sub_a_and_b = require("plugin_a").foo.sub_a_and_b
```

## 确保加载顺序

如上文所提，在插件 `require` 其他插件时，NoneBot2 会尝试在已加载的插件中搜索，如果存在则直接返回对应插件的 `plugin.module`，若不存在则尝试加载对应的插件，成功则返回对应插件的 `plugin.module`，失败则抛出 `RuntimeError`。

相对于使用 `load_plugin` 等方法加载插件，`require` 加载可以避免插件重复加载，这使得对于拥有复杂依赖关系的插件不会因加载顺序的问题或插件重复加载导致的错误。
