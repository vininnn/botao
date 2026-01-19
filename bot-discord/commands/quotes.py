import discord
from discord import app_commands
import json
from services.quotes_services import get_inspirational_quote

with open("bot-discord/data/sad_words.json", encoding="utf-8") as file:
    SAD_WORDS = json.load(file)["sad_words"]

# Event that response sad words
async def on_message(message: discord.Message):
    """Event listener that monitors messages for specific 'sad' keywords.

    If a keyword is detected, the bot replies with a supportive message.
    Ignores messages sent by bots to prevent infinite loops.

    Args:
        message (discord.Message): The message object provided by Discord.
    """
    if message.author.bot:
        return
    
    if any(word in message.content.lower() for word in SAD_WORDS):
        await message.reply(f"Don't feel down {message.author.mention} — you will get through this.")

def register_quotes(tree: app_commands.CommandTree):
    """Registers quote-related slash commands to the bot's command tree.

    Args:
        tree (app_commands.CommandTree): The bot's command tree instance.
    """
    
    @tree.command(name='inspiration', description='Send a random inspirational quote')
    async def inspiration(interaction: discord.Interaction):
        """Slash command that fetches and displays an inspirational quote from an external API.

        Args:
            interaction (discord.Interaction): The interaction object.
        """
        await interaction.response.defer()

        quote = await get_inspirational_quote()
        await interaction.followup.send(quote)
