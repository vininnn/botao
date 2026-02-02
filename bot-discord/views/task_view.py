import discord
from discord import ui
from managers.task_manager import TaskManager
from embeds.task_embed import *
from utils.constants import Emojis

CHECKBOX = Emojis.CHECKBOX
PLUS = Emojis.PLUS
UPDATE = Emojis.UPDATE

class TaskNewModal(ui.Modal, title='New Task'):
    name = ui.TextInput(
        label='What is your new task?',
        placeholder='Ex: Do homework, Read a book...',
        style=discord.TextStyle.short,
        required=True,
        max_length=20
    )

    def __init__(self, taskManager: TaskManager, view_to_update):
        super().__init__()
        self.taskManager = taskManager
        self.view_to_update = view_to_update

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        user_id = interaction.user.id
        task = self.name.value

        try:
            self.taskManager.add_task(user_id, task)

            tasks = self.taskManager.get_tasks(user_id)
            embed = task_list_embed(tasks, interaction.user)

            if self.view_to_update.message:
                await self.view_to_update.message.edit(embed=embed, view=self.view_to_update)

            await interaction.followup.send(f'Task added sucessfully! - {task}""', ephemeral=True)

        except ValueError as e:
            await interaction.followup.send(str(e), ephemeral=True)
        
class TaskCompleteSelect(ui.Select):
    def __init__(self, tasks, taskManager: TaskManager, parent_view):
        self.taskManager = taskManager
        self.parent_view = parent_view

        options = []
        for task in tasks[:25]: # Discord limit of options
            options.append(discord.SelectOption(label=task, value=task))

        super().__init__(
            placeholder='Task to complete', 
            options=options,
            min_values=1,
            max_values=1
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        user = interaction.user
        user_id = user.id

        task_to_complete = self.values[0]

        try:
            self.taskManager.remove_task(user_id, task_to_complete)

            tasks = self.taskManager.get_tasks(user_id)
            embed = task_list_embed(tasks, user)
            
            if self.parent_view.message:
                await self.parent_view.message.edit(embed=embed, view=self.parent_view)

            await interaction.followup.send(f'Task completed! - "{task_to_complete}"', ephemeral=True)
        
        except ValueError as e:
            await interaction.followup.send(f'{str(e)}', ephemeral=True)    


class TaskCompleteView(ui.View):
    def __init__(self, tasks, taskManager, main_view):
        super().__init__(timeout=60)
        self.owner_id = main_view.owner_id
        self.add_item(TaskCompleteSelect(tasks, taskManager, main_view))

class TaskDashboardView(ui.View):
    def __init__(self, taskManager: TaskManager, owner_id: int):
        super().__init__(timeout=300)
        self.taskManager = taskManager
        self.owner_id = owner_id
        self.message = None

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.owner_id

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        if self.message:
            await self.message.edit(view=self)

    @ui.button(label='New Task', style=discord.ButtonStyle.secondary, emoji=PLUS)
    async def new_task(self, interaction: discord.Interaction, button: ui.Button):
        user_id = interaction.user.id
        if user_id != self.owner_id:
            await interaction.response.send_message('You cannot edit this list! Create your own list /task list', ephemeral=True)
            return False
        
        modal = TaskNewModal(self.taskManager, self)
        await interaction.response.send_modal(modal)

    @ui.button(label='Complete Task', style=discord.ButtonStyle.secondary, emoji=CHECKBOX)
    async def complete_task(self, interaction: discord.Interaction, button: ui.Button):
        user_id = interaction.user.id
        if interaction.user.id != self.owner_id:
            await interaction.response.send_message('You cannot edit this list! Create your own list /task list', ephemeral=True)
            return False
        
        await interaction.response.defer(ephemeral=True)

        tasks = self.taskManager.get_tasks(user_id)
        if not tasks:
            await interaction.followup.send('Your list is empty!', ephemeral=True)
            return
        
        view = TaskCompleteView(tasks, self.taskManager, self)
        await interaction.followup.send('Select the task you want to complete:', view=view, ephemeral=True)
