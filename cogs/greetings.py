import nextcord
from nextcord.ext import commands
from nextcord import Interaction


class Greetings(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_member_join(self, member):
    welcome_message = f"Welcome to the server, {member.mention}!"

    channel = self.client.get_channel(name="general")
    if channel:
      await channel.send(welcome_message)

  @nextcord.slash_command(name='hey', description='Say Hey!')
  async def hey(self, ctx: Interaction):
    await ctx.response.send_message(
        'I have your Greetings! Perhaps may I be of any use to you? You shall use commands for my services.'
    )


def setup(client):
  client.add_cog(Greetings(client))
