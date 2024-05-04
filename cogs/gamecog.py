import nextcord
from nextcord import Interaction 
from nextcord.ext import commands
import asyncio
import requests
import random
import os


NINJA_API_KEY = os.environ['Ninja_API_Key']

class GameCog(commands.Cog):
  def __init__(self, client):
    self.client = client
  
  
  def valid_word(self, prev_word, curr_word, turn, used_words):
   api_url = 'https://api.api-ninjas.com/v1/dictionary?word={}'.format(curr_word)
   response = requests.get(api_url, headers={'X-Api-Key': NINJA_API_KEY})
   #print(curr_word + ":", end="")
   #print(response.json()['valid'])
   if turn == 0:
      used_words.add(curr_word.lower())
      return response.json()['valid']
   else:
      last_c = prev_word.lower()[-1]
      if last_c == curr_word.lower()[0] and response.json()['valid'] == True:
        if curr_word.lower() not in used_words:
          used_words.add(curr_word.lower())
          return True
      else:
        return False

  
  def get_word(self, prev_word, curr_word, turn, used_words):
    word = ''
    found = False
    last_c = curr_word.lower()[-1]
    api_url = f'https://api.datamuse.com/words?sp={last_c}*'
    response = requests.get(api_url)
    #print(response.json())
    options = []
    length = len(response.json())
    for j in range(length):
      temp = response.json()[j]['word']
      options.append(temp.capitalize())
    word = random.choice(options)
    return word
  
  async def pvp(self, ctx: nextcord.Interaction):
    channel = self.client.get_channel(1227675654510874687)
    author = ctx.user
    guild = ctx.guild
    category = nextcord.utils.get(guild.categories, name='Lobbies')
    lobby_id = random.randint(36, 10000)
    lobby = await guild.create_text_channel(name='pvp-lobby-id--' + str(lobby_id), category=category)
    
    embed = nextcord.Embed(
        title="Alfred's Wordle Game Guide",
        description="Greetings, dear guests. I, Alfred Pennyworth, shall guide you through the captivating Wordle game.",
        color=nextcord.Color.green()
    )

    # Add fields to the embed
    embed.add_field(name="How to Play:", value="1. Use the command `/play` to start the game.\n2. Guess words that start with the last letter of the previous word.\n3. Be strategic and expand your vocabulary.\n4. The game ends when a player cannot provide a valid word. The player with the most valid words wins.")

    # Add footer to the embed
    embed.set_footer(text="Enjoy the game and happy word guessing! - Alfred Pennyworth")

    # Send the embed message
    await lobby.send(embed=embed)
    await lobby.send(author.mention + 'New lobby has been created. Invite your opponent to this channel!')
    async def get_ready(player_name):
      await lobby.send(player_name + " type ready")

      def check(m):
        return m.content.lower() == 'ready'

      msg = await self.client.wait_for('message', check=check)
      return msg.author

    p1 = await get_ready("Player 1")
    if not p1:
      print("Error")
      return 
    p2 = await get_ready("Player 2")
    await lobby.send(p1.mention + " Vs " + p2.mention)

    used_words = set({})
    curr_word = ''
    prev_word = ''
    game_over = False
    players = [p1, p2]
    turn = 0

    while not game_over:
      curr_player = players[turn % 2]
      await lobby.send(curr_player.mention + "'s Word: ")

      def check(m):
        return m.author == curr_player

      word = await self.client.wait_for('message', check=check)
      prev_word = curr_word
      curr_word = word.content

      if not self.valid_word(prev_word, curr_word, turn, used_words):
        await lobby.send(curr_player.mention + " Lost! " + players[(turn + 1) % 2].mention + " Wins🎉🎉")
        await lobby.send('This lobby will be delete in 15 seconds')
        game_over = True
        await asyncio.sleep(15)
        await lobby.delete()
        break
      else:
        turn += 1

  async def vsai(self, ctx: Interaction):
    curr_word = ''
    prev_word = ''
    turn = 0
    used_words = set({})
    game_over = False
    author = ctx.user
    guild = ctx.guild
    category = nextcord.utils.get(guild.categories, name='Lobbies')
    lobby_id = random.randint(36, 10000)
    lobby = await guild.create_text_channel('vsai-lobby-id--'+ str(lobby_id), category=category)
    await lobby.send('New Lobby created!')
    embed = nextcord.Embed(
        title="Alfred's Wordle Game Guide",
        description="Greetings, dear guests. I, Alfred Pennyworth, shall guide you through the captivating Wordle game.",
        color=nextcord.Color.green()  # Choose a color for the embed
    )

    # Add fields to the embed
    embed.add_field(name="How to Play:", value="1. Use the command `/play` to start the game.\n2. Guess words that start with the last letter of the previous word.\n3. Be strategic and expand your vocabulary.\n4. The game ends when a player cannot provide a valid word. The player with the most valid words wins.")

    # Add footer to the embed
    embed.set_footer(text="Enjoy the game and happy word guessing! - Alfred Pennyworth")

    # Send the embed message
    await lobby.send(embed=embed)
    await lobby.send('Type your first word')
    
    while not game_over:
      if turn % 2 != 0:
        
        ai_word = self.get_word(prev_word, curr_word, turn, used_words)
        prev_word = curr_word
        curr_word = ai_word
        await lobby.send(curr_word)
        if not self.valid_word(prev_word, curr_word, turn, used_words):
          await lobby.send('You beat the AI!!')
          await lobby.send('This lobby will be deleted in 15 seconds.')
          game_over = True
          await asyncio.sleep(15)
          await lobby.delete()
          break 
        else:
          turn += 1
          
      else:  
        def check(m):
          return m.author == author
        word = await self.client.wait_for('message', check=check)
        prev_word = curr_word
        curr_word = word.content
        if not self.valid_word(prev_word, curr_word, turn, used_words):
          await lobby.send('You Lost!')
          await lobby.send('This lobby will be deleted in 15 seconds.')
          game_over = True
          await asyncio.sleep(15)
          await lobby.delete()
          break
        else:
          turn += 1

class GameMode(nextcord.ui.View):
  def __init__(self, client):
    super().__init__()
    self.value = None
    self.client = client

  @nextcord.ui.button(label='PvP', style=nextcord.ButtonStyle.green)
  async def pvp(self, button: nextcord.ui.Button, ctx: Interaction):
    await ctx.response.send_message('PvP it is!', ephemeral=True)
    await GameCog(self.client).pvp(ctx)
    self.value = True
    self.stop()

  @nextcord.ui.button(label='vs AI', style=nextcord.ButtonStyle.red)
  async def vsai(self, button: nextcord.ui.Button, ctx: Interaction):
    await ctx.response.send_message("You shall play against Alfred himself! Do not worry he will go easy on you.", ephemeral=True)
    await GameCog(self.client).vsai(ctx)
    self.value = False
    self.stop()

class UI(commands.Cog):
  def __init__(self, client):
    self.client = client

  @nextcord.slash_command(name='play', description='Play a Game!')
  async def play(self, ctx: Interaction):
    view = GameMode(self.client)
    await ctx.response.send_message('Which mode would you like to play?', view=view, ephemeral=True)
    await view.wait()

def setup(client):
  client.add_cog(UI(client))