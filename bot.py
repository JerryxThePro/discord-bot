import os
import discord
from discord.ext import commands

TOKEN = os.environ["DISCORD_BOT_TOKEN"]

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_interaction(interaction):
    if interaction.data.get("custom_id", "").startswith("unban_"):
        user_id = interaction.data["custom_id"].split("_")[1]
        # Optional: send POST to Flask server to unban
        await interaction.response.send_message(f"✅ Unbanned user ID: {user_id}", ephemeral=True)

bot.run(TOKEN)
