import discord
from discord import app_commands
from datetime import datetime, timezone

from managers.room_manager import RoomManager
from utils.formatter import time_formatter

# Function that register the commands
def register_study_rooms(tree: app_commands.CommandTree, roomManager: RoomManager):

    # Start a study room
    @tree.command(name='startroom', description='Start a study room')
    @app_commands.describe(name='room name')
    async def start_room(interaction: discord.Interaction, name: str):
        await interaction.response.defer()

        user_id = interaction.user.id
        sucess = roomManager.start(user_id, name)

        if not sucess:
            await interaction.followup.send('You are already in a study room! Quit it before you join another!')
            return
        
        await interaction.followup.send(f'Study room "{name}" started! Good studies!')

    # End a study room
    @tree.command(name='endroom', description='End your active study room')
    async def end_room(interaction: discord.Interaction):
        await interaction.response.defer()

        user_id = interaction.user.id
        room = roomManager.close(user_id)

        if not room:
            await interaction.followup.send('You are not in a study room yet! Join one!', ephemeral=True)
            return

        duration = time_formatter(room.duration_seconds)
        
        await interaction.followup.send(f'room "{room.room_name}" finished!\n'
                                        f'Time studied: {duration}')

    # Show the status of your current study room
    @tree.command(name='roomstatus', description='Show your current room status')
    async def room_status(interaction: discord.Interaction):
        await interaction.response.defer()

        user_id = interaction.user.id
        room = roomManager.get_active_room(user_id)

        if not room:
            await interaction.followup.send('You are not in a study room yet! Join one!', ephemeral=True)
            return

        duration = time_formatter(room.duration_seconds)
        
        await interaction.followup.send(f'Current room: "{room.room_name}"\n'
                                        f'Time in room: {duration}')

     # Shows the total time per room
    @tree.command(name='studysummary', description='Shows the total hours studied in a room')
    @app_commands.describe(name='Total time on room')
    async def study_summary(interaction: discord.Interaction, name: str):
        await interaction.response.defer()

        user_id = interaction.user.id
        room = roomManager.get_closed_rooms(user_id)

        if not room:
            await interaction.followup.send('You have no ended rooms!')
            return

        total_seconds = roomManager.get_total_time_by_room(user_id, name)

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
        room = roomManager.get_closed_rooms(user_id)

        if not room:
            await interaction.followup.send('You have no ended rooms!')
            return

        rooms_name = {rooms.room_name for rooms in room}

        lines = []

        for room_name in rooms_name:
            total_seconds = roomManager.get_total_time_by_room(user_id, room_name)
            lines.append(f'- "{room_name}": {time_formatter(total_seconds)}')

        await interaction.followup.send(f'All subjects studied:\n' + '\n'.join(lines)) 
