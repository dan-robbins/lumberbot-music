import ast
from discord.ext import commands

MAX_DISCORD_MESSAGE_LENGTH = 2000

def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.AsyncWith):
        insert_returns(body[-1].body)


async def eval_stmts(stmts, env=None):
    """
    Evaluates input.
    If the last statement is an expression, that is the return value.
    >>> from asyncio import run
    >>> run(eval_stmts("1+1"))
    2
    >>> ctx = {}
    >>> run(eval_stmts("ctx['foo'] = 1", {"ctx": ctx}))
    >>> ctx['foo']
    1
    >>> run(eval_stmts('''
    ... async def f():
    ...    return 42
    ...
    ... await f()'''))
    42
    """

    parsed_stmts = ast.parse(stmts)

    fn_name = "_eval_expr"

    fn = f"async def {fn_name}(): pass"
    parsed_fn = ast.parse(fn)

    for node in parsed_stmts.body:
        ast.increment_lineno(node)

    insert_returns(parsed_stmts.body)

    parsed_fn.body[0].body = parsed_stmts.body
    exec(compile(parsed_fn, filename="<ast>", mode="exec"), env)

    return await eval(f"{fn_name}()", env)

def code_block_escape(s):
    ns = ""
    count = 0
    for c in s:
        if c == "`":
            count += 1
            if count == 3:
                ns += "\N{ZERO WIDTH JOINER}"
                count = 1
        else:
            count = 0

        ns += c
    return ns

class eval_cog(commands.Cog):
    def __init__(self, bot: commands.Bot, owner_id: int):
        self.bot = bot
        self.owner_id = owner_id

    @commands.command(name='eval')
    async def _eval(self, ctx: commands.Context, *, stmts=None):
        """Evaluate arbitrary Python code on the host machine.
        Only the bot owner can run this command.
        """

        if not ctx.author.id == self.owner_id:
            await ctx.channel.send("Unauthorized user up in my grill! You trying to hack my Catch-a-Ride? Uncool bro, uncool.")
            return
        else:
            if stmts is None:
                return
            else:
                try:
                    stmts = stmts.strip().strip("`")
                    if not stmts:
                        await ctx.send("After stripping `'s, stmts can't be empty.")
                        return

                    res = await eval_stmts(stmts, {"bot": self.bot, "ctx": ctx})
                    escaped = code_block_escape(repr(res))
                    message = f"```python\n{escaped}\n```"
                    if len(message) > MAX_DISCORD_MESSAGE_LENGTH:
                        # The reason that we can safely truncate the message
                        # is because of how code_block_escape works
                        prefix = "Truncated result to length 0000:\n"
                        suffix = "\n```"
                        message = message.rstrip("`").strip()

                        new_length = MAX_DISCORD_MESSAGE_LENGTH - len(prefix) - len(suffix)
                        prefix = prefix.replace("0000", str(new_length))
                        message = prefix + message[:new_length] + suffix

                    await ctx.channel.send(message)
                except Exception as e:
                    await ctx.channel.send("`ERROR` ```xl\n${}\n```".format(e))