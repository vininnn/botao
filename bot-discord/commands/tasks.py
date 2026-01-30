import discord
from discord import app_commands

from managers.task_manager import TaskManager
from embeds.task_embed import *
from views.task_view import TaskDashboardView

# Function that register the commands
def register_task_commands(tree: app_commands.CommandTree, taskManager: TaskManager):
    """Registers the '/task' command group and its subcommands to the bot."""
    
    # Father Group (/task)
    task_group = app_commands.Group(name='task', description='Task manager')

    async def send_dashboard(interaction: discord.Interaction, msg: str = None):
        user = interaction.user
        user_id = user.id
        tasks = taskManager.get_tasks(user_id)
        embed = task_list_embed(tasks, user)
        view = TaskDashboardView(taskManager, owner_id=user_id)

        await interaction.response.send_message(content=msg, embed=embed, view=view)
        view.message = await interaction.original_response()

    # New (/task new)
    @task_group.command(name='new', description='Add a new task')
    @app_commands.describe(task='task name')
    async def task_new(interaction: discord.Interaction, task: str):
        """Creates a new task."""
        user = interaction.user
        user_id = user.id

        try:
            taskManager.add_task(user_id, task)
            await send_dashboard(interaction)

        except ValueError as e:
            await interaction.response.send_message(f'{str(e)}', ephemeral=True)

    # Complete (/task complete)
    @task_group.command(name='complete', description='Mark a task to completed')
    @app_commands.describe(task='task name')
    async def task_complete(interaction: discord.Interaction, task: str):
        """Remove a completed task."""
        user = interaction.user
        user_id = user.id

        try:
            taskManager.remove_task(user_id, task)
            await send_dashboard(interaction)

        except ValueError as e:
            await interaction.response.send_message(f'{str(e)}', ephemeral=True)

    # List (/task list)
    @task_group.command(name='list', description='Show your current tasks')
    async def task_list(interaction: discord.Interaction):
        """List the user\'s current tasks."""
        try:
            await send_dashboard(interaction)

        except ValueError as e:
            await interaction.response.send_message(f'{str(e)}', ephemeral=True)

    tree.add_command(task_group)
        