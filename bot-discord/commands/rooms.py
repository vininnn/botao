import discord
from discord import app_commands
from datetime import datetime, timezone

from managers.private_room_manager import PrivateRoomManager
from managers.server_room_manager import ServerRoomManager
from utils.formatter import time_formatter

def register_room_commands(tree: app_commands.CommandTree, privateRoomManager: PrivateRoomManager, serverRoomManager: ServerRoomManager):
    """Registers '/room private' and '/room server' commands to Discord."""

    # Father Group (/room)
    room_group = app_commands.Group(name='room', description='Study rooms manager')
    
    # SubGroups (/room private, /room server)
    private_group = app_commands.Group(name='private', parent=room_group, description='Manage Private Study Rooms')
    server_group = app_commands.Group(name='server', parent=room_group, description='Manage Server Study Rooms')

    # --- COMMON GROUP COMMANDS ---

    # Summary (/room summary)
    @room_group.command(name='summary', description='Shows the total hours of each room you studied')
    async def room_summary(interaction: discord.Interaction):
        """Aggregates all study rooms and displays a summary per subject."""
        await interaction.response.defer()
        try:
            history = privateRoomManager.get_closed_rooms(interaction.user.id)
            stats = {}
            for room in history:
                stats[room.name] = stats.get(room.name, 0) + room.duration_seconds

            msg = '**Your Study Summary:**\n'
            for name, seconds in stats.items():
                msg += f'- **{name}**: **{time_formatter(seconds)}**\n'
            
            await interaction.followup.send(msg)

        except ValueError as e:   
            await interaction.followup.send(f'{str(e)}', ephemeral=True)

    # Details (/room details)
    @room_group.command(name='details', description='Shows the total hours studied in a specific room')
    @app_commands.describe(name='room name')
    async def private_room_details(interaction: discord.Interaction, name: str):
        """Retrieves historical study data for a specific room name."""
        await interaction.response.defer()
        total_seconds = privateRoomManager.get_total_time_by_room(interaction.user.id, name)
        
        if total_seconds == 0:
            await interaction.followup.send(f'No history found for room **{name}**.', ephemeral=True)
        else:
            await interaction.followup.send(f'Time spent on **{name}**: **{time_formatter(total_seconds)}**')

    # --- PRIVATE GROUP COMMANDS ---

    # Open (/room private open)
    @private_group.command(name='open', description='Open a Private Study Room')
    @app_commands.describe(name='room name')
    async def private_room_open(interaction: discord.Interaction, name: str):
        """Calculates and displays the current room duration."""
        await interaction.response.defer()
        user_id = interaction.user.id
        try:
            if serverRoomManager.is_user_in_server_room(user_id):
                raise ValueError('You are currently in a Server Room! Leave it first.')

            privateRoomManager.open(user_id, name)
            await interaction.followup.send(f'Private Room **{name}** started! Good studies!')

        except ValueError as e:
            await interaction.followup.send(f'{str(e)}', ephemeral=True)

    # Close (/room private close)
    @private_group.command(name='close', description='Close your current Private Study Room and save your time')
    async def private_room_close(interaction: discord.Interaction):
        """Closes the user's active Private Study Room and saves it to history."""
        await interaction.response.defer()
        try:
            room = privateRoomManager.close(interaction.user.id)
            duration = time_formatter(room.duration_seconds)
            await interaction.followup.send(f'Private Room **{room.name}** finished!\nTime studied: **{duration}**')

        except ValueError as e:
            await interaction.followup.send(f'{str(e)}', ephemeral=True)

    # Status (/room private status)
    @private_group.command(name='status', description='Show the time of your current Private Study Room')
    async def private_room_status(interaction: discord.Interaction):
        """Opens a Private Study Room after verifying the user is not in a room."""
        await interaction.response.defer()
        try:
            room = privateRoomManager.get_open_room(interaction.user.id)
            duration = time_formatter(room.duration_seconds)
            await interaction.followup.send(f'**Private Room:** "{room.name}"\n**Study time:** "{duration}"')
        
        except ValueError as e:    
            await interaction.followup.send(f'{str(e)}', ephemeral=True)

    # --- SERVER GROUP COMMANDS ---

    # Open (/room server open)
    @server_group.command(name='open', description='Open a Server Study Room')
    @app_commands.describe(name='room name')
    async def server_room_open(interaction: discord.Interaction, name: str):
        """Opens a Server Study Room after verifying the user is not in a room."""
        await interaction.response.defer()
        try:
            serverRoomManager.open(interaction.guild_id, name)
            serverRoomManager.join(interaction.guild_id, name, interaction.user.id)
            await interaction.followup.send(f'Server room **{name}** opened!')

        except ValueError as e:
            await interaction.followup.send(f'{str(e)}', ephemeral=True)

    # Join (/room server join)
    @server_group.command(name='join', description='Join an existing Server Study Room')
    @app_commands.describe(name='room name')
    async def server_room_join(interaction: discord.Interaction, name: str):
        """Joins a Server Study Room after verifying the user has no active room."""
        await interaction.response.defer()
        user_id = interaction.user.id
        try:
            if privateRoomManager.has_open_room(user_id):
                raise ValueError('You are currently in a Private Study Room! Close it first.')

            serverRoomManager.join(interaction.guild_id, name, user_id)
            await interaction.followup.send(f'You joined the room **{name}**!')

        except ValueError as e:
            await interaction.followup.send(f'{str(e)}', ephemeral=True)

    # Leave (/room server leave)
    @server_group.command(name='leave', description='Leave your current Server Study Room')
    async def server_room_leave(interaction: discord.Interaction):
        """Leave the user's active Server Study Room and saves the room to history."""
        await interaction.response.defer()
        try:
            history = serverRoomManager.leave(interaction.user.id)
            duration = time_formatter(history.duration_seconds)
            await interaction.followup.send(f'You left **{history.name}**.\nTime studied: **{duration}**')

        except ValueError as e:
            await interaction.followup.send(f'{str(e)}', ephemeral=True)

    # Status (/room server status)
    @server_group.command(name='status', description='Show your current status in a Server Study Room')
    async def server_room_status(interaction: discord.Interaction):
        """Calculates and displays the current room duration."""
        await interaction.response.defer()
        try:
            user_id = interaction.user.id
            room = serverRoomManager.get_user_room(user_id)    
            student = room.students.get(user_id)
            # Recalculate duration manually since RoomStudent is not a BaseRoom
            seconds = int((datetime.now(timezone.utc) - student.join_time).total_seconds())
            duration = time_formatter(seconds)
                
            await interaction.followup.send(
                f'**Current Room:** `{room.name}`\n'
                f'**Your Time:** `{duration}`\n'
                f'**Total Students:** `{len(room.students)}`'
            )

        except ValueError as e:
            await interaction.followup.send(f'{str(e)}', ephemeral=True)

    # List (/room server list)
    @server_group.command(name='list', description='List all active shared rooms in this server')
    async def server_room_list(interaction: discord.Interaction):
        """Generates the list of rooms and active students."""
        await interaction.response.defer()
        try:
            rooms = serverRoomManager.list_rooms(interaction.guild_id)
            embed = discord.Embed(title='Active Server Rooms', color=discord.Color.blue())
            for r in rooms:
                student_count = len(r.students)

                student_names = ', '.join([f'<@{uid}>' for uid in r.students.keys()]) 
                
                embed.add_field(
                    name=f'{r.name}', 
                    value=f'**{student_count}** students\n {student_names if student_count > 0 else 'Empty'}', 
                    inline=False
                )
            
            await interaction.followup.send(embed=embed)

        except ValueError as e:
            await interaction.followup.send(f'{str(e)}', ephemeral=True)

    tree.add_command(room_group)
