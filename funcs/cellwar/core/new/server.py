from asyncio import TimeoutError
from collections.abc import Callable
from typing import Dict, Set, Tuple

from discord import Client, Member, User
from discord.ext.commands.cog import Cog
from discord.ext.commands.context import Context
from discord.message import Message as Msg

from bot_core.error_reporter import log
from ..cmdrecv import CmdRecv
from bot_core.signals import InvalidInput, OutOfBounds, Proceed
from config import get_config
from funcs.tools import is_intstr

from .. import local_parser, prompts
from .core import BoardVector, Character
from .parsing_stage import Stage

BOARD_MAX_SQUARE_SIZE = get_config("board_max_square_size", "cw")


class Player:
    def __init__(self, client: Member|User, belonging_chars: Set[Character]):
        self.client = client
        self.belonging_chars = belonging_chars


class PlayerManager(set):
    class PlayerAlreadyIn(Exception):
        def __init__(self, client_id: int):
            super().__init__(f"The client {client_id} has already in")
    
    def __init__(self, se: Set[Player]):
        super().__init__(se)

    def add(self, player: Player):
        for p in self:
            if p.client.id == player.client.id:
                raise self.PlayerAlreadyIn(player.client.id)
        super().add(player)

    def add_by_client(self, client: Member|User):
        self.add(Player(client, set()))

    def find_by_client_id(self, client_id: int):
        for p in self:
            if p.client.id == client_id:
                return p
        raise IndexError

class Runtime:
    def __init__(self, cog: Cog, ctx: Context, bot: Client, cmdrecv: CmdRecv):
        self.cog = cog
        self.ctx = ctx
        self.bot: Client = bot
        self.cmdrecv = cmdrecv
        self.players = PlayerManager(set())
        
        self.player_joinable = False
        self.allow_new_char = False

    async def asylog(self, m: str):
        await log(self.ctx.bot, "`[CW.Runtime]\n"+m+"`")
    
    def log(self, m: str):
        print("[CW.Runtime] "+m)
        pass
    
    async def prompt(self, key: str):
        await self.ctx.send(prompts.get(key))
        print(f"[CW.Prompt] {key}")

    #----------------------
  
    async def dev_test(self):
        await self.ctx.send("dev test")
        #self.stage.chars[0].actefs.append_by_name("freeze")

    async def exec_turn(self):
        await self.ctx.send(
            "turn exec"
        )
        char = None
        async def init_determine(self):
            char
            await self.ctx.send(
                "init determine"
            )
        await init_determine(self)

        async def move(self):
            await self.ctx.send(
                "move"
            )
    
    async def launch(self):
        await self.ctx.send(
            "parsing runtime launched"
        )

        async def init_stage(self):
            c = await self.cmdrecv.dispose_plain(
                    "init_stage"
                )
            board_size = c["size"]
            await self.ctx.send(f"You've set the stage's board to {board_size} x {board_size}!")
            self.stage = Stage(BoardVector.square(board_size))
            
        i = 0
        while True:
            try:
                await init_stage(self)
                break
            except KeyError as err:
                i += 1
                if i >= 3:
                    raise TimeoutError from err
        await self.prompt("waiting_for_start_instruction")

        async def start(self, _cmd):
            await self.ctx.send("Started!")

        i = 0
        while True:
            try:
                cmd = await self.cmdrecv.dispose_plain(
            "start"
            )
                await start(self, cmd)
                
            except TimeoutError as err:
                i += 1
                if i >= 3:
                    raise TimeoutError from err
        


#for debugging
class SessionTester:
    pass    

'''
class Turn:
    @staticmethod
    async def exec(runtime: Runtime,char):
        from ..assets import special_status
        await runtime.ctx.send(f"=====| {char.name}'s turn |====")
        
        try:
            runtime.stage.initial_determine(char)

            new_pos_data = await runtime.CharMoveRequirement.attempt(runtime, char)
            runtime.stage.move(char, new_pos_data)
            
            await runtime.SkillCasting.attempt(runtime, char)
            
            runtime.stage.ending_determine(char)

        
        except special_status.Freezed:
            await runtime.ctx.send(f"{char.name} is freezed...")
            
        await runtime.ctx.send(f"====| End of {char.name}'s turn |====")
        return


class CommandParser:
    @staticmethod
    def basic(cmd_key: str, input_msg: Msg):
        return input_msg.content[len(cmd_key)+1:]
        

class InputParser:
    @staticmethod
    def new_char(new_char_input: str):
        char_career, team_id_str = new_char_input.split(" ")
        return char_career, team_id_str
    
    @staticmethod
    def size(size_input: str):
        if not is_intstr(size_input):
            raise InvalidInput
        if int(size_input) < 1 or int(size_input) >= BOARD_MAX_SQUARE_SIZE:
            raise OutOfBounds
        return int(size_input)
    
    @staticmethod
    def movement(move_input: str):
        move_input.split(",")
        if len(move_input)  != 2:
            raise InvalidInput
        if( (not is_intstr(move_input[0]) ) or (not is_intstr(move_input[1]))):
            raise InvalidInput
        r = int(move_input[1])
        c = int(move_input[0])
        return r, c
'''





"/create_stage -size 10 -admin_id 13868791835798"


'''
class CharRegistration:
    class InvalidName(Exception):
        pass

    @staticmethod
    async def get_parse_check_char_data(runtime: Runtime):
        input_str = await CtxCommandReceiver.get_input_str(runtime.recv, "!new_char")
        new_char_data = InputParser.new_char(input_str)
        char_career, team_id_str = new_char_data
        runtime.log(f"Got char_career input: {char_career}, team id = {team_id_str}")
        runtime.stage.InputValidityChecker.char_data(char_career, team_id_str)
        return char_career, team_id_str
    
    @staticmethod
    def name_censor(name):
        if name[0] == "!":
            raise CharRegistration.InvalidName

    @staticmethod
    async def get_char_name(recv: Receiver, m: Msg):
        name_input = await recv.dispose_plain(
            lambda m2: m2.author == m.author
        )
        return name_input.content

    @staticmethod
    async def name_input_loop(runtime: Runtime, m: Msg):
        while True:
            try:
                name = await CharRegistration.get_char_name(runtime.recv, m)
                CharRegistration.name_censor(name)
            except CharRegistration.InvalidName:
                await runtime.ctx.send("The name is not valid, Try again!")
                continue
    
    @staticmethod
    async def new_char(runtime: Runtime, m: Msg):
        try:
            char_career, team_id_str = await CharRegistration.get_parse_check_char_data(runtime)
            
            await runtime.ctx.send("How would you call your character? Give it a name!")
            name = await CharRegistration.name_input_loop(runtime, m)
            await runtime.ctx.send(f'We call your character {name} now!')
            runtime.stage.chars.add( 
                Character.create_by_career(
                    char_career,
                    name, 
                    int(team_id_str)
                )
            )
            await runtime.ctx.send(f"You've added {name} in type `{char_career}` and in team `{team_id_str}`!")
        
        except runtime.stage.InputValidityChecker.NoSuchCareer as char_career:
            await runtime.ctx.send(f"No such career like {char_career}! Here's all careers for selection:")
            all_careers = get_config("careers","cw")
            await runtime.ctx.send(f"{all_careers}")
        except runtime.stage.InputValidityChecker.TeamIDMustBeNumber:
            await runtime.prompt("team_id_must_be_number")

    @staticmethod
    def is_new_char_msg(m: Msg) -> bool:
        return m.content[:9] == "!new_char" and len(m.content) > 9
    
    @staticmethod
    def enable(runtime: Runtime):
        if not runtime.allow_new_char:
            runtime.allow_new_char = True
            runtime.recv.add(
                CharRegistration.is_new_char_msg,
                lambda m: CharRegistration.new_char(runtime,m)
            )
        else:
            raise Exception("Receiver.remove(): Haven't implemented this yet!") 

    
class CharMoveRequirement:
    @staticmethod
    async def attempt(runtime: Runtime, char: Character) -> Dict[str, int]:
        while True:
            try:
                await runtime.prompt("require_move")
                move_input = await CtxCommandReceiver.get_input_str(
                    runtime.recv,
                    "!move",
                    runtime.bot.get_user(char.owner_id)
                )
                new_pos_data = InputParser.movement(move_input)
                r, c = new_pos_data
                await runtime.ctx.send(f"{char.name} has moved to ({c},{r})!")
                return {
                    "r": r,
                    "c": c
                }
                
            except InvalidInput:
                await runtime.prompt("require_move_!valid")
                continue
            except OutOfBounds:
                await runtime.prompt("require_move_!valid::out_of_bounds")
                continue
            except Character.MoveBeyondMV:
                await runtime.prompt("require_move_!valid::beyond_mv")
                continue
            except runtime.stage.TileOccupied:
                await runtime.prompt("require_move_!valid::tile_occupied")
                continue
            except TimeoutError:
                await runtime.prompt("still_waiting_for_input")
                continue


class SkillCasting:
    class InvalidArguments(Exception):
        def __init__(self, err_msg):
                super().__init__(err_msg)

    class NotBelongToChar(Exception):
        pass

    class CannotSelectSelf(Exception):
        pass

    class CannotSelectSameTeam(Exception):
        pass

    @staticmethod
    def parse_name_input(input_str: str, skill_data, char):
        skill_name = input_str
        if skill_name not in skill_data.get_skill_names():
            raise skill_data.NoSuchSkill
        if skill_name not in char.skills:
            raise SkillCasting.NotBelongToChar
        return skill_name

    @staticmethod
    async def waitfor_name_input(runtime: Runtime, char: Character) -> str:
        await runtime.prompt("require_skill")
        input_msg = await runtime.recv.dispose_plain(lambda m: m.content [:6] == "!skill")
        skill_name = SkillCasting.parse_name_input(
            input_msg.content[7:],
            runtime.stage.skill_data,
            char
        )
        runtime.log(f"skill name input: {skill_name}")
        return skill_name
        
        

    @staticmethod
    async def select_target(runtime: Runtime):
        select_input = await runtime.recv.dispose_plain(lambda m: m.content[:2]=="!t")
        selection = select_input.content[3:]
        return selection
        
    
    @staticmethod
    async def select_an_enemy(runtime: Runtime, char: Character):
        await runtime.prompt("require_skill::waitfor_not_my_team")
        selection = await SkillCasting.select_target(runtime)
        selected_char = runtime.stage.chars.by_name(selection)
        
        if char == selected_char:
            raise SkillCasting.CannotSelectSelf
        if char.is_same_team(selected_char):
            raise SkillCasting.CannotSelectSameTeam
        return selected_char


    @staticmethod
    async def name_input_loop(runtime: Runtime, char: Character):
        while True:
            try:
                skill_name = await SkillCasting.waitfor_name_input(runtime, char)
                return skill_name

            except InvalidInput:
                await runtime.prompt("require_skill!valid")
                continue
                
            except runtime.stage.skill_data.NoSuchSkill:
                await runtime.prompt("require_skill!valid::no_such_skill")
                continue
                
            except SkillCasting.NotBelongToChar:
                await runtime.prompt("require_skill!valid::not_belong_to_char")
                continue
                

    @staticmethod
    async def cast_loop(runtime: Runtime, char: Character, skill_name: str):
        while True:
            try:
                skill = runtime.stage.skill_data.get_skill(skill_name)
                
                if skill["select_type"] == "enemy":
                    target_char = await SkillCasting.select_an_enemy(runtime, char)
                    skill["func"](char, target_char)
                    await runtime.ctx.send(f"{char.name} casted `{skill_name}` to {target_char.name}!!")
                    
                elif skill["select_type"] == "none":
                    skill["func"](char)
                    await runtime.ctx.send(f"{char.name} casted `{skill_name}`!!")
                
                else:
                    raise KeyError
                    
                break

            except SkillCasting.CannotSelectSameTeam:
                await runtime.prompt("require_skill!valid::cannot_select_same_team")
                continue
                
            except SkillCasting.CannotSelectSelf:
                await runtime.prompt("require_skill!valid::cannot_select_self")
                continue

            except KeyError:
                await runtime.prompt("require_skill!valid::no_such_char")
            
    
    @staticmethod
    async def attempt(runtime: Runtime, char: Character):
        skill_name = await SkillCasting.name_input_loop(runtime, char)
        await SkillCasting.cast_loop(runtime, char, skill_name)
        '''