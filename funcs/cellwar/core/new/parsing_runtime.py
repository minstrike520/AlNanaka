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
    # err
    "/init",
    # ok
    "/newc",
    # ok
    "/newc",
    # ok
    "/newc",
    # ok
    "/start",
    # ok
    # process
    # now char: ...
    "/move -c 1"
    )
    for inp in inpset:
        resls = r.inp(inp)
        print(resls)
        
if __name__ == '__main__':
    main()