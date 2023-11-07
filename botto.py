# Import necessary libraries
import os
import discord
import configparser
from dotenv import load_dotenv
from collections import Counter

# Load environment variables
load_dotenv()
# Get the Discord token from environment variables
TOKEN = os.getenv('DISCORD_TOKEN')

# Create a client instance with all intents enabled
client = discord.Client(intents=discord.Intents.all())

# Event handler for when the bot has connected to Discord
@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord! Woohoo!')

# Create a ConfigParser instance
config = configparser.ConfigParser()
# Define the configuration file
CONFIG_FILE = 'jottobotto.ini'

# Create the configuration file
with open(CONFIG_FILE, 'w') as f:
    config.write(f)

# Define an embed for the Jotto game
embed = discord.Embed(title="Jotto Game 1", description="", color=0x0000FF)
embed.add_field(name='', value='')

# Event handler for when a message is received
@client.event
async def on_message(message):
    # Ignore messages sent by the bot itself
    if message.author == client.user:
        return
    
    # Read the configuration data
    config.read(CONFIG_FILE)
    
    # If the message is '!jotto', start a new game
    if message.content == '!jotto':
        # Initialize the configuration data for the new game
        config['1'] = {'word_list': ""}
        config['2'] = {'word_list': ""}
        config['info'] = {'player_turn': "1", 'secret_word': "WORDS", 'turn_num': "1"}
        # Write the configuration data to the file
        with open(CONFIG_FILE, 'w') as f:
            config.write(f)
        # Send the embed to the channel
        await message.channel.send(embed=embed)

    # If the message starts with "!g", process a guess
    if message.content.startswith("!g"):
        # Extract the guessed word from the message
        guess_word = message.content.split()[1]
        # Read the current game state from the configuration data
        player_turn = config['info']['player_turn']
        secret_word = config['info']['secret_word']
        turn_num = config['info']['turn_num']
        word_list = config[player_turn]['word_list']
        # Calculate the number of matching characters between the guessed word and the secret word
        res = sum((Counter(secret_word) & Counter(guess_word)).values())
        # Add the guessed word and the number of matches to the word list
        words = "\n".join([word_list, guess_word + "  " + str(res)])
        config[player_turn]['word_list'] = words
        # Write the updated configuration data to the file
        with open(CONFIG_FILE, 'w') as f:
            config.write(f)

        # Read the word lists from the configuration data
        word_list_1 = config['1']['word_list'].splitlines()
        word_list_2 = config['2']['word_list'].splitlines()
        # Pad the shorter list with empty strings so that both lists have the same length
        while len(word_list_1) < len(word_list_2):
            word_list_1.append("")
        while len(word_list_2) < len(word_list_1):
            word_list_2.append("")
        # Combine the two lists into a single string, with the words from the first player aligned to the left and the words from the second player aligned to the right
        display_words = "\n".join(w1.ljust(20) + "    " + w2 for w1, w2 in zip(word_list_1, word_list_2))
        # Update the embed with the new word lists
        embed.set_field_at(index=0, name='', value=display_words)
        # Switch the turn to the other player
        config['info']['player_turn'] = "1" if player_turn == "2" else "2"
        # Increment the turn number if it's the second player's turn
        config['info']['turn_num'] = str(int(turn_num) + 1) if player_turn == "2" else turn_num
        # Write the updated configuration data to the file
        with open(CONFIG_FILE, 'w') as f:
            config.write(f)
        # Send the updated embed to the channel
        await message.channel.send(embed=embed)

# Start the bot
client.run(TOKEN)