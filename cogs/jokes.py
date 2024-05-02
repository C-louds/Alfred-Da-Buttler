import nextcord
from nextcord import Interaction 
from nextcord.ext import commands
from jokeapi import Jokes
import random
import asyncio

class Happy(commands.Cog):
  def __init__(self, client):
    self.client = client

  async def get_jokes(self, category, input, amount):
    j = await Jokes()
    joke = await j.get_joke(response_format = 'txt', category = category, search_string = input, amount=amount)
    if joke is None:
      joke = "Bruh."
    return joke
  @nextcord.slash_command(name='hearjokes', description="You will laugh unless you don't want to.")
  async def hearjokes(self, ctx: Interaction, amount: int):
    author = ctx.user
    category = []
    input = ''
    await ctx.response.send_message('Wanna hear a Joke?', ephemeral=True)
    await ctx.followup.send("Here's the menu: \nDark: Everyone likes dark jokes but not the people. \nMisc: Feeling lucky? \nPun: Don't worry this bot isn't a Dad yet. \nProgramming: Miss me with that nerd shit. \nRandom: Or perhaps leave it to odds?", ephemeral=True)
    def check(m):
      return m.author == author
      
    msg = await self.client.wait_for('message', check=check)
    type = msg.content.lower()
    if type != 'random':
      category.append(type)
    else:
      category = []
    joke = await self.get_jokes(category, input, amount)

    await ctx.send(joke)

def setup(client):
  client.add_cog(Happy(client))