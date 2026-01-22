import discord
from embeds.factory import EmbedFactory
from utils.constants import PanelsText

TEXT = PanelsText.QUOTES

def inspirational_embed(quote: str, author_name: str, user: discord.User) -> discord.Embed:
    return EmbedFactory.base_embed(
        user=user,
        author_text=TEXT,
        title=author_name,
        description=quote
    )
