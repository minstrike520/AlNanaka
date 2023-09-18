from discord.message import Message as Msg
from typing_extensions import Self
from typing import Tuple, List, Callable, Coroutine, Any

TIMEOUT = 60

class Receiver:
    def __init__(self, bot, ctx):
        self.marks = []
        self.bot = bot
        self.ctx = ctx

    def log(self, m: str):
        print("[Receiver] "+m)
        pass
        
    def add(self,cond, asy_callback) -> Self:
        print()
        self.log("add()")
        self.log(f"...cond: {cond.__name__}")
        self.log(f"...call: {asy_callback.__name__}")
        self.marks.append(
            (cond, asy_callback)
        )
        return self
        
    def add_plain(self,cond: Callable) -> Self:
        print()
        self.log("add_plain()")
        self.log(f"...cond: {cond.__name__}")
        self.log("...call: None")
        self.marks.append(
            (cond, None)
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
        self.log("get_checks() called")
        for react_set in self.marks:
            self.log(f"...checking: {react_set[0].__name__}")
            if react_set[0](m):
                self.log("get_checks() returned -> True")
                return True
        self.log("get_checks() returned -> False")
        return False
        
    async def get_msg(self, timeout=TIMEOUT) -> Msg:
        print()
        self.log("get_msg() called")
        msg = await self.bot.wait_for(
            "message",
            check=self.get_checks,
            timeout=timeout
        )
        self.log(f'...got "{msg.content}"')
        self.log("get_msg() complete")
        return msg

    async def react(self,m: Msg) -> None:
        print()
        self.log("react() called")
        async def mock_f():
            pass
        
        for react_set in self.marks:
            if not react_set[0](m):
                continue
            self.log(f"...checking callback of {react_set[0].__name__}")
            self.log(f"...callback's type: {type(react_set[1]).__name__}")
            if react_set[1] is not None:
                self.log(f"...executing {react_set[1].__name__}")
                await react_set[1](m)
        self.log("react() complete")
        
    async def work(self,timeout=TIMEOUT) -> Msg:
        print()
        self.log("work() called")
        msg: Msg = await self.get_msg(timeout)
        await self.react(msg)
        self.log("work() complete")
        return msg
        
    async def dispose(self, cond: Callable[[Msg], bool], callback: Callable[[Msg], Coroutine[Any, Any, Any]], timeout=TIMEOUT) -> Msg:
        print()
        self.log("dispose() called")
        msg = await self.dup().add(cond,callback).work(timeout)
        self.log("dispose() complete")
        print()
        return msg
        
    async def dispose_plain(self, cond: Callable, timeout=TIMEOUT) -> Msg:
        self.log("dispose() called")
        msg = await self.dup().add_plain(cond).work(timeout)
        self.log("dispose() complete")
        return msg