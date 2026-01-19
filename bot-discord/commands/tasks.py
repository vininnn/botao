import discord
from discord import app_commands
from managers.task_manager import TaskManager

# Function that register the commands
def register_task_commands(tree: app_commands.CommandTree, taskManager: TaskManager):
    

    task_group = app_commands.Group(name='task', description='Task manager')

    @task_group.command(name='new', description='Add a new task')
    @app_commands.describe(task='task name')
    async def task_new(interaction: discord.Interaction, task: str):
        await interaction.response.defer()
        try:
            taskManager.add_task(interaction.user.id, task)
            await interaction.followup.send(f'Task add successfully! Task: "{task}"')
            
        except ValueError as e:
            await interaction.followup.send(f'{str(e)}', ephemeral=True)

    @task_group.command(name='complete', description='Mark a task to completed')
    @app_commands.describe(task='task name to complete')
    async def task_complete(interaction: discord.Interaction, task: str):
        await interaction.response.defer()
        try:
            taskManager.remove_task(interaction.user.id, task)
            await interaction.followup.send(f'"{task}" completed successfully! Good work {interaction.user.mention}!')

        except ValueError as e:
            await interaction.followup.send(f'{str(e)}', ephemeral=True)

    @task_group.command(name='current', description='Show your current tasks')
    async def task_complete(interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            tasks = taskManager.get_tasks(interaction.user.id)
            formatted_tasks = '\n'.join(f'- {task}' for task in tasks)
            await interaction.followup.send(f'Your ongoing tasks:\n{formatted_tasks}')

        except ValueError as e:
            await interaction.followup.send(f'{str(e)}', ephemeral=True)

    tree.add_command(task_group)
        