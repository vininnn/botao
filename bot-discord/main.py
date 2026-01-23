# Import libs
import discord
from discord.ext import commands
import os

# Import funcitons
from utils.notification import send_dm_safe

# Import commands
from commands.rooms import register_room_commands
from commands.tasks import register_task_commands
from commands.quotes import register_quote_commands, on_message

# Import managers
from managers.task_manager import TaskManager
from managers.private_room_manager import PrivateRoomManager
from managers.server_room_manager import ServerRoomManager
from managers.public_room_manager import PublicRoomManager

from dotenv import load_dotenv
load_dotenv()

taskManager = TaskManager()

privateRoomManager = PrivateRoomManager()
serverRoomManager = ServerRoomManager(privateRoomManager)
publicRoomManager = PublicRoomManager(privateRoomManager, serverRoomManager)

intents = discord.Intents.all()
bot = commands.Bot('!', intents=intents)

bot.add_listener(on_message)

# Bot initialization
@bot.event
async def on_ready():
    register_room_commands(bot.tree, privateRoomManager, serverRoomManager, publicRoomManager)
    register_task_commands(bot.tree, taskManager)
    register_quote_commands(bot.tree)
    synced = await bot.tree.sync()
    print(f'Synchro: {len(synced)}')
    print('All right!')

@bot.event
async def on_voice_state_update(member, before, after):
    """ Detects if the student has completely disconnected.
        If they only changed channels the code will not run.
    """
    if before.channel is not None and after.channel is None:
        user_id = member.id

        # Closing Private Study Room
        try:
            if privateRoomManager.is_user_in_private_room(user_id):
                room = privateRoomManager.close(user_id)
                await send_dm_safe(member, f'**[AUTO-CLOSE]** | Private Study Room `{room.name}` of `{member.name}` was closed due to a disconnection with the voice channel.')
            
            if serverRoomManager.is_user_in_server_room(user_id):
                room = serverRoomManager.leave(user_id)
                await send_dm_safe(member, f'**[AUTO-LEAVE]** | Server Study Room `{room.name}` of `{member.name}` was left due to a disconnection with the voice channel.')
            
            if publicRoomManager.is_user_in_public_room(user_id):
                room = publicRoomManager.leave(user_id)
                await send_dm_safe(member, f'**[AUTO-LEAVE]** | Public Study Room `{room.name}` of `{member.name}` was left due to a disconnection with the voice channel.')

        except Exception:
            pass


bot.run(os.getenv('TOKEN'))