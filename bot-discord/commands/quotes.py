import discord
from discord import app_commands
import json
from services.quotes_services import get_inspirational_quote

with open("data/sad_words.json", encoding="utf-8") as file:
    SAD_WORDS = json.load(file)["sad_words"]

# Event that response sad words
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    
    if any(word in message.content.lower() for word in SAD_WORDS):
        await message.reply(f"Don't feel down {message.author.mention} — you will get through this.")

# Function that register the commands
def register_quotes(tree: app_commands.CommandTree):
    # Send inspirational quotes
    @tree.command(name='inspiration', description='Send a random inspirational quote')
    async def inspiration(interaction: discord.Interaction):
        await interaction.response.defer()

        quote = await get_inspirational_quote()
        await interaction.followup.send(quote)
