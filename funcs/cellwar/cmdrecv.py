from discord.message import Message as Msg
from discord import Client
from typing_extensions import Self
from typing import Tuple, List, Callable, Coroutine, Any, Dict

from . import local_parser

TIMEOUT = 60

class CmdRecv:
    def __init__(self, bot, ctx):
        self.marks = []
        self.bot = bot
        self.ctx = ctx

    def log(self, m: str):
        print("[CmdRecv] "+m)
        pass
        
    def add(self,key: str, asy_callback) -> Self:
        print()
        self.log("add()")
        self.log(f"...key: {key}")
        self.log(f"...call: {asy_callback.__name__}")
        self.marks.append(
            (key, asy_callback)
        )
        return self
        
    def add_plain(self, key: str) -> Self:
        print()
        self.log("add_plain()")
        self.log(f"...cond: {key}")
        self.log("...call: None")
        self.marks.append(
            (key, None)
        )
        return self
    
    @classmethod
    def copy(cls,sample) -> Self:
        product = cls(sample.bot, sample.ctx)
        for react_set in sample.marks:
            product.add(
                react_set[0],react_set[1]
            )
        return product

    def dup (self) -> Self:
        return self.copy(self)

    def get_checks(self,m:Msg) -> bool:
        print()
        try:
            print("?")
            instruction = local_parser.parse(m.content)
        except local_parser.IllegalInstruction as e:
            self.log(str(e))
            return False
        self.log("get_checks() called")
        for react_set in self.marks:
            self.log(f"...checking: {react_set[0]}")
            if instruction["command"] == react_set[0]:
                self.log("get_checks() returned -> True")
                return True
        self.log("get_checks() returned -> False")
        return False
        
    async def wait_for_msg(self, timeout=TIMEOUT) -> Dict:
        print()
        self.log("wait_for_msg() called")
        msg: Msg = await self.bot.wait_for(
            "message",
            check=self.get_checks,
            timeout=timeout
        )
        self.log(f'...got "{msg.content}"')
        self.log("wait_for_msg() complete")
        cmd = local_parser.parse(msg.content)
        cmd["author_id"] = msg.author.id
        cmd["channel_id"] = msg.channel.id
        return cmd

    async def react(self, cmd: Dict) -> None:
        print()
        self.log("react() called")
        
        for react_set in self.marks:
            if react_set[0] != cmd["command"]:
                continue
            self.log(f"...checking callback of {react_set[0]}")
            self.log(f"...callback's type: {type(react_set[1]).__name__}")
            if react_set[1] is not None:
                self.log(f"...executing {react_set[1].__name__}")
                await react_set[1](cmd)
        self.log("react() complete")
        
    async def work(self,timeout=TIMEOUT) -> Dict:
        print()
        self.log("work() called")
        cmd: Dict = await self.wait_for_msg(timeout)
        await self.react(cmd)
        self.log("work() complete")
        return cmd
        
    async def dispose(self, key: str, callback: Callable[[Msg], Coroutine[Any, Any, Any]], timeout=TIMEOUT) -> Dict:
        print()
        self.log("dispose() called")
        cmd = await self.dup().add(key, callback).work(timeout)
        self.log("dispose() complete")
        print()
        return cmd
        
    async def dispose_plain(self, key: str, timeout=TIMEOUT) -> Dict:
        self.log("dispose() called")
        cmd = await self.dup().add_plain(key).work(timeout)
        self.log("dispose() complete")
        return cmd