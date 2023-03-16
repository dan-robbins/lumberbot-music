from discord.ext import commands
import re

class eval_cog(commands.Cog):
    def __init__(self, bot: commands.Bot, owner_id: int):
        self.bot = bot
        self.owner_id = owner_id

    def clean_text(text):
        if type(text) is str:
            return re.sub(r"`", "`" + chr(8203), re.sub(r"@", "@" + chr(8203), text))
        else:
            return text

    @commands.command(name='eval')
    async def _eval(self, ctx: commands.Context, *, arg: str):
        if not ctx.author.id == self.owner_id:
            await ctx.channel.send("Unauthorized user up in my grill! You trying to hack my Catch-a-Ride? Uncool bro, uncool.")
            return
        else:
            try:
                code = " ".join(re.split(r" +", arg.strip().strip("` ")))
                evaled = eval(code)
                if not type(evaled) is str:
                    evaled = str(evaled)
                await ctx.channel.send(self.clean_text(evaled), {code:"xl"})
            except Exception as e:
                await ctx.channel.send("\`ERROR\` \`\`\`xl\n${}\n\`\`\`".format(self.clean_text(e)))