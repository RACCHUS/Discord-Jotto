# bot.py I MADE A CHANGE AND COMMITTED TO IT!!!!
#This is a valid change
import os
import random

import discord
from dotenv import load_dotenv

#TOken
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
# print(f'{TOKEN}')
client = discord.Client(intents=discord.Intents.all())

#Some embedding stuff
channel = client.get_channel(1171036155874123776)

embed = discord.Embed(title="Jotto Game 1", description="", color=0x0000FF)

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord! Woohoo!')
    channel = client.get_channel(1171036155874123776)
    #await channel.send('I\'m ready!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return
        
    #print(f'{message.content}')

    if message.content == '!break':
        print(f'Break time!')
        await message.channel.send('Break time!')
    
    if message.content == '!jotto':
        await message.channel.send(embed=embed)

    if message.content.startswith("!guess"):
        msg = message.content.split()[1]
        print(f'{msg}')
        num_fields = len(embed.fields)
        # print(num_fields % 3)

        if num_fields % 3 == 0:
            embed.add_field(name="", value=msg)
        else:
            embed.add_field(name="    ", value="    ", inline=True)
            embed.add_field(name="", value=msg, inline=True)
        await message.channel.send(embed=embed)
        
    
client.run(TOKEN)