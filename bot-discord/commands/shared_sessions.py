import discord
from discord import app_commands
from datetime import datetime, timezone


#     # Start a study session in a group
#     @tree.command(name='startwith', description='Start a timer for a specific study subject to study in a group')
#     @app_commands.describe(subject='Study subject', partner1='Who will study with you?', partner2='Who will study with you?', partner3='Who will study with you?', partner4='Who will study with you?', partner5='Who will study with you?')
#     async def start_with(
#         interaction: discord.Interaction,
#         subject: str,
#         partner1: discord.Member,
#         partner2: discord.Member = None,
#         partner3: discord.Member = None,
#         partner4: discord.Member = None,
#         partner5: discord.Member = None,
#         ):
#         await interaction.response.defer()

#         user_id = interaction.user.id
#         if user_id in study_sessions:
#             await interaction.followup.send('You are already in a study session! Quit it before you join another!')
#             return
        
#         partners_ids = []
#         partners_names = []
#         unvalidated_partner = [partner1]
#         if partner2:
#             unvalidated_partner.append(partner2)
#         if partner3:
#             unvalidated_partner.append(partner3)
#         if partner4:
#             unvalidated_partner.append(partner4)
#         if partner5:
#             unvalidated_partner.append(partner5)
            
#         for partner in unvalidated_partner:
#             if partner.bot:
#                 await interaction.followup.send('You cannot add a bot as a study partner')
#                 return
#             elif partner.id == user_id:
#                 await interaction.followup.send('You cannot add yourself as a study partner')
#                 return
#             elif partner.id in study_sessions:
#                 await interaction.followup.send(f'Your partner ({partner.name}) is already in a study session! They need to quit it before joining another!')
#                 return
#             else:
#                 partners_ids.append(partner.id)
#                 partners_names.append(partner.name)

#         partners_ids.append(user_id)
#         partners_names.append(interaction.user.name)
#         for partner in partners_ids:
#             study_sessions[partner] = {subject: {'start_time': datetime.now(timezone.utc), 'partners_ids': partners_ids, 'partners_names': partners_names, 'session_creator_id': user_id, 'session_creator_name': interaction.user.name}}

#         await interaction.followup.send(f'Timer started successfully! Study subject: "{subject}". Member in the group: {partners_names}')


#         else:
#             remaining_partners_ids = []
#             remaining_partners_names = []
#             start_time = study_sessions[user_id][subject].pop('start_time')
#             for id in study_sessions[user_id][subject]['partners_ids']:
#                 if id != user_id:
#                     remaining_partners_ids.append(id)
#             for name in study_sessions[user_id][subject]['partners_names']:
#                 if name != interaction.user.name:
#                     remaining_partners_names.append(name)

#             for id in study_sessions[user_id][subject]['partners_ids']:
#                 study_sessions[id][subject]['partners_ids'] = remaining_partners_ids
#                 study_sessions[id][subject]['partners_names'] = remaining_partners_names

#         del study_sessions[user_id]
#         study_duration = datetime.now(timezone.utc) - start_time

#         if user_id not in ended_sessions:
#             ended_sessions[user_id] = {}

#         if subject not in ended_sessions[user_id]:
#             ended_sessions[user_id][subject] = study_duration
#         else:
#             ended_sessions[user_id][subject] += study_duration

#         formatted_study_duration = format_study_duration(study_duration)
#         await interaction.followup.send(f'Timer finished successfully! Time spent on "{subject}":  {formatted_study_duration}')

#         else:
#             study_duration = datetime.now(timezone.utc) - study_sessions[user_id][subject]['start_time']
#             formatted_study_duration = format_study_duration(study_duration)
#             await interaction.followup.send(f'Study session name: "{subject}". Time in session: {formatted_study_duration}. Partners of study session: {study_sessions[user_id][subject]['partners_names']}. Creator of the session: {study_sessions[user_id][subject]['session_creator_name']}.')