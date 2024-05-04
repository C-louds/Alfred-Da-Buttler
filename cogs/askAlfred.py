import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import requests
import json


class askAlfred(commands.Cog):

  def __innit__(self, client):
    self.client = client

  def search_result(self, query):
    url = "https://duckduckgo-duckduckgo-zero-click-info.p.rapidapi.com/"
    querystring = {
        "q": query,
        "no_html": "1",
        "no_redirect": "1",
        "skip_disambig": "1",
        "format": "json"
    }
    headers = {
        "X-RapidAPI-Key": "1f176a2d30msh6791931ee4acabcp142ab5jsn903e988f12a7",
        "X-RapidAPI-Host":
        "duckduckgo-duckduckgo-zero-click-info.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    result = response.json()['Abstract']
    #print(response.json())
    #print(result)
    return result

  @nextcord.slash_command(
      name='alfred',
      description=
      "Keep your queries short & ask Alfred your question & he will try to answer according to how we are paying him :/"
  )
  async def alfred(self, ctx: Interaction, query):
    result = self.search_result(query)
    if result:
      await ctx.response.send_message(result)
    else:
      await ctx.response.send_message("I don't get paid enough for this.")

def setup(client):
  client.add_cog(askAlfred(client))
