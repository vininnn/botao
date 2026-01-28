import discord
from embeds.factory import EmbedFactory
from utils.constants import PanelsText, Emojis
import time

from utils.formatter import format_time

ROOMS = PanelsText.ROOMS

BOOKMARK = Emojis.BOOKMARK
CLOSE_DOOR = Emojis.CLOSE_DOOR
DOCUMENT = Emojis.DOCUMENT
EARTH = Emojis.EARTH
FILTER = Emojis.FILTER
FUNCTION = Emojis.FUNCTION
JOIN = Emojis.JOIN
LEAVE = Emojis.LEAVE
LIST = Emojis.LIST
NO_USER = Emojis.NO_USER
OPEN_DOOR = Emojis.OPEN_DOOR
PALETTE = Emojis.PALETTE
SEARCH = Emojis.SEARCH
TERMINAL = Emojis.TERMINAL
TEXT = Emojis.TEXT
TIME = Emojis.TIME
USER = Emojis.USER
USERS = Emojis.USERS

    # --- COMMON ROOM EMBEDS ---

def room_summary_embed(rooms: dict[str, int], user: discord.User) -> discord.Embed:
    embed = EmbedFactory.base_embed(
        user=user,
        author_text=ROOMS,
        title=f'{BOOKMARK} Your study summary',
    )
    
    for room, duration in rooms.items():
        string_time = format_time(duration)

        embed.add_field(
            name=f'{room}',
            value=f'`{string_time}`',
            inline=True
        )

    return embed

def room_details_embed(room: str, user: discord.User, duration: str) -> discord.Embed:
    embed = EmbedFactory.base_embed(
        user=user,
        author_text=ROOMS,
        title=f'{SEARCH} Details of - {room}',
    )

    embed.add_field(name=f'Room', value=f'`{room}`', inline=True)
    embed.add_field(name=f'Total time', value=f'`{duration}`', inline=True)

    return embed

    # --- PRIVATE ROOM EMBEDS ---

def private_open_embed(room: str, user: discord.User) -> discord.Embed:
    embed = EmbedFactory.base_embed(
        user=user,
        author_text=ROOMS,
        title=f'{OPEN_DOOR} Room opened - **{room}**',
        description=f'Private room **{room}** was open! Good studies <@{user.id}>!'
    )

    embed.add_field(name=f'{USER} Student', value=f'<@{user.id}>', inline=True)
    embed.add_field(name=f'{FILTER} Type', value=f'`Private`', inline=True)
    embed.add_field(name=f'{TIME} Opened', value=f'<t:{int(time.time())}:R>', inline=True)

    embed.set_image(url='https://mir-s3-cdn-cf.behance.net/project_modules/1400/58a87a182606383.6530875274ecf.gif')

    return embed

def private_leave_embed(room: str, user: discord.User, duration: str) -> discord.Embed:
    embed = EmbedFactory.base_embed(
        user=user,
        author_text=ROOMS,
        title=f'{CLOSE_DOOR} Room closed - **{room}**',
        description=f'Private room **{room}** closed.'
    )

    embed.add_field(name=f'{USER} Student', value=f'<@{user.id}>', inline=True)
    embed.add_field(name=f'{FILTER} Type', value=f'`Private`', inline=True)
    embed.add_field(name=f'{TIME} Total time', value=f'`{duration}`', inline=True)

    return embed

def private_status_embed(room: str, user: discord.User, duration: str) -> discord.Embed:
    embed = EmbedFactory.base_embed(
        user=user,
        author_text=ROOMS,
        title=f'{CLOSE_DOOR} Status of - {room}',
        description=f'Current status of Private room **{room}**!'
    )

    embed.add_field(name=f'{USER} Student', value=f'<@{user.id}>', inline=True)
    embed.add_field(name=f'{FILTER} Type', value=f'`Private`', inline=True)
    embed.add_field(name=f'{TIME} Total time', value=f'`{duration}`', inline=True)

    return embed

    # --- SERVER ROOM EMBEDS ---

def server_open_embed(room: str, user: discord.User) -> discord.Embed:
    embed = EmbedFactory.base_embed(
        user=user,
        author_text=ROOMS,
        title=f'{OPEN_DOOR} Room opened - **{room}**',
        description=f'Server room **{room}** was open by <@{user.id}>! Invite your friends too!'
    )

    embed.add_field(name=f'{USER} Students', value=f'<@{user.id}>', inline=True)
    embed.add_field(name=f'{FILTER} Type', value=f'`Server`', inline=True)
    embed.add_field(name=f'{TIME} Opened', value=f'<t:{int(time.time())}:R>', inline=True)

    embed.set_image(url='https://mir-s3-cdn-cf.behance.net/project_modules/1400/58a87a182606383.6530875274ecf.gif')

    return embed

def server_join_embed(room: str, user: discord.User, students_list: list) -> discord.Embed:
    embed = EmbedFactory.base_embed(
        user=user,
        author_text=ROOMS,
        title=f'{JOIN} Room joined - **{room}**',
        description=f'<@{user.id}> Joined the Server room **{room}**!'
    )

    students = ', '.join([f'<@{uid}>' for uid in students_list])

    embed.add_field(name=f'{USERS} Students', value=f'{students}', inline=True)
    embed.add_field(name=f'{FILTER} Type', value=f'`Server`', inline=True)
    embed.add_field(name=f'{TIME} Joined', value=f'<t:{int(time.time())}:R>', inline=True)

    embed.set_image(url='https://mir-s3-cdn-cf.behance.net/project_modules/1400/58a87a182606383.6530875274ecf.gif')

    return embed

def server_leave_embed(room: str, user: discord.User, duration: str, students_list: list) -> discord.Embed:
    embed = EmbedFactory.base_embed(
        user=user,
        author_text=ROOMS,
        title=f'{LEAVE} Room left - **{room}**',
        description=f'Server room **{room}** left.'
    )

    students = ', '.join([f'<@{uid}>' for uid in students_list])

    if len(students_list) == 0:
        user_emoji = NO_USER
    elif len(students_list) == 1:
        user_emoji = USER
    else:
        user_emoji = USERS

    embed.add_field(name=f'{user_emoji} Remaining Students', value=f'{students if len(students) > 1 else '`Empty Room`'}', inline=True)
    embed.add_field(name=f'{FILTER} Type', value=f'`Server`', inline=True)
    embed.add_field(name=f'{TIME} Total time', value=f'`{duration}`', inline=True)

    return embed

def server_close_embed(room: str, user: discord.ClientUser) -> discord.Embed:
    embed = EmbedFactory.base_embed(
        user=user,
        author_text=ROOMS,
        title=f'{CLOSE_DOOR} Room closed - **{room}**',
        description=f'Since there are no more students on Server room **{room}**, the room has been closed.'
    )

    embed.add_field(name=f'{NO_USER} Remaining Students', value='`Empty Room`', inline=True)
    embed.add_field(name=f'{FILTER} Type', value=f'`Server`', inline=True)

    return embed

def server_status_embed(room: str, user: discord.User, duration: str, students: dict) -> discord.Embed:
    embed = EmbedFactory.base_embed(
        user=user,
        author_text=ROOMS,
        title=f'{CLOSE_DOOR} Status of - {room}',
        description=f'Current status of Server room **{room}**!'
    )

    students_text = f'<@{user.id}>'
    total_students = 0
    if len(students) > 1:
        total_students = len(students) - 1
        students_text = f'<@{user.id}> +{total_students}'        

    embed.add_field(name=f'{USER if not total_students else USERS} Students', value=students_text, inline=True)
    embed.add_field(name=f'{FILTER} Type', value=f'`Server`', inline=True)
    embed.add_field(name=f'{TIME} Total time', value=f'`{duration}`', inline=True)

    return embed

def server_list_embed(rooms: list, user: discord.User) -> discord.Embed:
    embed = EmbedFactory.base_embed(
        user=user,
        author_text=ROOMS,
        title=f'{LIST} List of opens Server room',
        description='\u200b'
    )

    for room in rooms:

        student_names = ', '.join([f'<@{uid}>' for uid in room.students.keys()]) 
        
        embed.add_field(
            name=f'{room.name}', 
            value=f'{student_names}', 
            inline=True
        )        

    return embed

    # --- PUBLIC ROOM EMBEDS ---

def public_join_embed(room: str, user: discord.User, total_students: int) -> discord.Embed:
    embed = EmbedFactory.base_embed(
        user=user,
        author_text=ROOMS,
        title=f'{JOIN} Room joined - **{room}**',
        description=f'<@{user.id}> Joined the Public room **{room}**!'
    )

    students_text = f'<@{user.id}>'
    if total_students > 1:
        total_students = total_students - 1
        students_text = f'<@{user.id}> +{total_students}' 
    

    embed.add_field(name=f'{USERS} Students', value=f'{students_text}', inline=True)
    embed.add_field(name=f'{FILTER} Type', value=f'`Public`', inline=True)
    embed.add_field(name=f'{TIME} Joined', value=f'<t:{int(time.time())}:R>', inline=True)

    embed.set_image(url='https://mir-s3-cdn-cf.behance.net/project_modules/1400/58a87a182606383.6530875274ecf.gif')

    return embed

def public_status_embed(room: str, user: discord.User, duration: str, students: dict) -> discord.Embed:
    embed = EmbedFactory.base_embed(
        user=user,
        author_text=ROOMS,
        title=f'{CLOSE_DOOR} Status of - {room}',
        description=f'Current status of Public room **{room}**!'
    )

    students_text = f'<@{user.id}>'
    total_students = 0
    if len(students) > 1:
        total_students = len(students) - 1
        students_text = f'<@{user.id}> +{total_students}'        

    embed.add_field(name=f'{USER if not total_students else USERS} Students', value=students_text, inline=True)
    embed.add_field(name=f'{FILTER} Type', value=f'`Public`', inline=True)
    embed.add_field(name=f'{TIME} Total time', value=f'`{duration}`', inline=True)

    return embed

def public_list_embed(rooms: list, user: discord.User, server: discord.Guild) -> discord.Embed:
    embed = EmbedFactory.base_embed(
        user=user,
        author_text=ROOMS,
        title=f'{LIST} List of opens Public room',
        description='\u200b'
    )

    emojis_list = [TERMINAL, PALETTE, FUNCTION, EARTH, DOCUMENT]

    for room, emoji in zip(rooms, emojis_list):
        all_students = list(room.students.keys())
        student_count = len(all_students)

        local_students = []
        #limit = 10

        for uid in all_students:
            member = server.get_member(uid)
            if member:
                local_students.append(member.mention)

        #if len(local_students) >= limit:
        #   break

        if local_students:
            names = ''.join(local_students)
            if student_count > len(local_students):
                extra = student_count - len(local_students)
                value_text = f'{names} +{extra} others globally'
            else:
                value_text = f'{names}'
        else:
            value_text = f'**{student_count}** students active'
        
        embed.add_field(name=f'{emoji} {room.name}', value=value_text, inline=False)

    return embed
