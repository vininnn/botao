import discord
from embeds.utils_embed import display_author

def task_new_embed(task: str, user: discord.User) -> discord.Embed:
    embed = discord.Embed(
        title='New task added',
        description=f'**{task}** was addes into your task list.',
        color=discord.Color.blurple(),
    )
    
    display_author(embed, user)
    
    return embed

def task_complete_embed(task: str, user: discord.User) -> discord.Embed:
    embed = discord.Embed(
        title='Task completed',
        description=f'**{task}** was completed.',
        color=discord.Color.blurple(),
    )
    
    display_author(embed, user)
    
    return embed

def task_current_embed(tasks: list[str], user: discord.User) -> discord.Embed:
    embed = discord.Embed(
        title='Your current tasks',
        color=discord.Color.blurple(),
    )
    
    display_author(embed, user)

    i = 1
    for task in tasks:
        embed.add_field(
            name=f'{i}. {task}',
            value='\u200b',
            inline=False
        )
        i += 1
    
    return embed
