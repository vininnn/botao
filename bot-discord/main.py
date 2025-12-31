import discord
from discord.ext import commands
from commands.sessions import register_study_sessions
from commands.task import register_task
from commands.quotes import register_quotes, on_message
import os

from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot('!', intents=intents)

bot.add_listener(on_message)

# Bot initialization
@bot.event
async def on_ready():
    register_study_sessions(bot.tree)
    register_task(bot.tree)
    register_quotes(bot.tree)
    synced = await bot.tree.sync()
    print(f'Synchro: {len(synced)}')
    print('All right!')


bot.run(os.getenv('TOKEN'))