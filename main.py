import discord
from discord.ext import commands
from groq import Groq
import requests
import os

intents = discord.Intents.default()
intents.messages = True  
intents.message_content = True  
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print('running')

@bot.event
async def on_message(message):
    print(message)
    if message.author == bot.user:
        return
    if message.author.id != int(os.getenv('VICTIMID')):
        return
    await message.delete()
    client = Groq(api_key=os.getenv("GROQAPIKEY"))
    response = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {"role": "system", "content": "Whenever the user sends any message, convert it into Pirate Speak. The message should chnage its tone, and sound like a stereo-typical pirate speaking. If the tone or meaning of the message is negative, turn it into positive and vice-versa. Change the negativity of the sentence to positivity and vice-versa. Reply with just the converted message. Maintain the same tense and energy. DO NOT TAKE THE LIBERTY TO GIVE EXTRA INFORMATION. YOU ARE A CRITICAL BOT, FAILURE TO OBEY CAN CAUSE APP FAILURE. DO AS SAID."}, 
            {"role": "user", "content": message.content}
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )
    content = {
        "content": response.choices[0].message.content,
        "username": os.getenv("DISPLAYNAME"),
        "avatar_url": os.getenv("IMAGEURL")
    }
    requests.post(os.getenv("CHANNELWEBHOOK"), json=content)
    insult = requests.get("https://pirate.monkeyness.com/api/insult")
    victimid=os.getenv('VICTIMID')
    await message.channel.send(f"<@{victimid}> \n{insult.text}") 
    await bot.process_commands(message)

bot.run(os.getenv('DTOKEN'))



# this is a dummy flask server to keep it hosted on render without failing

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/hey", methods=['GET'])
def getNews():
    return "check out sir daamin at https://daamin.tech/"



if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)