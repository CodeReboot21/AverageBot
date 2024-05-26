# bot_init.py
import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize bot with the proper intents
intents = discord.Intents.default()
intents.message_content = True  # Ensure the correct intents are enabled

# Create the bot instance
bot = commands.Bot(command_prefix="!", intents=intents)

# State variables for mimic mode
mimic_mode = False
mimic_user_id = None

def jump_start():
    pass

@bot.event
async def on_ready():
    """Event triggered when the bot is ready"""
    print(f'Logged on as {bot.user}!')
    try:
        global synced
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s): {[cmd.name for cmd in synced]}")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.event
async def on_message(message):
    """Event triggered on every message received"""
    global mimic_mode, mimic_user_id

    # Avoid the bot mimicking its own messages
    if message.author == bot.user:
        return

    # Check if mimic mode is active and the message is from the mimicked user
    if mimic_mode and message.author.id == mimic_user_id:
        await message.channel.send(message.content)

    # Log the message (optional)
    username = message.author
    user_message = message.content
    channel = message.channel
    server = message.guild
    print(f"[{server}] [{channel}] {username} {user_message}")

    # Process commands
    await bot.process_commands(message)

# Import commands to register them with the bot
import commands

# Run the bot with the token from environment variable
bot.run(os.getenv("TOKEN"))
