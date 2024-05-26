# commands.py
import discord
from discord.ext import commands
from discord import app_commands
from keep_alive import keep_alive
import random
from bot_init import bot, jump_start
import requests

keep_alive()

@bot.hybrid_command(name='hello')
async def hello(ctx: commands.Context):
    """Responds with a greeting"""
    await ctx.send(f"Howdy {ctx.author.mention}!")

@bot.hybrid_command(name='stop')
async def stop(ctx: commands.Context):
    """Stops the bot"""
    if ctx.author == 'reyansh21':
        await ctx.send(f"Stopped by {ctx.author.mention}")
        await bot.close()

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
    """Gamble anything and everything"""
    await ctx.send(random.choice(["You lost a limb", "You won an extra limb!", "You lost your life savings", "You won a crore rupess!"]))


@bot.hybrid_command(name='list')
async def list(ctx: commands.Context):
    """Get a list of commands"""
    from bot_init import synced
    synced = await bot.tree.sync()
    for cmd in synced:
        await ctx.send(cmd.name)

@bot.hybrid_command(name='message')
@app_commands.describe(identifier='The username or user ID to send a message to', message='The message to send')
async def message(ctx: commands.Context, identifier: str, message: str):
    """Send an anonymous message to anyone"""
    try:
        user = None
        # Try to find user by username first
        for guild in bot.guilds:
            user = discord.utils.find(lambda u: u.name == identifier, guild.members)
            if user:
                break
        # If user not found by username, try to fetch by ID
        if not user:
            try:
                user = await bot.fetch_user(int(identifier))
            except ValueError:
                pass
        if not user:
            raise discord.NotFound(discord.Object(id=identifier), "User not found")
        
        await user.send(message)
        if isinstance(ctx, commands.Context):
            await ctx.send(f"Message sent to {user.name}!")
        else:
            await ctx.response.send_message(f"Message sent to {user.name}!", ephemeral=True)
    except discord.Forbidden:
        if isinstance(ctx, commands.Context):
            await ctx.send(f"Cannot send message to {identifier}. They might have DMs disabled.")
        else:
            await ctx.response.send_message(f"Cannot send message to {identifier}. They might have DMs disabled.", ephemeral=True)
    except discord.NotFound:
        if isinstance(ctx, commands.Context):
            await ctx.send(f"User {identifier} not found.")
        else:
            await ctx.response.send_message(f"User {identifier} not found.", ephemeral=True)
    except discord.ext.commands.errors.MissingRequiredArgument:
        if isinstance(ctx, commands.Context):
            await ctx.send(f"Missing Required Argument")
    except Exception as e:
        if isinstance(ctx, commands.Context):
            await ctx.send(f"An error occurred: {e}")
        else:
            await ctx.response.send_message(f"An error occurred: {e}", ephemeral=True)

@bot.hybrid_command(name='joke')
async def joke(ctx: commands.Context):
    """Fetches and displays a random joke."""
    url = "https://v2.jokeapi.dev/joke/Any"

    response = requests.get(url)
    data = response.json()

    if data["type"] == "single":
        await ctx.send(data["joke"])
    else:
        await ctx.send(f"{data['setup']} - {data['delivery']}")