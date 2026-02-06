import discord
from discord import ui
from managers.private_room_manager import PrivateRoomManager
from embeds.room_embed import *
from utils.constants import Emojis

LEAVE = Emojis.LEAVE
LIST = Emojis.LIST
UPDATE = Emojis.UPDATE

class ReOpenRoomModal(ui.Modal, title='ReOpen'):
    name = ui.TextInput(
        label='Name of your new room:',
        placeholder='Ex: Math, programming...',
        style=discord.TextStyle.short,
        required=True,
        max_length=20
    )

    def __init__(self, privateManager: PrivateRoomManager, user_id: int, main_view):
        super().__init__()
        self.privateManager = privateManager
        self.user_id = user_id
        self.main_view = main_view

    async def on_submit(self, interaction: discord.Interaction):
        if self.privateManager.is_user_in_private_room(self.user_id):
            self.privateManager.leave(self.user_id)

        try:
            self.privateManager.open(self.user_id, interaction.guild.name, self.name.value)
            
            new_room = self.privateManager.get_open_room(self.user_id)
            embed = private_open_embed(new_room, interaction.user)
            await interaction.response.edit_message(embed=embed, view=self.main_view)
        
        except ValueError as e:
            await interaction.response.send_message(f'{str(e)}', ephemeral=True)

class BaseRoomView(ui.View):
    def __init__(self, privateManager: PrivateRoomManager, user_id: int):
        super().__init__(timeout=300)
        self.privateManager = privateManager
        self.user_id = user_id

    @ui.button(label='Leave', style=discord.ButtonStyle.secondary, emoji=LEAVE)
    async def leave(self, interaction: discord.Interaction, button: ui.Button):
        try:
            room = self.privateManager.leave(self.user_id)
            duration = format_time(room.duration_seconds)
            
            for child in self.children:
                child.disable = True

            embed = private_leave_embed(room.name, interaction.user, duration)
            await interaction.response.edit_message(embed=embed, view=self)
        
        except ValueError as e:
            await interaction.response.send_message(f'{str(e)}', ephemeral=True)           

    @ui.button(label='Summary', style=discord.ButtonStyle.secondary, emoji=LIST)
    async def summary(self, interaction: discord.Interaction, button: ui.Button):
        try:
            history = self.privateManager.get_left_rooms(self.user_id)
            rooms = {}
            for room in history:
                rooms[room.name] = rooms.get(room.name, 0) + room.duration_seconds

            embed = room_summary_embed(rooms, interaction.user)
            
            await interaction.response.send_message(embed=embed)

        except ValueError as e:   
            await interaction.response.send_message(f'{str(e)}', ephemeral=True)
        
class PrivateRoomView(BaseRoomView):
    def __init__(self, privateManager, user_id):
        super().__init__(privateManager, user_id)

        @ui.button(label='Switch Room', style=discord.ButtonStyle.secondary, emoji=UPDATE)
        async def switch_room(self, interaction: discord.Interaction, button: ui.Button):
            await interaction.response.send_modal(ReOpenRoomModal(self.privateManager, self.user_id, self))
            