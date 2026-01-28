# Import libs
import discord
from discord.ext import commands
import os

# Import funcitons
from utils.notification import send_dm_safe
from utils.formatter import format_time

# Import commands
from commands.rooms import register_room_commands
from commands.tasks import register_task_commands
from commands.quotes import register_quote_commands, on_message

# Import embeds
from embeds.room_embed import server_close_embed
from embeds.disconnect_embed import *

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
        bot_user = bot.user

        try:
            # Closing Private Study Room
            if privateRoomManager.is_user_in_private_room(user_id):
                room = privateRoomManager.leave(user_id)
                guild_name = room.guild_name
                room_name = room.name

                duration = format_time(room.duration_seconds)

                embed = private_disconnect_embed(room_name, guild_name, duration, bot_user)

                await send_dm_safe(member, msg=embed)

            # Closing Server Study Room    
            if serverRoomManager.is_user_in_server_room(user_id):
                room = serverRoomManager.get_user_room(user_id)
                guild_name = room.guild_name
                channel_id = room.channel_id
                room_name = room.name

                is_closing = len(room.students) == 1

                history = serverRoomManager.leave(user_id)
                duration = format_time(history.duration_seconds)

                embed = server_disconnect_embed(room_name, guild_name, duration, bot_user)

                await send_dm_safe(member, msg=embed)

                if is_closing:
                    existing_channel = bot.get_channel(channel_id)
                    if existing_channel:
                        embed = server_close_embed(room_name, bot_user)
                        await existing_channel.send(embed=embed)
            
            # Closing Public Study Room
            if publicRoomManager.is_user_in_public_room(user_id):
                room = publicRoomManager.leave(user_id)
                duration = format_time(room.duration_seconds)

                embed = public_disconnect_embed(room.name, duration, bot_user)

                await send_dm_safe(member, msg=embed)

        except Exception:
            pass


bot.run(os.getenv('TOKEN'))