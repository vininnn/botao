import discord
from embeds.factory import EmbedFactory
from utils.constants import PanelsText, Emojis
import time

ROOMS = PanelsText.ROOMS

CLOSE_DOOR = Emojis.CLOSE_DOOR
FILTER = Emojis.FILTER
OPEN_DOOR = Emojis.OPEN_DOOR
TIME = Emojis.TIME
USER = Emojis.USER
USERS = Emojis.USERS

def private_open_embed(room: str, user: discord.User) -> discord.Embed:
    embed = EmbedFactory.base_embed(
        user=user,
        author_text=ROOMS,
        title=f'{OPEN_DOOR} Room opened - **{room}**',
        description=f'Private room **{room}** was open! Good studies <@{user.id}>!'
    )

    embed.add_field(name=f'{USER} Member', value=f'<@{user.id}>', inline=True)
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

    embed.add_field(name=f'{USER} Member', value=f'<@{user.id}>', inline=True)
    embed.add_field(name=f'{FILTER} Type', value=f'`Private`', inline=True)
    embed.add_field(name=f'{TIME} Total time', value=f'`{duration}`', inline=True)

    return embed


def server_open_embed(room: str, user: discord.User) -> discord.Embed:
    embed = EmbedFactory.base_embed(
        user=user,
        author_text=ROOMS,
        title=f'{OPEN_DOOR} Room opened - **{room}**',
        description=f'Private room **{room}** was open! Good studies <@{user.id}>!'
    )

    embed.add_field(name=f'{USER} Member', value=f'<@{user.id}>', inline=True)
    embed.add_field(name=f'{FILTER} Type', value=f'`Private`', inline=True)
    embed.add_field(name=f'{TIME} Open', value=f'<t:{int(time.time())}:R>', inline=True)

    embed.set_image(url='https://mir-s3-cdn-cf.behance.net/project_modules/1400/58a87a182606383.6530875274ecf.gif')

    return embed