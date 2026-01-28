import discord
from discord import app_commands
from datetime import datetime, timezone

from managers.private_room_manager import PrivateRoomManager
from managers.server_room_manager import ServerRoomManager
from managers.public_room_manager import PublicRoomManager

from utils.formatter import format_time
from utils.validator import validate_student_availability
from embeds.room_embed import *

def register_room_commands(tree: app_commands.CommandTree, privateRoomManager: PrivateRoomManager, serverRoomManager: ServerRoomManager, publicRoomManager: PublicRoomManager):
    """Registers '/room private' and '/room server' commands to Discord."""

    # Father Group (/room)
    room_group = app_commands.Group(name='room', description='Study rooms manager')
    
    # SubGroups (/room private, /room server)
    private_group = app_commands.Group(name='private', parent=room_group, description='Manage Private Study Rooms')
    server_group = app_commands.Group(name='server', parent=room_group, description='Manage Server Study Rooms')
    public_group = app_commands.Group(name='public', parent=room_group, description='Manage Public Study Rooms')

    # --- COMMON GROUP COMMANDS ---

    # Summary (/room summary)
    @room_group.command(name='summary', description='Shows the total hours of each Study Room you studied')
    async def room_summary(interaction: discord.Interaction):
        """Aggregates all study rooms and displays a summary per subject."""
        user = interaction.user
        user_id = user.id

        try:
            history = privateRoomManager.get_left_rooms(user_id)
            rooms = {}
            for room in history:
                rooms[room.name] = rooms.get(room.name, 0) + room.duration_seconds

            embed = room_summary_embed(rooms, user)
            
            await interaction.response.send_message(embed=embed)

        except ValueError as e:   
            await interaction.response.send_message(f'{str(e)}', ephemeral=True)

    # Details (/room details)
    @room_group.command(name='details', description='Shows the total hours studied in a specific Study Room')
    @app_commands.describe(name='Room name')
    async def room_details(interaction: discord.Interaction, name: str):
        """Retrieves historical study data for a specific room name."""
        user = interaction.user
        total_seconds = privateRoomManager.get_total_time_by_room(interaction.user.id, name)
        
        if total_seconds == 0:
            await interaction.response.send_message(f'No history found for room **{name}**.', ephemeral=True)
        else:
            embed = room_details_embed(name, user, format_time(total_seconds))
            await interaction.response.send_message(embed=embed)

    # Leave (/room leave)
    @room_group.command(name='leave', description='Leave your current Study Room and save your time')
    async def room_leave(interaction: discord.Interaction):
        """Leaves the user's active Study Room and saves it to history."""
        user = interaction.user
        user_id = user.id
        bot = interaction.client.user
        
        # Try leave Private Study Room
        try:
            room = privateRoomManager.leave(user_id)
            duration = format_time(room.duration_seconds)

            embed = private_leave_embed(room.name, user, duration)
            return await interaction.response.send_message(embed=embed)

        except ValueError:
            pass      

        # Try leave Server Study Room
        try:
            room = serverRoomManager.get_user_room(user_id)
            room_name = room.name

            is_closing = len(room.students) == 1
            students_ids = [uid for uid in room.students.keys() if uid != user_id]

            history = serverRoomManager.leave(user_id)
            duration = format_time(history.duration_seconds)

            embed = server_leave_embed(room_name, user, duration, students_ids)

            if is_closing:
                embed_close = server_close_embed(room_name, bot)
                return await interaction.response.send_message(embeds=[embed, embed_close])
            else:
                return await interaction.response.send_message(embed=embed)

        except ValueError:
            pass

        # Try leave Public Study Room
        try:
            history = publicRoomManager.leave(user_id)
            duration = format_time(history.duration_seconds)
            return await interaction.response.send_message(f'You left **{history.name}**.\nTime studied: **{duration}**')

        except ValueError as e:
            await interaction.response.send_message(f'You are not in any Study Room!', ephemeral=True)

    # Status (/room status)
    @room_group.command(name='status', description='Show the time of your current Study Room')
    async def room_status(interaction: discord.Interaction):
        """Calculates and displays the current Study Room duration."""
        user = interaction.user
        user_id = user.id

        # Try status Private Study Room
        try:
            room = privateRoomManager.get_open_room(user_id)
            duration = format_time(room.duration_seconds)

            embed = private_status_embed(room.name, user, duration)
            return await interaction.response.send_message(embed=embed)
        
        except ValueError:    
            pass

        # Try status Private Study Room
        try:
            room = serverRoomManager.get_user_room(user_id)    
            student = room.students.get(user_id)
            # Recalculate duration manually since RoomStudent is not a BaseRoom
            seconds = int((datetime.now(timezone.utc) - student.join_time).total_seconds())
            duration = format_time(seconds)
                
            embed = server_status_embed(room.name, user, duration, room.students)
            return await interaction.response.send_message(embed=embed)

        except ValueError:
            pass

        # Try status Private Study Room
        try:
            room = publicRoomManager.get_user_room(user_id)    
            student = room.students.get(user_id)
            # Recalculate duration manually since RoomStudent is not a BaseRoom
            seconds = int((datetime.now(timezone.utc) - student.join_time).total_seconds())
            duration = format_time(seconds)
                
            return await interaction.response.send_message(
                f'**Current Room:** `{room.name}`\n'
                f'**Your Time:** `{duration}`\n'
                f'**Total Students:** `{len(room.students)}`'
            )

        except ValueError:
            await interaction.response.send_message(f'You are not in any Study Room', ephemeral=True)    

    # --- PRIVATE GROUP COMMANDS ---

    # Open (/room private open)
    @private_group.command(name='open', description='Open a Private Study Room')
    @app_commands.describe(name='Room name')
    async def private_room_open(interaction: discord.Interaction, name: str):
        """Calculates and displays the current room duration."""
        user = interaction.user
        user_id = user.id
        guild_name = interaction.guild.name

        try:
            validate_student_availability(interaction, privateRoomManager, serverRoomManager, publicRoomManager)
            privateRoomManager.open(user_id, guild_name, name)

            embed = private_open_embed(name, user)
            await interaction.response.send_message(embed=embed)

        except ValueError as e:
            await interaction.response.send_message(f'{str(e)}', ephemeral=True)

    # --- SERVER GROUP COMMANDS ---

    # Open (/room server open)
    @server_group.command(name='open', description='Open a Server Study Room')
    @app_commands.describe(name='Room name')
    async def server_room_open(interaction: discord.Interaction, name: str):
        """Opens a Server Study Room after verifying the user is not in a room."""
        user = interaction.user
        user_id = user.id
        guild_id = interaction.guild.id
        guild_name = interaction.guild.name
        channel_id = interaction.channel.id

        try:
            validate_student_availability(interaction, privateRoomManager, serverRoomManager, publicRoomManager)

            serverRoomManager.open(guild_id, guild_name, name, channel_id)
            serverRoomManager.join(guild_id, name, user_id)

            embed = server_open_embed(name, user)
            await interaction.response.send_message(embed=embed)
            
        except ValueError as e:
            await interaction.response.send_message(f'{str(e)}', ephemeral=True)

    # Join (/room server join)
    @server_group.command(name='join', description='Join an existing Server Study Room')
    @app_commands.describe(name='Room name')
    async def server_room_join(interaction: discord.Interaction, name: str):
        """Joins a Server Study Room after verifying the user has no active room."""
        user = interaction.user
        user_id = user.id
        guild_id = interaction.guild_id

        try:
            validate_student_availability(interaction, privateRoomManager, serverRoomManager, publicRoomManager)

            serverRoomManager.join(guild_id, name, user_id)
            room = serverRoomManager.get_room(guild_id, name)
            students_ids = list(room.students.keys())

            embed = server_join_embed(name, user, students_ids)
            await interaction.response.send_message(embed=embed)

        except ValueError as e:
            await interaction.response.send_message(f'{str(e)}', ephemeral=True)

    # List (/room server list)
    @server_group.command(name='list', description='List all active server rooms in this server')
    async def server_room_list(interaction: discord.Interaction):
        """Generates the list of rooms and active students."""
        server = interaction.guild
        user = interaction.user

        try:
            rooms = serverRoomManager.list_rooms(server.id)
            embed = server_list_embed(rooms, user, server.name)
            await interaction.response.send_message(embed=embed)

        except ValueError as e:
            await interaction.response.send_message(f'{str(e)}', ephemeral=True)

    # --- PUBLIC GROUP COMMANDS ---

    # Join (/room server join)
    @public_group.command(name='join', description='Join an existing Public Study Room')
    @app_commands.describe(name='Select your room')
    @app_commands.choices(name=[
        app_commands.Choice(name='Computing', value='Computing'),
        app_commands.Choice(name='Creative Arts', value='Creative Arts'),
        app_commands.Choice(name='Exact Sciences', value='Exact Sciences'),
        app_commands.Choice(name='Humanities', value='Humanities'),
        app_commands.Choice(name='Writing', value='Writing'),
    ])
    async def public_room_join(interaction: discord.Interaction, name: app_commands.Choice[str]):
        """Joins a Public Study Room after verifying the user has no active room."""
        user_id = interaction.user.id

        try:
            validate_student_availability(interaction, privateRoomManager, serverRoomManager, publicRoomManager)
            publicRoomManager.join(name.value, user_id)

            await interaction.response.send_message(f'You joined the Puclic Study Room **{name.value}**!')

        except ValueError as e:
            await interaction.response.send_message(f'{str(e)}', ephemeral=True)

    # List (/room public list)
    @public_group.command(name='list', description='List all active public rooms')
    async def public_room_list(interaction: discord.Interaction):
        """Generates the list of rooms and active students."""

        rooms = publicRoomManager.list_rooms()
        embed = discord.Embed(title='Public Rooms',
                               color=discord.Color.purple())
        for room in rooms:
            all_students = list(room.students.keys())
            student_count = len(all_students)

            local_students = []
            #limit = 10

            for uid in all_students:
                member = interaction.guild.get_member(uid)
                if member:
                    local_students.append(member.mention)

            #if len(local_students) >= limit:
            #   break

            if local_students:
                names = ', '.join(local_students)
                if student_count > len(local_students):
                    extra = student_count - len(local_students)
                    value_text = f'{names} +{extra} others globally'
                else:
                    value_text = f'{names}'
            else:
                value_text = f'**{student_count}** students active'
            
            embed.add_field(
                name=f'{room.name}', 
                value=value_text, 
                inline=False
            )
        
        await interaction.response.send_message(embed=embed)


    tree.add_command(room_group)
