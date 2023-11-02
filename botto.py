# bot.py
import os
import random

import discord
from dotenv import load_dotenv

#TOken
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
print(f'{TOKEN}')
client = discord.Client(intents=discord.Intents.all())

#Some embedding stuff
channel = client.get_channel(1169182459611590688)

embed = discord.Embed(title="My Title", description="My Description", color=0x0000FF)
embed.add_field(name="Field Name", value="Field Value")
embed.set_footer(text="My Footer")

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord! Woohoo!')
    channel = client.get_channel(1169182459611590688)
    await channel.send('https://tenor.com/view/ready-im-ready-running-spongebob-squarepants-gif-4184916')

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
    
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    if message.content == '99!':
        response = random.choice(brooklyn_99_quotes)
        await message.channel.send(response)
     
    if message.content == '!break':
        print(f'Break time!')
        await message.channel.send('Break time!')
    
    if message.content == '!embed':
        await message.channel.send(embed=embed)
    
client.run(TOKEN)