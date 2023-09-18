import discord
from discord.ext import commands
import json
import os
import asyncio
from bot_core.keep_alive import keep_alive
from config import get_config



READY_CHANNEL_ID: int = get_config("ready_channel")
''''''
intents=discord.Intents().all()
bot = commands.Bot(command_prefix='_',intents=intents,owner_ids=get_config("owners"))

@bot.event #online
async def on_ready(): 
  channel = bot.get_channel(READY_CHANNEL_ID)
  await channel.send('已上線')
  print('**al_nanaka is currently online!')

@bot.command()
async def load(ctx,extension):
  try:
    await bot.load_extension(f'cmds.{extension}')
    await ctx.send(f'{extension}擴展加載成功.')
  except:
    print('An exception occurred! Cannot load.')
    await ctx.send("加載失敗!")

@bot.command()
async def unload(ctx,extension):
  try:
    await bot.unload_extension(f'cmds.{extension}')
    await ctx.send(f'{extension}擴展卸載成功.')
  except:
    print('An exception occurred! Cannot unload.')
    await ctx.send("卸載失敗!")

@bot.command()
async def reload(ctx,extension):
  try:
    await bot.reload_extension(f'cmds.{extension}')
    await ctx.send(f'已將{extension}擴展重新導入.')
  except:
    print('An exception occurred! Cannot reload.')
    await ctx.send("導入失敗!")

async def load_extensions():
    for filename in os.listdir("./cmds"):
        if filename.endswith(".py"):
            print(filename)
            # cut off the .py from the file name
            await bot.load_extension(f"cmds.{filename[:-3]}")

#if "__name__" == "__main__":
  #bot.run(data["token"])

async def main():
    async with bot:
        keep_alive()
        await load_extensions()
        await bot.start(os.environ["TOKEN"])

asyncio.run(main())