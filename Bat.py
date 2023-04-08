import discord
import random
import time
import os

client = discord.Client()

# Read messages from txt file and store them in a list
with open('pesan.txt', 'r') as f:
    messages = f.readlines()

# Remove newline characters from messages
messages = [m.strip() for m in messages]

# Define server ID to send messages to
server_id = 1234567890

# Define time interval in seconds to send messages
interval = 150

# Define time interval in seconds to delete messages
delete_interval = 30

# Define list of error messages
error_messages = [
    "Gagal mengirim pesan. Silakan coba lagi nanti.",
    "Terjadi kesalahan saat mengirim pesan. Mohon tunggu beberapa saat dan coba lagi.",
    "Pesan gagal dikirim. Mohon coba beberapa saat lagi."
]

# Function to send message to a channel
async def send_message(channel, message):
    try:
        await channel.send(message)
    except:
        print(f"Failed to send message to channel {channel}")
        notify_error()

# Function to notify errors
def notify_error():
    error_message = random.choice(error_messages)
    print(error_message)

# Function to send messages to the server
async def send_messages():
    server = client.get_guild(server_id)
    channels = server.text_channels
    for channel in channels:
        message = random.choice(messages)
        await send_message(channel, message)
        time.sleep(5)

# Function to delete messages in a channel
async def delete_messages(channel):
    messages = await channel.history(limit=200).flatten()
    for message in messages:
        await message.delete()

# Event handler for bot ready event
@client.event
async def on_ready():
    print('Bot is ready.')

# Event handler for timer event
@client.event
async def on_timer():
    while True:
        await send_messages()
        time.sleep(interval)

# Event handler for message received event
@client.event
async def on_message(message):
    if message.content.startswith('!delete'):
        await delete_messages(message.channel)
    elif message.content.startswith('!start'):
        await message.channel.send('Bot is starting...')
        client.loop.create_task(on_timer())
    elif message.content.startswith('!stop'):
        await message.channel.send('Bot is stopping...')
        for task in client.loop.tasks:
            task.cancel()
    elif message.content.startswith('!setserver'):
        global server_id
        server_id = int(message.content.split()[1])
        await message.channel.send(f"Server ID has been set to {server_id}.")

# Get Discord bot token from environment variable
token = os.getenv('DISCORD_BOT_TOKEN')

# Run the bot
client.run(token)
