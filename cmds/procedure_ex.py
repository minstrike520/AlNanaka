import discord
from discord.ext import commands

from bot_core.cog import Cog, Receiver
from bot_core.signals import ExitSignal

#from src.tools import is_intstr

async def do_test(ctx):
    await ctx.send("Program Showcase!")

async def loop_test(cog,ctx,recv:Receiver):
    def c1(m):
        return m.content == "1"
    def c2(m):
        return m.content == "2"
    async def fp(m):
        print(m.content)
        await ctx.send(m.content)
        return

    #c1
    await recv.dispose(c1,fp)
    '''
    both pieces of code of res1 and res2 actually works the same. 
    I simplified one of res2 to one of res1.
    '''
    #c2
    res2 = await recv.dup() \
                     .add(c2,None) \
                     .work()
    await ctx.send(res2.content)
    
             

class Test(Cog):
    def _init_(self,bot):
        self.bot = bot
    @commands.command()
    async def progt(self,ctx):
        await do_test(ctx)
        receiver = Receiver.copy(
            self.get_basic_recv(self.bot)
        )
        try:
            print("a1")
            while True:
                print("a2")
                await loop_test(self,ctx, receiver)
                print("a10")
        except ExitSignal:
            await ctx.send("Terminated!")
            


    
async def setup(bot):
    await bot.add_cog(Test(bot))