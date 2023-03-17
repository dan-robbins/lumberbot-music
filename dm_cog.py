import discord
import re
from discord.ext import commands
from datetime import datetime

class dm_cog(commands.Cog):
    def __init__(self, bot: commands.Bot, owner_id: int):
        self.bot = bot
        self.owner_id = owner_id
        self.id_regex = re.compile(r"\d{18}")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        
        if str(message.channel.type) == "private" and not message.author.id == self.bot.user.id and not message.author.id == self.owner_id:
            await self.bot.get_user(self.owner_id).send("DM recieved from {}#{}/{} at {}\nContent: {}".format(message.author.name, message.author.discriminator, message.author.id, datetime.now().strftime("%m/%d/%Y %H:%M:%S"), message.content))

        if str(message.channel.type) == "private" and message.author.id == self.owner_id and self.id_regex.match(message.content) is not None:
            if(len(message.content) > 19):
                reply_id = int(message.content[0:18])
                await self.bot.get_user(reply_id).send(message.content[19:])
            else:
                message.channel.send("Please include a message to send")