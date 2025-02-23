import os
import discord 
from discord import app_commands
from discord.ext import commands
import json

interaction = app_commands.Interaction

# Load enviroment variables
from dotenv import load_dotenv
load_dotenv()

# To load and initialise customers' AeroCredits data
if os.path.exits('AeroCredits.json'):
    with open('AeroCredits.json', 'r') as f:
        AeroCredits = json.load(f)
else:
    AeroCredits = {}

# Bot Setup
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync() # Sync commands with Discord
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
@bot.tree.command(name='AeroCredits', description='Check your AeroCredits!')
async def AeroCredits(ctx):
    user = ctx.author
    if user.id not in AeroCredits:
        AeroCredits[user.id] = 0
    await interaction.response.send_message(f'You have {AeroCredits[user.id]} AeroCredits!')

@bot.tree.command(name='addAeroCredits', description='Add AeroCredits to your account!')
async def addAeroCredits(ctx, amount: int):
    user = ctx.author
    if user.id not in AeroCredits:
        AeroCredits[user.id] = 0
    AeroCredits[user.id] += amount
    await interaction.response.send_message(f'You now have {AeroCredits[user.id]} AeroCredits!')

@bot.tree.command(name='substractAeroCredits', description='Substract AeroCredits from your account!')
async def removeAeroCredits(ctx, amount: int):
    user = ctx.author
    if user.id not in AeroCredits:
        AeroCredits[user.id] = 0
    AeroCredits[user.id] -= amount
    await interaction.response.send_message(f'You now have {AeroCredits[user.id]} AeroCredits!')

    # Ensure the AeroCredits is not below 0
    if AeroCredits[user.id] < 0:
        AeroCredits[user.id] = 0

# Save AeroCredits to a file
    with open('AeroCredits.json', 'w') as f:
        json.dump(AeroCredits, f)

    await interaction.response.send_message('AeroCredits have been saved! They now have {AeroCredits[user.id]} AeroCredits!')

bot.run('DISCORD_TOKEN')