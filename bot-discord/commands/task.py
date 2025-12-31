import discord
from discord import app_commands
from managers.task_manager import TaskManager

task_manager = TaskManager()

def register_task(tree: app_commands.CommandTree):

    # Add a task
    @tree.command(name='task', description='Add a new task')
    @app_commands.describe(task='Task description')
    async def task(interaction: discord.Interaction, task: str):
        await interaction.response.defer()

        user_id = interaction.user.id
        sucess = task_manager.add_task(user_id, task)

        if not sucess:
            await interaction.followup.send(f'You already have a task named "{task}" setted!')
            return

        await interaction.followup.send(f'Task add successfully! Task: "{task}"')        

    # Completes a task
    @tree.command(name='done', description='Mark a task as complete')
    @app_commands.describe(task='Task to complete')
    async def done(interaction: discord.Interaction, task: str):
        await interaction.response.defer()

        user_id = interaction.user.id
        sucess = task_manager.remove_task(user_id, task)

        if not sucess:
            await interaction.followup.send(f'You have no tasks named "{task}"!')
            return

        await interaction.followup.send(f'"{task}" completed successfully! Good work {interaction.user.mention}!') 

    # Shows the task list
    @tree.command(name='ongoing', description='Show ongoing tasks')
    async def ongoing(interaction: discord.Interaction):
        await interaction.response.defer()

        user_id = interaction.user.id
        tasks = task_manager.get_tasks(user_id)

        if not tasks:
            await interaction.followup.send('You have no tasks!')
            return

        formatted_tasks = '\n'.join(f'- {task}' for task in tasks)
        await interaction.followup.send(f'Your ongoing tasks:\n{formatted_tasks}')