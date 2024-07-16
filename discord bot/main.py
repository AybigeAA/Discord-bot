import discord
from discord.ext import commands
import os


TOKEN ='your bot token'
CHANNEL_ID =1235 #add your discord channel's id, 1235 is a sample.     
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.id == CHANNEL_ID:
        await bot.process_commands(message)

# function for loading the cogs
async def load_cogs():
    await bot.load_extension('cogs.load_update')    
    await bot.load_extension('cogs.add_role')

    await bot.load_extension('cogs.send_invite')
    await bot.load_extension('cogs.add_nick')
    await bot.load_extension('cogs.show_user')
    await bot.load_extension('cogs.send_message')
    await bot.load_extension('cog.ban_users')    
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')
    await load_cogs()  

bot.run(TOKEN)
