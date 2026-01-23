import discord
from discord import app_commands

from managers.task_manager import TaskManager
from embeds.task_embed import *

# Function that register the commands
def register_task_commands(tree: app_commands.CommandTree, taskManager: TaskManager):
    """Registers the '/task' command group and its subcommands to the bot."""
    
    # Father Group (/task)
    task_group = app_commands.Group(name='task', description='Task manager')

    # New (/task new)
    @task_group.command(name='new', description='Add a new task')
    @app_commands.describe(task='task name')
    async def task_new(interaction: discord.Interaction, task: str):
        """Creates a new task."""
        user_id = interaction.user.id

        try:
            taskManager.add_task(user_id, task)
            embed = task_new_embed(task, interaction.user)

            await interaction.response.send_message(embed=embed)
            
        except ValueError as e:
            await interaction.response.send_message(f'{str(e)}', ephemeral=True)

    # Complete (/task complete)
    @task_group.command(name='complete', description='Mark a task to completed')
    @app_commands.describe(task='task name')
    async def task_current(interaction: discord.Interaction, task: str):
        """Remove a completed task."""
        user_id = interaction.user.id

        try:
            taskManager.remove_task(user_id, task)
            embed = task_complete_embed(task, interaction.user)

            await interaction.response.send_message(embed=embed)

        except ValueError as e:
            await interaction.response.send_message(f'{str(e)}', ephemeral=True)

    # List (/task list)
    @task_group.command(name='list', description='Show your current tasks')
    async def task_current(interaction: discord.Interaction):
        """List the user\'s current tasks."""
        user_id = interaction.user.id

        try:
            tasks = taskManager.get_tasks(user_id)
            embed = task_current_embed(tasks, interaction.user)

            await interaction.response.send_message(embed=embed)

        except ValueError as e:
            await interaction.response.send_message(f'{str(e)}', ephemeral=True)

    tree.add_command(task_group)
        