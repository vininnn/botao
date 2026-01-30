import discord
from embeds.factory import EmbedFactory
from utils.constants import PanelsText

TASKS = PanelsText.TASKS

def task_new_embed(task: str, user: discord.User) -> discord.Embed:
    return EmbedFactory.base_embed(
        user=user,
        author_text=TASKS,
        title='New task added',
        description=f'**{task}** was added into your task list.'
    )

def task_complete_embed(task: str, user: discord.User) -> discord.Embed:
    return EmbedFactory.base_embed(
        user=user,
        author_text=TASKS,
        title='Task completed',
        description=f'**{task}** was completed.'
    )

def task_list_embed(tasks: list[str], user: discord.User) -> discord.Embed:
    embed = EmbedFactory.base_embed(
        user=user,
        author_text=TASKS,
        title='Your current tasks',
    )
    
    i = 1
    for task in tasks:
        embed.add_field(
            name=f'{i}. {task}',
            value='\u200b',
            inline=False
        )
        i += 1
    
    return embed
