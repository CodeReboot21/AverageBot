import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import random
from keep_alive import keep_alive

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

@bot.hybrid_command(name='hello')
async def hello(ctx: commands.Context):
    """Responds with a greeting"""
    await ctx.send(f"Howdy {ctx.author.mention}!")

@bot.hybrid_command(name='rps')
@app_commands.describe(choice='Your choice: rock, paper, or scissors')
async def rps(ctx: commands.Context, choice: str):
    """Play a game of Rock, Paper, Scissors"""
    choices = ["rock", "paper", "scissors"]
    if choice not in choices:
        await ctx.send("Invalid choice! Please choose rock, paper, or scissors.")
        return

    bot_choice = random.choice(choices)
    if choice == bot_choice:
        result = "It's a tie!"
    elif (choice == "rock" and bot_choice == "scissors") or \
         (choice == "paper" and bot_choice == "rock") or \
         (choice == "scissors" and bot_choice == "paper"):
        result = "You win!"
    else:
        result = "You lose!"

    response = f"You chose {choice}, I chose {bot_choice}. {result}"
    await ctx.send(response)

@bot.hybrid_command(name='mimic')
@app_commands.describe(action='Choose to activate or deactivate mimic mode',
                       user='The user to mimic (only for activate)')
async def mimic(ctx: commands.Context, action: str, user: discord.User = None):
    """Toggle mimic mode on and off"""
    global mimic_mode, mimic_user_id

    if action.lower() == 'activate':
        if user is None:
            await ctx.send("You need to mention a user to mimic.")
            return
        mimic_mode = True
        mimic_user_id = user.id
        await ctx.send(f"Mimic mode activated! Mimicking {user.name}.")
    elif action.lower() == 'deactivate':
        mimic_mode = False
        mimic_user_id = None
        await ctx.send("Mimic mode deactivated!")
    else:
        await ctx.send("Invalid action! Use 'activate' or 'deactivate'.")

@bot.hybrid_command(name='gamble')
async def gamble(ctx: commands.Context):
  await ctx.send(random.choice(["You lost a limb", "You won an extra limb!", "You lost your life savings", "You won a crore rupess!"]))

@bot.hybrid_command(name='list')
async def list(ctx: commands.Context):
    global synced
    for cmd in synced:
      await ctx.send(cmd.name)

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

# Run the bot with the token from environment variable
keep_alive()
bot.run(os.getenv('TOKEN'))
