from nonebot.plugin import on_command

matcher = on_command('ping')

@matcher.handle()
async def _():
    await matcher.finish('pong!')

try:
    pass
except:
    pass