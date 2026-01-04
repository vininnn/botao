import discord
from discord import app_commands

from managers.shared_session_manager import SharedSessionManager
from utils.formatter import time_formatter

# Function that register the commands
def register_shared_sessions(tree: app_commands.CommandTree, sharedSessionManager: SharedSessionManager):

    # Start a shared study session
    @tree.command(name='startshared', description='Start a shared study session')
    @app_commands.describe(name='Session name')
    async def start_shared(interaction: discord.Interaction, name: str):
        await interaction.response.defer()

        guild_id = interaction.guild.id

        try:
            sharedSessionManager.start(guild_id, name)
            await interaction.followup.send(f'Shared session "{name}" created sucessfully')
        except ValueError as e:
            await interaction.followup.send(str(e))
    
    # Join an existing shared study session
    @tree.command(name='joinshared', description='Join a shared study session')
    @app_commands.describe(name='Session name')
    async def join_shared(interaction: discord.Interaction, name: str):
        await interaction.response.defer()

        guild_id = interaction.guild.id
        user_id = interaction.user.id

        try:
            sharedSessionManager.join(guild_id, name, user_id)
            await interaction.followup.send(f'You joined the shared session "{name}"!')
        except ValueError as e:
            await interaction.followup.send(str(e))

    # Leave your current shared study session
    @tree.command(name='leaveshared', description='Leave your shared study session')
    async def leave_shared(interaction: discord.Interaction):
        await interaction.response.defer()

        user_id = interaction.user.id

        try:
            session = sharedSessionManager.leave(user_id)
            formatted_time = time_formatter(session.duration_seconds)

            await interaction.followup.send(f'You leave the shared session "{session.session_name}".\n'
                f'Time studied: {formatted_time}')
        except ValueError as e:
            await interaction.followup.send(str(e))

    # List all current shared study sessions in the server
    @tree.command(name='listshared', description='List all shared study session in this server')
    async def list_shared(interaction: discord.Interaction):
        await interaction.response.defer()

        guild_id = interaction.guild.id
        sessions = sharedSessionManager.list_sessions(guild_id)

        if not sessions:
            await interaction.followup.send(f'There are no shared sessions in this server!')
            return
        
        msg = 'Shared Sessions:\n'

        for session in sessions:
            partipants_count = len(session.participants)
            msg += f'- "{session.name}" "({partipants_count} participants)"'

        await interaction.followup.send(msg)
