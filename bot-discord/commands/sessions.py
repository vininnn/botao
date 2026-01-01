import discord
from discord import app_commands
from datetime import datetime, timezone

from managers.session_manager import SessionManager
from utils.time_formatter import time_formatter as format_duration

sessionManger = SessionManager()

# Function that register the commands
def register_study_sessions(tree: app_commands.CommandTree):

    # Start a study session
    @tree.command(name='startsession', description='Start a study session')
    @app_commands.describe(name='Session name')
    async def start_session(interaction: discord.Interaction, name: str):
        await interaction.response.defer()

        user_id = interaction.user.id
        sucess = sessionManger.start_session(user_id, name)

        if not sucess:
            await interaction.followup.send('You are already in a study session! Quit it before you join another!')
            return
        
        await interaction.followup.send(f'Study session "{name}" started! Good studies!')

    # End a study session
    @tree.command(name='endsession', description='End your active study session')
    async def end_session(interaction: discord.Interaction):
        await interaction.response.defer()

        user_id = interaction.user.id
        session = sessionManger.end_session(user_id)

        if not session:
            await interaction.followup.send('You are not in a study session yet! Join one!', ephemeral=True)
            return

        duration = format_duration(session.duration_seconds)
        
        await interaction.followup.send(f'Session "{session.session_name}" finished!\n'
                                        f'Time studied: {duration}')


    # Show the status of your current study session
    @tree.command(name='sessionstatus', description='Show your current session status')
    async def session_status(interaction: discord.Interaction):
        await interaction.response.defer()

        user_id = interaction.user.id
        session = sessionManger.get_active_session(user_id)

        if not session:
            await interaction.followup.send('You are not in a study session yet! Join one!', ephemeral=True)
            return

        duration = format_duration(session.duration_seconds)
        
        await interaction.followup.send(f'Current session: "{session.session_name}"\n'
                                        f'Time in session: {duration}')
    

#     # Shows the total time per subject
#     @tree.command(name='studysummary', description='Shows the total hours studied in the subject')
#     @app_commands.describe(subject='Total time on subject')
#     async def study_summary(interaction: discord.Interaction, subject: str):
#         await interaction.response.defer()

#         user_id = interaction.user.id

#         if user_id not in ended_sessions:
#             await interaction.followup.send('You have no ended sessions!')
#             return

#         if subject not in ended_sessions[user_id]:
#             await interaction.followup.send(f'There are no ended sessions named "{subject}"!')
#             return

#         formatted_time = format_study_duration(ended_sessions[user_id][subject])
#         await interaction.followup.send(f'Time spent on "{subject}":  {formatted_time}') 

#     # Shows everything you studied
#     @tree.command(name='studysummary_all', description='Shows the total hours of each subject you studied')
#     async def study_summary(interaction: discord.Interaction):
#         await interaction.response.defer()

#         user_id = interaction.user.id

#         if user_id not in ended_sessions:
#             await interaction.followup.send('You have no ended sessions!')
#             return

#         all_summary = ''
#         for subject in ended_sessions[user_id]:
#             formatted_time = format_study_duration(ended_sessions[user_id][subject])
#             all_summary += f'"{subject}": {formatted_time}\n'

#         await interaction.followup.send(f'All subject studied:\n{all_summary}')   
