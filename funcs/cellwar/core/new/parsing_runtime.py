from ... import local_parser


class IllegalOperation(Exception):
    def __init__(self, di):
        super().__init__()
        self.detail = di

class Runtime:
    def __init__(self):
        pass
    def init(self, cmd):
        pass

    def newc(self, cmd):
        pass

    def start(self, cmd):
        pass

    def move(self, cmd):
        pass

    def inp(self,s):
        try:
            cmd = local_parser.parse(s)
        except local_parser.IllegalInstruction as err:
            return ("none", {
            "detail": str(err)
            }
            )
        try:
            if cmd["command"] == "init":
                self.init(cmd)
            elif cmd["command"] == "newc":
                self.newc(cmd)
            elif cmd["command"] == "start":
                self.start(cmd)
            elif cmd["command"] == "move":
                self.move(cmd)
            else:
                return ("none", {
                    "inp": cmd})
        except IllegalOperation as err:
            return ("err", err.detail)

        return "ok", {"inp": cmd}


def main():
    r = Runtime()
    inpset = (
        "/jti",
        # none
        "/start nfowkg",
        # err: `start` in inappropriate timing
        "/init -client_id 123 -board_size ASQT",
        # err: argument with inaprropriate input
            # argument: board_size
            # input value: ASQT
            # input should be: a number
        "/init -client_id 123 -board_size 10",
        # ok
        "/newc -client_id 123 -name A -char_career base -team_id 1 -pos_r 11 -pos_c 2",
        # err: out of bounds
            # the position: (11, 2)
        "/newc -client_id 123 -name A -char_career base -team_id 1 -pos_r 5 -pos_c 2",
        # ok
        "/newc -client_id 123 -name A -char_career base -team_id 1 -pos_r 5 -pos_c 2",
        # err: there's already a char with the same name
            # the char: A
        "/newc -client_id 123 -name B -char_career base -team_id 1 -pos_r 5 -pos_c 2",
        # err: in the position is already a char
            # the position: (5, 2)
            # the char there: A
        "/newc -client_id 123 -name B -char_career base -team_id 1 -pos_r 2 -pos_c 2",
        # ok
        "/newc -client_id 456 -name C -char_career base -team_id 2 -pos_r 3 -pos_c 5",
        # ok
        "/newc -client_id 456 -name D -char_career base -team_id 2 -pos_r 4 -pos_c 1",
        # ok
        "/start",
        # ok
            # char going to do turn: A
            # initial_determination: passed
            # waiting for char's `move`
        "/move -client_id 456 -char B -pos_r 11 -pos_c 2"
        # err: no permission to controll the char
            # one who has the permission: find_owner_of_char(B) -> 123
        "/move -client_id 123 -char B -pos_r 11 -pos_c 2"
        # err: not the char's turn
        "/move -client_id 123 -char A -pos_r 11 -pos_c 2",
        # err: out of bounds
            # bounds: (0,0) to (10,10)
        "/move -client_id 123 -char A -pos_r 9 -pos_c 9",
        # err: out of char's move range
            # char's move range: char.MV -> 6
        "/move -client_id 123 -char A -pos_r 3 -pos_c 5",
        # err: in the position is already a char
            # the position: (11, 2)
            # the char there: C
        "/move -client_id 123 -char A -pos_r 3 -pos_c 4",        
        # ok
            # waiting for char's `skill casting`
        "/skill -client_id 123 -char A -skill_name attack -target_id B"
        # err: can't cast offensive spells to a teammate
            # skill_name: attack
            # team_id: 1
            # target char: B
        "/skill -client_id 123 -char A -skill_name attack -target_id D",
        # err: distance to the destination (or to the target) out of the skill's casting range
            # the skill_name: attack
            # the skill's casting range: 1 
                # **range here is different from the moving one;
                # **moving one is grid distance; the casting one is linear distance
            # now position: A.pos -> (3,4)
            # casting destination: D.pos -> (4,1)
            # distance: |D.pos - A.pos| -> |(1, -3)| = 316 / 100
        "/skill -client_id 123 -char A -skill_name attack -target_id C"
        # ok
    )
    for inp in inpset:
        resls = r.inp(inp)
        print(resls)
        
if __name__ == '__main__':
    main()