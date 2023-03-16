from discord.ext import commands
import re

class eval_cog(commands.Cog):
    def __init__(self, bot: commands.Bot, owner_id: int):
        self.bot = bot
        self.owner_id = owner_id

    @commands.command(name='eval')
    async def _eval(self, ctx: commands.Context, *, arg: str):
        """Evaluate some code on the host machine.
        Only the bot owner can run this command.
        """

        if not ctx.author.id == self.owner_id:
            await ctx.channel.send("Unauthorized user up in my grill! You trying to hack my Catch-a-Ride? Uncool bro, uncool.")
            return
        else:
            try:
                code = " ".join(re.split(r" +", arg.strip().strip("` ")))
                evaled = eval(code)
                if not type(evaled) is str:
                    evaled = str(evaled)
                await ctx.channel.send("```xl\n{}\n```".format(evaled))
            except Exception as e:
                await ctx.channel.send("`ERROR` ```xl\n${}\n```".format(e))