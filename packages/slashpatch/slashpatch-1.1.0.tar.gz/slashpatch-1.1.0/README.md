# vcokltfre/SlashPatch

## A command handler/dispatcher webserver for Discord slash commands

Example:
```py
from slashpatch import Server, Context, command, Cog

app = Server('c293758d88bc26d54963f05676a8fa6c3404570169e350afd5c1f318bf52732a')

class Example(Cog):
    @command(name="example")
    async def example(self, ctx: Context):
        print(ctx.raw)
        return ctx.respond("Hello, world!", ephemeral=True)

    @command(name="cases")
    async def cases(self, ctx: Context):
        return ctx.respond(embed={"description":"h"})

app.add_cog(Example())
```

Then run:

`uvicorn main:app --host 0.0.0.0`