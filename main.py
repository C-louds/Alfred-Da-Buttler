import nextcord
from nextcord.ext import commands
#from keep_alive import keep_alive
import os

intents = nextcord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix='/', intents=intents)

@client.event
async def on_ready():
    print("----------------------------------")
    print("Alfred Da' Butler is always available!")
    print("----------------------------------")
    
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        print(f'cogs.{filename[:-3]}')
#client.load_extension('trial_cog')
BOTTOKEN = os.environ['Discord_Bot']
#keep_alive()
client.run(BOTTOKEN)

