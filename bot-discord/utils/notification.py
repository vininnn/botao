import discord

async def send_dm_safe(user: discord.User | discord.Member, msg: discord.Embed | str) -> None:
    """Send a DM securely, ignoring if DMs are closed.

    Args:
        user (discord.User | discord.Member): The Discord User/Member object.
        msg (discord.Embed | str): Message to send via DM.
    """
    try:
        if isinstance(msg, discord.Embed):
            await user.send(embed=msg)
        else:
            await user.send(content=msg)
    except discord.Forbidden:
        # Ignores if the user blocks the bot or DMs
        pass