# Import libs
import discord
from discord.ext import commands
import os

# Import commands
from commands.rooms import register_room_commands
from commands.tasks import register_task_commands
from commands.quotes import register_quotes, on_message

# Import managers
from managers.task_manager import TaskManager
from managers.private_room_manager import PrivateRoomManager
from managers.server_room_manager import ServerRoomManager

from dotenv import load_dotenv
load_dotenv()

taskManager = TaskManager()

privateRoomManager = PrivateRoomManager()
serverRoomManager = ServerRoomManager(privateRoomManager)

privateRoomManager.set_server_room_manager(serverRoomManager)

intents = discord.Intents.all()
bot = commands.Bot('!', intents=intents)

bot.add_listener(on_message)

# Bot initialization
@bot.event
async def on_ready():
    register_room_commands(bot.tree, privateRoomManager, serverRoomManager)
    register_task_commands(bot.tree, taskManager)
    register_quotes(bot.tree)
    synced = await bot.tree.sync()
    print(f'Synchro: {len(synced)}')
    print('All right!')


bot.run(os.getenv('TOKEN'))