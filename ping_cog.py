from discord.ext import commands

class ping_cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='ping')
    async def _ping(self, ctx: commands.Context):
        m = await ctx.channel.send("Ping?")
        m.edit("Pong! Latency is {}ms. API Latency is {}ms".format(round((m.created_at - ctx.message.created_at).total_seconds() * 1000), round(self.bot.latency * 1000)))