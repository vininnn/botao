import discord
from datetime import datetime
from utils.constants import Colors

class EmbedFactory:
    """Represents an factory of a standardized base embeds."""
    @staticmethod
    def base_embed(user: discord.User, author_text: str = None, title: str = None, description: str = None, color: discord.Color = Colors.DEFAULT):
        """Standardized base for Embeds, configuring author, cores and structure.

        Args:
            user (discord.User): The Discord User object.
            author_text (str, optional): Custom text for the author field. If none, it gets the user display_name. Defaults to None.
            title (str, optional): Embed main title. Defaults to None.
            description (str, optional): Embed description text. Defaults to None.
            color (discord.Color, optional): Embed lateral color. Defaults to Colors.DEFAULT (discord.Color.blurple()).

        Returns:
            discord.Embed: Embed object from Discord.
        """
        embed = discord.Embed(
            title=title,
            description=description,
            color=color,
        )

        if not author_text:
            author_text=user.display_name

        embed.set_author(
            name=author_text,
            icon_url=user.display_avatar.url
        )

        return embed
    