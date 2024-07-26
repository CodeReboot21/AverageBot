# commands.py
import discord
from discord.ext import commands
from discord import app_commands
from keep_alive import keep_alive
import random
from bot_init import bot, jump_start
import asyncio
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

@bot.hybrid_command(name='trivia')
async def trivia(ctx: commands.Context):
    """Ask a trivia question"""
    questions = [
        ("What is the capital of France?", "Paris"),
        ("What is the largest planet in our solar system?", "Jupiter"),
        ("Who wrote 'Romeo and Juliet'?", "William Shakespeare"),
        ("What is the chemical symbol for water?", "H2O"),
        ("Who painted the Mona Lisa?", "Leonardo da Vinci"),
        ("What is the smallest country in the world?", "Vatican City"),
        ("What is the tallest mountain in the world?", "Mount Everest"),
        ("Who is known as the father of computers?", "Charles Babbage"),
        ("What is the hardest natural substance on Earth?", "Diamond"),
        ("Which planet is known as the Red Planet?", "Mars"),
        ("What is the fastest land animal?", "Cheetah"),
        ("Who discovered penicillin?", "Alexander Fleming"),
        ("What is the longest river in the world?", "Nile River"),
        ("What is the main ingredient in traditional Japanese miso soup?", "Miso paste"),
        ("Who was the first man to walk on the moon?", "Neil Armstrong"),
        ("What is the largest ocean on Earth?", "Pacific Ocean"),
        ("Who developed the theory of relativity?", "Albert Einstein"),
        ("What is the capital of Japan?", "Tokyo"),
        ("What is the primary language spoken in Brazil?", "Portuguese"),
        ("Who directed the movie 'Jaws'?", "Steven Spielberg"),
        ("What is the currency of the United Kingdom?", "Pound Sterling"),
        ("What is the name of the first artificial satellite launched by the Soviet Union in 1957?", "Sputnik"),
        ("Which element has the chemical symbol 'O'?", "Oxygen"),
        ("What is the most widely spoken language in the world?", "Mandarin Chinese"),
        ("Who wrote the 'Harry Potter' series?", "J.K. Rowling"),
        ("What is the capital of Canada?", "Ottawa"),
        ("What year did the Titanic sink?", "1912"),
        ("What is the main ingredient in guacamole?", "Avocado"),
        ("Who painted the ceiling of the Sistine Chapel?", "Michelangelo"),
        ("What is the largest mammal in the world?", "Blue Whale")
    ]

    question, answer = random.choice(questions)

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send(question)

    try:
        response = await bot.wait_for('message', timeout=30.0, check=check)
        if response.content.lower() == answer.lower():
            await ctx.send(f"Correct! The answer is {answer}.")
        else:
            await ctx.send(f"Wrong! The correct answer is {answer}.")
    except asyncio.TimeoutError:
        await ctx.send(f"Time's up! The correct answer was {answer}.")

@bot.hybrid_command(name='quote')
async def quote(ctx: commands.Context):
    """Fetches and displays a random inspirational quote."""
    url = "https://api.quotable.io/random"

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        await ctx.send(f"{data['content']} — {data['author']}")
    else:
        await ctx.send("Could not retrieve a quote at this time.")

@bot.hybrid_command(name='fact')
async def fact(ctx: commands.Context):
    """Fetches and displays a random fact."""
    url = "https://uselessfacts.jsph.pl/random.json?language=en"

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        # Use respond() for interactions and send() for regular messages
        if ctx.interaction:
            await ctx.interaction.response.send_message(data['text'])
        else:
            await ctx.send(data['text'])
    else:
        if ctx.interaction:
            await ctx.interaction.response.send_message("Could not retrieve a fact at this time.")
        else:
            await ctx.send("Could not retrieve a fact at this time.")
