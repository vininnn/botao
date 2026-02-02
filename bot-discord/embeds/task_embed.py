import discord
from embeds.factory import EmbedFactory
from utils.constants import PanelsText, Emojis

TASKS = PanelsText.TASKS

EMPTY = Emojis.EMPTY
LIST = Emojis.LIST

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
        title=f'{LIST} List of current tasks',
        description=f'All current tasks of <@{user.id}>.'
    )
    
    i = 1
    if not tasks:
        embed.add_field(name=f'{EMPTY} Empty task list', value='You have no tasks')
    else:
        for task in tasks:
            embed.add_field(
                name=f'{i}. {task}',
                value='\u200b',
                inline=False
            )
            i += 1
    
    return embed
