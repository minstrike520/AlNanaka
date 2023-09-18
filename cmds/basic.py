import discord
from discord.ext import commands
from bot_core.cog import Cog

class Basic(Cog):
    def _init_(self,bot):
        self.bot = bot
    @commands.command() #ping
    async def ping(self, ctx):
        await ctx.send(f'{round(self.bot.latency*1000)} ms')

async def setup(bot):
    await bot.add_cog(Basic(bot)) 