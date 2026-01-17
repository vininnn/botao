import discord
from discord import app_commands

from managers.server_room_manager import ServerRoomManager
from managers.room_manager import RoomManager
from utils.formatter import time_formatter

# Function that register the commands
def register_server_rooms(tree: app_commands.CommandTree, serverRoomManager: ServerRoomManager, roomManager: RoomManager):

    # Start a shared study room
    @tree.command(name='startshared', description='Start a shared study room')
    @app_commands.describe(name='room name')
    async def start_shared(interaction: discord.Interaction, name: str):
        await interaction.response.defer()

        guild_id = interaction.guild.id
        user_id = interaction.user.id

        if roomManager.has_open_room(user_id) or serverRoomManager.is_user_in_server_room(user_id):
            await interaction.followup.send("You already are in a room! Quit it before create it!")
            return

        try:
            serverRoomManager.start(guild_id, name)
            serverRoomManager.join(guild_id, name, user_id)
            await interaction.followup.send(f'Shared room "{name}" created sucessfully')
        except ValueError as e:
            await interaction.followup.send(str(e))
            
    # Join an existing shared study room
    @tree.command(name='joinshared', description='Join a shared study room')
    @app_commands.describe(name='room name')
    async def join_shared(interaction: discord.Interaction, name: str):
        await interaction.response.defer()

        guild_id = interaction.guild.id
        user_id = interaction.user.id

        try:
            serverRoomManager.join(guild_id, name, user_id)
            await interaction.followup.send(f'You joined the shared room "{name}"!')
        except ValueError as e:
            await interaction.followup.send(str(e))

    # Leave your current shared study room
    @tree.command(name='leaveshared', description='Leave your shared study room')
    async def leave_shared(interaction: discord.Interaction):
        await interaction.response.defer()

        user_id = interaction.user.id

        try:
            room = serverRoomManager.leave(user_id)
            formatted_time = time_formatter(room.duration_seconds)

            await interaction.followup.send(f'You leave the shared room "{room.name}".\n'
                f'Time studied: {formatted_time}')
        except ValueError as e:
            await interaction.followup.send(str(e))

    # List all current shared study rooms in the server
    @tree.command(name='listshared', description='List all shared study room in this server')
    async def list_shared(interaction: discord.Interaction):
        await interaction.response.defer()

        guild_id = interaction.guild.id
        rooms = serverRoomManager.list_rooms(guild_id)

        if not rooms:
            await interaction.followup.send(f'There are no shared rooms in this server!')
            return
        
        msg = 'Shared rooms:\n'

        for room in rooms:
            partipants_count = len(room.students)
            msg += f'- "{room.name}" "({partipants_count} participants)"'

        await interaction.followup.send(msg)
