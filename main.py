import discord
from discord.ext import commands
import requests
import os
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print('running')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(e)

@bot.tree.command(name="who", description="Know about Daamin")
async def who(interaction: discord.Interaction):
    await interaction.response.send_message("I'm Daamin Ashai, a 14-year-old student from Jammu and Kashmir, India. I'm passionate about coding, web development, and tech projects! Check out my website: https://daamin.tech/")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.author.id != int(os.getenv('VICTIMID')):
        return
    await message.delete()
    content = {
        "content": "I'm dumb!",
        "username": os.getenv("DISPLAYNAME"),
        "avatar_url": os.getenv("IMAGEURL")
    }
    requests.post(os.getenv("CHANNELWEBHOOK"), json=content)
    insult = requests.get("https://pirate.monkeyness.com/api/insult")
    victimid = os.getenv('VICTIMID')
    await message.channel.send(f"<@{victimid}> \n{insult.text}")
    await bot.process_commands(message)

if __name__ == '__main__':
    bot.run(os.getenv('DTOKEN'))
