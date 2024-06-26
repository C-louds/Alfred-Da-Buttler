import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from jokeapi import Jokes
import random
import asyncio
import requests


class Happy(commands.Cog):

  def __init__(self, client):
    self.client = client
    self.is_joke = False

  async def get_jokes(self, category, input, amount):
    j = await Jokes()
    joke = await j.get_joke(response_format='txt',
                            category=category,
                            search_string=input,
                            amount=amount)
    if joke is None:
      joke = "Bruh."
    return joke

  async def get_insult(self, amount):
    req_amount = []
    while len(req_amount) < amount:
      n = random.randint(0, 1)
      if n == 0:
        api_url = "https://evilinsult.com/generate_insult.php?lang=en&type=json"
      else:
        api_url = 'https://www.yomama-jokes.com/api/v1/jokes/random/'
      response = requests.get(api_url)
      if n == 0:
        insult = response.json()['insult']
        req_amount.append(insult)
      else:
        insult = response.json()['joke']
        req_amount.append(insult)
    #print(insult)
    return req_amount

  @nextcord.slash_command(
      name='hearjokes', description="You will laugh unless you don't want to.")
  async def hearjokes(self, ctx: Interaction, amount: int):
    author = ctx.user
    category = []
    input = ''

    embed = nextcord.Embed(
        title='Would it be a joke or an insult?',
        description='Cheer up your mood or worsen it. Up to you!',
        color=nextcord.Color.dark_purple())
    embed.add_field(
        name='Menu:',
        value=
        "Dark: Everyone likes dark jokes but not the people. \nMisc: Feeling lucky? \nPun: Don't worry this bot isn't a Dad yet. \nProgramming: Miss me with that nerd shit. \nInsult: I shall do as asked. \nRandom: Or perhaps leave it to odds?"
    )
    await ctx.response.send_message('Wanna hear a Joke?',
                                    embed=embed,
                                    ephemeral=True)

    def check(m):
      return m.author == author

    msg = await self.client.wait_for('message', check=check)
    type = msg.content.lower()
    if type not in ['insult', 'random']:
      category.append(type)
      self.is_joke = True
    elif type == 'insult':
      self.is_joke = False
    else:
      category = []
      num = random.randint(0,1)
      if num == 0:
        self.is_joke = True
      else:
        self.is_joke = False
    
    if self.is_joke:
      joke = await self.get_jokes(category, input, amount)
      await ctx.send(joke)
    else:
      insult = ""
      insults = []
      insults = await self.get_insult(amount)
      if insults:
        for i in range(len(insults)):
            insult += insults[i]
            if i != amount - 1:
              insult += "\n\n-------------------------------------\n\n"
      await ctx.send(insult)

def setup(client):
  client.add_cog(Happy(client))
