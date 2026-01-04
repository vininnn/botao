import discord
from discord import app_commands
from datetime import datetime, timezone

from managers.session_manager import SessionManager
from utils.formatter import time_formatter

# Function that register the commands
def register_study_sessions(tree: app_commands.CommandTree, sessionManager: SessionManager):

    # Start a study session
    @tree.command(name='startsession', description='Start a study session')
    @app_commands.describe(name='Session name')
    async def start_session(interaction: discord.Interaction, name: str):
        await interaction.response.defer()

        user_id = interaction.user.id
        sucess = sessionManager.start_session(user_id, name)

        if not sucess:
            await interaction.followup.send('You are already in a study session! Quit it before you join another!')
            return
        
        await interaction.followup.send(f'Study session "{name}" started! Good studies!')

    # End a study session
    @tree.command(name='endsession', description='End your active study session')
    async def end_session(interaction: discord.Interaction):
        await interaction.response.defer()

        user_id = interaction.user.id
        session = sessionManager.end_session(user_id)

        if not session:
            await interaction.followup.send('You are not in a study session yet! Join one!', ephemeral=True)
            return

        duration = time_formatter(session.duration_seconds)
        
        await interaction.followup.send(f'Session "{session.session_name}" finished!\n'
                                        f'Time studied: {duration}')

    # Show the status of your current study session
    @tree.command(name='sessionstatus', description='Show your current session status')
    async def session_status(interaction: discord.Interaction):
        await interaction.response.defer()

        user_id = interaction.user.id
        session = sessionManager.get_active_session(user_id)

        if not session:
            await interaction.followup.send('You are not in a study session yet! Join one!', ephemeral=True)
            return

        duration = time_formatter(session.duration_seconds)
        
        await interaction.followup.send(f'Current session: "{session.session_name}"\n'
                                        f'Time in session: {duration}')

     # Shows the total time per session
    @tree.command(name='studysummary', description='Shows the total hours studied in a session')
    @app_commands.describe(name='Total time on session')
    async def study_summary(interaction: discord.Interaction, name: str):
        await interaction.response.defer()

        user_id = interaction.user.id
        session = sessionManager.get_ended_sessions(user_id)

        if not session:
            await interaction.followup.send('You have no ended sessions!')
            return

        total_seconds = sessionManager.get_total_time_by_session(user_id, name)

        if total_seconds == 0:
            await interaction.followup.send(f'There are no ended sessions named "{name}"!')
            return

        formatted_time = time_formatter(total_seconds)
        await interaction.followup.send(f'Time spent on "{name}":  {formatted_time}') 

    # Shows everything you studied
    @tree.command(name='studysummary_all', description='Shows the total hours of each session you studied')
    async def study_summary(interaction: discord.Interaction):
        await interaction.response.defer()

        user_id = interaction.user.id
        session = sessionManager.get_ended_sessions(user_id)

        if not session:
            await interaction.followup.send('You have no ended sessions!')
            return

        sessions_name = {sessions.session_name for sessions in session}

        lines = []

        for session_name in sessions_name:
            total_seconds = sessionManager.get_total_time_by_session(user_id, session_name)
            lines.append(f'- "{session_name}": {time_formatter(total_seconds)}')

        await interaction.followup.send(f'All subjects studied:\n' + '\n'.join(lines)) 
