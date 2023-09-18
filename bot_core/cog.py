import discord
from discord.ext import commands
from discord.message import Message as Msg
from typing_extensions import Self

from bot_core.receiver import Receiver
from bot_core.signals import ExitSignal




class Cog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot