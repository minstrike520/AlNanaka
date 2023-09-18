from asyncio import TimeoutError

import discord
from discord import Message as Msg
from discord import Client
from discord.ext import commands
from discord.ext.commands.context import Context

from bot_core.cog import Cog
from bot_core.error_reporter import report_traceback
from funcs.cellwar.cmdrecv import CmdRecv
from bot_core.signals import ExitSignal
from funcs.cellwar.core.parsing_runtime import Runtime
from config import get_config


def exit_cond(m: Msg):
    return m.content == "!exit"
def exit_callback(m):
    raise ExitSignal


ERR_MSG_CH_ID = get_config("err_msg_ch_id")

class CellWarCons(Cog):
    def __init__(self,bot: Client):
        self.bot = bot
        
    @commands.command()
    async def cwcons(self, ctx: Context):
        print("Command called: _cwcons")
        recv = CmdRecv(self.bot, ctx).add("exit", exit_callback)
        runtime = Runtime(self, ctx, self.bot, recv)
        try:
            await runtime.launch()
            await ctx.send("Game Terminated without signals")
        except ExitSignal:
            await ctx.send("Game Exited.")  
        except TimeoutError:
            await ctx.send("No Valid Input For Too Long, Game Exited Automatically.") 
        except Exception:
            await ctx.send("WARN: Unknown error occurred and caused game to terminate.")
            await report_traceback(self.bot)
                       

async def setup(bot):
    await bot.add_cog(CellWarCons(bot))