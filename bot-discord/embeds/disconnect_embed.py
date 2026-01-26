import discord
from embeds.factory import EmbedFactory
from utils.constants import PanelsText, Emojis

DISCONNECT = PanelsText.DISCONNECT

DISCORD = Emojis.DISCORD
FILTER = Emojis.FILTER
NO_WIFI = Emojis.NO_WIFI
TIME = Emojis.TIME

def private_disconnect_embed(room: str, guild_name: str, duration: str, user: discord.ClientUser) -> discord.Embed:
    embed = EmbedFactory.base_embed(
        user=user,
        author_text=DISCONNECT,
        title=f'{NO_WIFI} AUTO-CLOSE - **{room}**',
        description=f'You close automatically the Server Study Room `{room}` of `{guild_name}` due to a disconnection with the voice channel.'
    )

    embed.add_field(name=f'{DISCORD} Server', value=f'`{guild_name}`', inline=True)
    embed.add_field(name=f'{FILTER} Type', value=f'`Private`', inline=True)
    embed.add_field(name=f'{TIME} Total time', value=f'`{duration}`', inline=True)

    embed.set_footer(text='Remember to close your Server Study Room before disconnecting. You cannot be in there without being on a voice channel!')

    return embed

def server_disconnect_embed(room: str, guild_name: str, duration: str, user: discord.ClientUser) -> discord.Embed:
    embed = EmbedFactory.base_embed(
        user=user,
        author_text=DISCONNECT,
        title=f'{NO_WIFI} AUTO-LEAVE - **{room}**',
        description=f'You left automatically the Server Study Room `{room}` of `{guild_name}` due to a disconnection with the voice channel.'
    )

    embed.add_field(name=f'{DISCORD} Server', value=f'`{guild_name}`', inline=True)
    embed.add_field(name=f'{FILTER} Type', value=f'`Server`', inline=True)
    embed.add_field(name=f'{TIME} Total time', value=f'`{duration}`', inline=True)

    embed.set_footer(text='Remember to leave your Server Study Room before disconnecting. You cannot be in there without being on a voice channel!')

    return embed

def public_disconnect_embed(room: str, duration: str, user: discord.ClientUser) -> discord.Embed:
    embed = EmbedFactory.base_embed(
        user=user,
        author_text=DISCONNECT,
        title=f'{NO_WIFI} AUTO-LEAVE - **{room}**',
        description=f'You left automatically the Public Study Room `{room}` due to a disconnection with the voice channel.'
    )

    embed.add_field(name=f'{DISCORD} Public Room', value=f'`{room}`', inline=True)
    embed.add_field(name=f'{FILTER} Type', value=f'`Public`', inline=True)
    embed.add_field(name=f'{TIME} Total time', value=f'`{duration}`', inline=True)

    embed.set_footer(text='Remember to close your Public Study Room before disconnecting. You cannot be in there without being on a voice channel!')

    return embed