import os

import discord
from dotenv import load_dotenv
from discord.ext import commands

from music_cog import music_cog
from eval_cog import eval_cog
from ping_cog import ping_cog
from dm_cog import dm_cog

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
OWNER_ID = int(os.getenv('OWNER_ID'))
intents = discord.Intents.all()
prefix = 'music.'

async def add_cogs(bot: commands.Bot):
    await bot.add_cog(music_cog(bot))
    #await bot.add_cog(eval_cog(bot, owner_id=OWNER_ID))
    #await bot.add_cog(ping_cog(bot))
    #await bot.add_cog(dm_cog(bot, owner_id=OWNER_ID))

bot = commands.Bot(command_prefix=prefix, description='Yet another music bot.', intents=intents)

@bot.event
async def on_ready():
    await add_cogs(bot)
    print('Logged in as:\n{0.user.name}\n{0.user.id}'.format(bot))

bot.run(TOKEN)