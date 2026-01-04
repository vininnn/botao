# Import libs
import discord
from discord.ext import commands
import os

# Import commands
from commands.sessions import register_study_sessions
from commands.shared_sessions import register_shared_sessions
from commands.tasks import register_task
from commands.quotes import register_quotes, on_message

# Import managers
from managers.session_manager import SessionManager
from managers.shared_session_manager import SharedSessionManager

from dotenv import load_dotenv
load_dotenv()

sessionManager = SessionManager()
sharedSessionManager = SharedSessionManager(sessionManager)

sessionManager.set_shared_session_manager(sharedSessionManager)

intents = discord.Intents.all()
bot = commands.Bot('!', intents=intents)

bot.add_listener(on_message)

# Bot initialization
@bot.event
async def on_ready():
    register_study_sessions(bot.tree, sessionManager)
    register_shared_sessions(bot.tree, sharedSessionManager)
    register_task(bot.tree)
    register_quotes(bot.tree)
    synced = await bot.tree.sync()
    print(f'Synchro: {len(synced)}')
    print('All right!')


bot.run(os.getenv('TOKEN'))