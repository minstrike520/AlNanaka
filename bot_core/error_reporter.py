from discord import Client
from config import get_config
from traceback import format_exc

ERR_MSG_CH_ID = get_config("error_channel")

async def log(bot: Client, m: str):
    ch = bot.get_channel(ERR_MSG_CH_ID)
    await ch.send(m)


async def report_specific(bot: Client, e: Exception):
    #print(f"[{type(e).__name__}] {str(e)}")
    
    await log(bot,f"[{type(e).__name__}] {str(e)}")
    
async def report_traceback(bot: Client):
    print("[ErrRep] traceback()")
    ch = bot.get_channel(ERR_MSG_CH_ID)
    await log(bot,f"```{format_exc()}```")
    
    