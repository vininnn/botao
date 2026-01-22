import discord

async def send_dm_safe(user: discord.User | discord.Member, msg: str) -> None:
    """Send a DM securely, ignoring if DMs are closed.

    Args:
        user (discord.User | discord.Member): The Discord User/Member object.
        msg (str): Message to send via DM.
    """
    try:
        await user.send(msg)
    except discord.Forbidden:
        # Ignores if the user blocks the bot or DMs
        pass