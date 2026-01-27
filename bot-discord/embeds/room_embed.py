import discord
from embeds.factory import EmbedFactory
from utils.constants import PanelsText, Emojis
import time

from utils.formatter import format_time

ROOMS = PanelsText.ROOMS

BOOKMARK = Emojis.BOOKMARK
CLOSE_DOOR = Emojis.CLOSE_DOOR
FILTER = Emojis.FILTER
JOIN = Emojis.JOIN
LEAVE = Emojis.LEAVE
LIST = Emojis.LIST
NO_USER = Emojis.NO_USER
OPEN_DOOR = Emojis.OPEN_DOOR
SEARCH = Emojis.SEARCH
TIME = Emojis.TIME
TEXT = Emojis.TEXT
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
    embed.add_field(name=f'{TIME} Open', value=f'<t:{int(time.time())}:R>', inline=True)

    embed.set_image(url='https://mir-s3-cdn-cf.behance.net/project_modules/1400/58a87a182606383.6530875274ecf.gif')

    return embed

def private_close_embed(room: str, user: discord.User, duration: str) -> discord.Embed:
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
        description=f'Current status of Private Study Room **{room}**!'
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
    embed.add_field(name=f'{TIME} Open', value=f'<t:{int(time.time())}:R>', inline=True)

    embed.set_image(url='https://mir-s3-cdn-cf.behance.net/project_modules/1400/58a87a182606383.6530875274ecf.gif')

    return embed

def server_join_embed(room: str, user: discord.User, students_list: list) -> discord.Embed:
    embed = EmbedFactory.base_embed(
        user=user,
        author_text=ROOMS,
        title=f'{JOIN} Room joined - **{room}**',
        description=f'<@{user.id}> Joined the server room **{room}**!'
    )

    students = ', '.join([f'<@{uid}>' for uid in students_list])

    embed.add_field(name=f'{USERS} Students', value=f'{students}', inline=True)
    embed.add_field(name=f'{FILTER} Type', value=f'`Server`', inline=True)
    embed.add_field(name=f'{TIME} Open', value=f'<t:{int(time.time())}:R>', inline=True)

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
        description=f'Current status of Server Study Room **{room}**!'
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

def server_list_embed(rooms: list, user: discord.User, server_name: str) -> discord.Embed:
    embed = EmbedFactory.base_embed(
        user=user,
        author_text=ROOMS,
        title=f'{LIST} List of open server rooms',
        description=f'All actives Server Study Room of `{server_name}`'
    )

    for room in rooms:

        student_names = ', '.join([f'<@{uid}>' for uid in room.students.keys()]) 
        
        embed.add_field(
            name=f'{room.name}', 
            value=f'{student_names}', 
            inline=True
        )        

    return embed
