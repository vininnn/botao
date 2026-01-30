import discord
from embeds.quote_embed import inspirational_embed
from services.quotes_services import get_inspirational_quote
from utils.constants import Emojis

class QuoteView(discord.ui.View):
    def __init__(self, user: discord.User):
        super().__init__(timeout=None)
        
        self.user = user

    @discord.ui.button(label='New Quote', style=discord.ButtonStyle.secondary, emoji=Emojis.QUOTATION_MARKS)
    async def new_quote_view(self, interaction: discord.Interaction, button: discord.ui.Button):
        quote, author = await get_inspirational_quote()
        embed = inspirational_embed(quote, author, self.user)

        await interaction.response.edit_message(embed=embed, view=self)
