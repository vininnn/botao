import discord
from discord import app_commands

from managers.private_room_manager import PrivateRoomManager
from managers.server_room_manager import ServerRoomManager
from utils.formatter import time_formatter

# Function that register the commands
def register_room_commands(tree: app_commands.CommandTree, privateRoomManager: PrivateRoomManager, serverRoomManager: ServerRoomManager):

    # Father (/room)
    room_group = app_commands.Group(name='room', description='Study rooms manager')
    # SubGroups (/room private, /room server)
    private_group = app_commands.Group(name='private', parent=room_group, description='Private rooms')
    server_group = app_commands.Group(name='server', parent=room_group, description='Shared server rooms')

    # Private Rooms commands
    @private_group.command(name='private_start', description='Start counting your time')
    async def private_start(interaction: discord.Interaction, name: str):
        # Chama o Manager Privado
        if privateRoomManager.open(interaction.user.id, name):
            await interaction.response.send_message(f'Study room "{name}" started! Good studies!')
        else:
            await interaction.response.send_message('You are already in a study room! Quit it before you join another!', ephemeral=True)

    @private_group.command(name='private_stop', description='Stop and save your time')
    async def private_stop(interaction: discord.Interaction):
        # Chama o Manager Privado
        room = privateRoomManager.close(interaction.user.id)
        if room:
            duration = time_formatter(room.duration_seconds)
            await interaction.response.send_message(f'room "{room.name}" finished!\n'
                                                    f'Time studied: {duration}')
        else:
            await interaction.response.send_message('You are not in a study room yet! Join one!', ephemeral=True)

    @private_group.command(name='summary', description='Shows the total hours of each room you studied')
    async def summary(interaction: discord.Interaction):
        await interaction.response.defer()
        history = privateRoomManager.get_closed_rooms(interaction.user.id)
        
        if not history:
            await interaction.followup.send('You have no ended rooms!')
            return

        stats = {}
        for room in history:
            stats[room.name] = stats.get(room.name, 0) + room.duration_seconds

        msg = '** Your study summay:**\n'
        for name, seconds in stats.items():
            msg += f'- **{name}**: {time_formatter(seconds)}\n'
        
        await interaction.followup.send(msg)

    @private_group.command(name="details", description="Shows the total hours studied in a specific room")
    async def details(interaction: discord.Interaction, name: str):
        await interaction.response.defer()
        total_seconds = privateRoomManager.get_total_time(interaction.user.id, name)
        
        if total_seconds == 0:
            await interaction.followup.send(f'There are no close rooms named "{name}"!')
        else:
            await interaction.followup.send(f'Time spent on "{name}": {time_formatter(total_seconds)}')

    # Server Rooms commands


    # Start a study room
    @tree.command(name='startroom', description='Start a study room')
    @app_commands.describe(name='room name')
    async def start_room(interaction: discord.Interaction, name: str):
        await interaction.response.defer()

        user_id = interaction.user.id
        sucess = privateRoomManager.open(user_id, name)

        if not sucess:
            await interaction.followup.send('You are already in a study room! Quit it before you join another!')
            return
        
        await interaction.followup.send(f'Study room "{name}" started! Good studies!')

    # End a study room
    @tree.command(name='endroom', description='End your active study room')
    async def end_room(interaction: discord.Interaction):
        await interaction.response.defer()

        user_id = interaction.user.id
        room = privateRoomManager.close(user_id)

        if not room:
            await interaction.followup.send('You are not in a study room yet! Join one!', ephemeral=True)
            return

        duration = time_formatter(room.duration_seconds)
        
        await interaction.followup.send(f'room "{room.name}" finished!\n'
                                        f'Time studied: {duration}')

    # Show the status of your current study room
    @tree.command(name='roomstatus', description='Show your current room status')
    async def room_status(interaction: discord.Interaction):
        await interaction.response.defer()

        user_id = interaction.user.id
        room = privateRoomManager.get_open_room(user_id)

        if not room:
            await interaction.followup.send('You are not in a study room yet! Join one!', ephemeral=True)
            return

        duration = time_formatter(room.duration_seconds)
        
        await interaction.followup.send(f'Current room: "{room.name}"\n'
                                        f'Time in room: {duration}')

     # Shows the total time per room
    @tree.command(name='studysummary', description='Shows the total hours studied in a room')
    @app_commands.describe(name='Total time on room')
    async def study_summary(interaction: discord.Interaction, name: str):
        await interaction.response.defer()

        user_id = interaction.user.id
        room = privateRoomManager.get_closed_rooms(user_id)

        if not room:
            await interaction.followup.send('You have no ended rooms!')
            return

        total_seconds = privateRoomManager.get_total_time_by_room(user_id, name)

        if total_seconds == 0:
            await interaction.followup.send(f'There are no ended rooms named "{name}"!')
            return

        formatted_time = time_formatter(total_seconds)
        await interaction.followup.send(f'Time spent on "{name}":  {formatted_time}') 

    # Shows everything you studied
    @tree.command(name='studysummary_all', description='Shows the total hours of each room you studied')
    async def study_summary(interaction: discord.Interaction):
        await interaction.response.defer()

        user_id = interaction.user.id
        room = privateRoomManager.get_closed_rooms(user_id)

        if not room:
            await interaction.followup.send('You have no ended rooms!')
            return

        rooms_name = {rooms.name for rooms in room}

        lines = []

        for room_name in rooms_name:
            total_seconds = privateRoomManager.get_total_time_by_room(user_id, room_name)
            lines.append(f'- "{room_name}": {time_formatter(total_seconds)}')

        await interaction.followup.send(f'All subjects studied:\n' + '\n'.join(lines)) 
