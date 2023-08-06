# SetupPanel
Intuitive and flexible configuration of interactive embed-based setup panels
for `discord.py`. This library provides convenient abstraction of "normal" setup
panel code into a powerful, yet simple API.

## Requirements
- Python 3.6+
- `discord.py`

## Getting Started
If you would like to install `discord.py` along with this library, in your
terminal, run:
```
pip install -U setuppanel[dpy]
```
To install `discord.py` with voice capabilities, run:
```
pip install -U setuppanel[dpyv]
```
Or to install just this library, run:
```
pip install -U setuppanel
```
You're all set! However, it is recommended to install to a *Virtual Environment*
to avoid polluting your global package installation. For more information,
[read here](https://docs.python.org/3/tutorial/venv.html).

## API

### `setuppanel.SetupPanel`

#### Attributes
- **info** `Union[List[Tuple[str, bool, bool, bool]], None]`: information about
  the steps in a `SetupPanel` instance. If steps have been added, returns a
  list of tuples of the name, conditional flag, loop flag, and group_loop flag
  of each step. Otherwise, `None`
- **is_used** `bool`: if the `SetupPanel` instance has already been run
- **`len(SetupPanel)`** `int`: the number of steps this setup panel will run

#### Parameters
- **bot** `Union[Bot, AutoShardedBot]`: the instance of a discord bot
- **ctx** `Context`: the command's invocation context
- **title** `str`: the title of this setup panel
- **duplicate_roles** `Optional[bool]`: whether or not this setup panel allows
  duplicate roles to be specified during a looping step, default `False`
- **duplicate_role_embed** `Optional[discord.Embed]`: the embed to send if a
  duplicate role is received and `duplicate_roles` is `False`. Defaults to `None`
- **duplicate_emojis** `Optional[bool]`: whether or not this setup panel allows
  duplicate emojis to be specified during a looping step, default `False`
- **duplicate_emoji_embed** `Optional[discord.Embed]`: the embed to send if a
  duplicate emoji is received and `duplicate_emojis` is `False`. Defaults to `None`
- **error_color** `Optional[Union[discord.Color, int]]`: the color of the embed
  that will be sent for the timeout and canceled message

### Setup Operation Names
Below are all the various setup names that can be passed into the `name` and `names`
parameters of the API functions.

>Please note that the typing information merely describes the return type of a
> step with a given name, not that the name should be of that type. Provide the
> name as stated below, for example, content would be provided as `name="content"`

- content `str`
- message `str` *(alias for content)*
- channel `discord.TextChannel`
- role `discord.Role`
- emoji `str`
- reaction `str` *(alias for emoji)*
- member `discord.Member`
- integer `int`
- float `float`
- title `Union[str, EmptyEmbed]`
- description `Union[str, EmptyEmbed]`
- color `discord.Color`
- author `Union[str, None]`
- footer `Union[str, None]`
- url `Union[str, None]`

### Add Step
- Usage: `SetupPanel.add_step(params)`
- Parameters:
  - **name** `str`: see [valid names](#setup-operation-names)
  - **embed** `discord.Embed`: the embed to display during the step
  - **timeout** `Optional[int]`: the time (in seconds) to wait for a user to respond
    with an option that satisfies `predicate`. Defaults to `120`
  - **predicate** `Optional[Callable]`: a function that accepts the output of the
    appropriate `bot.wait_for` listener and returns a `bool`
- Returns class instance for fluuid chaining


### Add Conditional Step
- Usage: `SetupPanel.add_conditional_step(params)`
- Parameters:
  - **name** `str`: see [valid names](#setup-operation-names)
  - **embed** `discord.Embed`: the embed to display during the step
  - **condition** `Callable`: a function that accepts the output of the last step,
    returning a `bool`. Step will be executed if the result of `condition` is
    `True`, otherwise the result of this step will be `None`
  - **timeout** `Optional[int]`: the time (in seconds) to wait for a user to respond
    with an option that satisfies `predicate`. Defaults to `120`
  - **predicate** `Optional[Callable]`: a function that accepts the output of the
    appropriate `bot.wait_for` listener and returns a `bool`
- Returns class instance for fluuid chaining

### Add Looping Step
- Usage: `SetupPanel.add_until_finish(params)`
- Parameters:
  - **name** `str`: see [valid names](#setup-operation-names)
  - **embed** `discord.Embed`: the embed to display during the step
  - **break_check** `Callable`: a function that accepts the same arguments as `predicate`,
    returning a `bool`. If the result of `break_check` is `True`, it will break out
    of the loop, proceeding to the next step. The result of this step is an aggregate
    list of individual results of each loop
  - **timeout** `Optional[int]`: the time (in seconds) to wait for a user to respond
    with an option that satisfies `predicate`. Defaults to `120`
  - **predicate** `Optional[Callable]`: a function that accepts the output of the
    appropriate `bot.wait_for` listener and returns a `bool`
- Returns class instance for fluuid chaining

### Add Grouped Looping Step
- Usage: `SetupPanel.add_group_loop(params)`
- Parameters:
  - **names** `List[str]`: see [valid names](#setup-operation-names)
  - **embeds** `List[discord.Embed]`: the embed to display during the step
  - **break_checks** `List[Callable]`: a list of functions that accept the same
    arguments as `predicates` for each function, returning a `bool`. If the
    result of `break_check` for a step is `True`, it will break out of the loop,
    proceeding to the next step. The result of this step is an aggregate
    list of the tuple of individual results of each loop
  - **timeouts** `List[int]`: list of the time (in seconds) to wait for a user to respond
    with an option that satisfies `predicates`
  - **predicates** `Optional[List[Callable]]`: a list of functions that accept the
    output of the appropriate `bot.wait_for` listener and returns a `bool`
- Returns class instance for fluuid chaining
> **Note:** *The length of each of the list parameters must be the same*

### Start Setup
- Usage: `await SetupPanel.start()`
- Returns the aggregate list of the results of all setup steps in order. If
  setup is canceled or times out, returns `None`

## Examples
```python
import discord
from discord.ext import commands
from discord.ext.commands import AutoShardedBot, Context
from setuppanel import SetupPanel


class ExampleCog(commands.Cog):
    def __init__(self, bot: AutoShardedBot) -> None:
        self.bot = bot

    @commands.command()
    async def setuptest(self, ctx: Context):
        sp = SetupPanel(
            bot=self.bot,
            ctx=ctx,
            title="Test Setup Panel",
        ).add_step(
            name="content",
            embed=discord.Embed(
                title="Test Setup",
                description=f"{ctx.author.mention}, message content please",
                color=discord.Color.blue(),
            ),
            timeout=300,
        )
        for name in ["channel", "role", "member"]:
            sp.add_step(
                name=name,
                embed=discord.Embed(
                    title="Test Setup",
                    description=f"{ctx.author.mention}, mention a {name}",
                    color=discord.Color.blue(),
                ),
                timeout=300,
            )
        sp.add_until_finish(
            name="content",
            embed=discord.Embed(
                title="Test Setup",
                description=f"{ctx.author.mention}, message content please",
                color=discord.Color.blue(),
            ),
            timeout=300,
            break_check=lambda m: m.content == "finish" and m.author == ctx.author and m.channel == ctx.channel,
        ).add_conditional_step(
            name="integer",
            embed=discord.Embed(
                title="Test Setup",
                description=f"{ctx.author.mention}, please specify an integer value",
                color=discord.Color.blue(),
            ),
            timeout=300,
            condition=lambda lv: bool(lv)
        ).add_group_loop(
            names=["content", "integer"],
            embeds=[
                discord.Embed(
                    title="Test Setup",
                    description=f"{ctx.author.mention}, say something",
                    color=discord.Color.blue().
                ),
                discord.Embed(
                    title="Test Setup",
                    description=f"{ctx.author.mention}, say a number",
                    color=discord.Color.blue().
                )
            ],
            timeouts=[300, 300],
            break_checks=[
                lambda m: m.content == "stop looping",
                None,
            ],
        )
        res = await sp.start()
        await ctx.channel.send(content=res)


def setup(bot: AutoShardedBot) -> None:
    bot.add_cog(Testing(bot))
```