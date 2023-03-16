import discord
from discord.ext import commands
from datetime import datetime

class dm_cog(commands.Cog):
    def __init__(self, bot: commands.Bot, owner_id: int):
        self.bot = bot
        self.owner_id = owner_id

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        
        if not message.author.id == self.bot.user.id and not message.author.id == self.owner_id and str(message.channel.type) == "private":
            await self.bot.get_user(self.owner_id).send("DM recieved from {}#{} at {}\nContent: {}".format(message.author.name, message.author.discriminator, datetime.now().strftime("%m/%d/%Y %H:%M:%S"), message.content))