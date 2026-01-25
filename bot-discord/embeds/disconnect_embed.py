import discord
from embeds.factory import EmbedFactory
from utils.constants import PanelsText, Emojis

DISCONNECT = PanelsText.DISCONNECT

DISCORD = Emojis.DISCORD
FILTER = Emojis.FILTER
NO_WIFI = Emojis.NO_WIFI
TIME = Emojis.TIME

def private_disc_embed(room: str, guild_name: str, duration: str) -> discord.Embed:
    embed = EmbedFactory.base_embed(
        user=guild_name,
        author_text=DISCONNECT,
        title=f'{NO_WIFI} AUTO-CLOSE - **{room}**',
        description=f'You close automatically the Server Study Room `{room.name}` of `{guild_name}` due to a disconnection with the voice channel.'
    )

    embed.add_field(name=f'{DISCORD} Server', value=f'**{guild_name}**', inline=True)
    embed.add_field(name=f'{FILTER} Type', value=f'`Private`', inline=True)
    embed.add_field(name=f'{TIME} Total time', value=f'`{duration}`', inline=True)

    embed.footer('Remember to close your Server Study Room before disconnecting. You **cannot** be in there without being on a voice channel!')

    return embed

def server_disc_embed(room: str, guild_name: str, duration: str) -> discord.Embed:
    embed = EmbedFactory.base_embed(
        user=guild_name,
        author_text=DISCONNECT,
        title=f'{NO_WIFI} AUTO-LEAVE - **{room}**',
        description=f'You left automatically the Server Study Room `{room.name}` of `{guild_name}` due to a disconnection with the voice channel.'
    )

    embed.add_field(name=f'{DISCORD} Server', value=f'**{guild_name}**', inline=True)
    embed.add_field(name=f'{FILTER} Type', value=f'`Server`', inline=True)
    embed.add_field(name=f'{TIME} Total time', value=f'`{duration}`', inline=True)

    embed.footer('Remember to leave your Server Study Room before disconnecting. You **cannot** be in there without being on a voice channel!')

    return embed

def public_disc_embed(room: str, duration: str) -> discord.Embed:
    embed = EmbedFactory.base_embed(
        user='Public',
        author_text=DISCONNECT,
        title=f'{NO_WIFI} AUTO-LEAVE - **{room}**',
        description=f'You left automatically the Public Study Room `{room.name}` due to a disconnection with the voice channel.'
    )

    embed.add_field(name=f'{DISCORD} Public Room', value=f'`{room}`', inline=True)
    embed.add_field(name=f'{FILTER} Type', value=f'`Public`', inline=True)
    embed.add_field(name=f'{TIME} Total time', value=f'`{duration}`', inline=True)

    embed.footer('Remember to close your Public Study Room before disconnecting. You **cannot** be in there without being on a voice channel!')

    return embed