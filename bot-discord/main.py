# Import libs
import discord
from discord.ext import commands
import os

# Import commands
from commands.rooms import register_study_rooms
from commands.server_rooms import register_server_rooms
from commands.tasks import register_tasks
from commands.quotes import register_quotes, on_message

# Import managers
from managers.room_manager import RoomManager
from managers.server_room_manager import ServerRoomManager

from dotenv import load_dotenv
load_dotenv()

sessionManager = RoomManager()
sharedSessionManager = ServerRoomManager(sessionManager)

sessionManager.set_server_room_manager(sharedSessionManager)

intents = discord.Intents.all()
bot = commands.Bot('!', intents=intents)

bot.add_listener(on_message)

# Bot initialization
@bot.event
async def on_ready():
    register_study_rooms(bot.tree, sessionManager)
    register_server_rooms(bot.tree, sharedSessionManager, sessionManager)
    register_tasks(bot.tree)
    register_quotes(bot.tree)
    synced = await bot.tree.sync()
    print(f'Synchro: {len(synced)}')
    print('All right!')


bot.run(os.getenv('TOKEN'))