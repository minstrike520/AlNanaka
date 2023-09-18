
COMMAND_INDICATOR = "/"
PARAMETER_INDICATOR = "-"

def spaces(amount):
    s = ""
    for i in range(amount):
        s += " "
    return s

def combine(li):
    s = ""
    for item in li:
        s += item+" "
    return s


class IllegalInstruction(Exception):
    def __init__(self, err_msg, inp, position):
        super().__init__(
            f"{err_msg}\n....{inp}\n....{spaces(position)}^"
        )
    pass


def parse(s):
    from string import ascii_lowercase
    LEGAL_CHARACTER = list(ascii_lowercase) + [str(i) for i in range(0,10)]
    li = s.split(" ")
    if li[0][0] != COMMAND_INDICATOR:
        raise IllegalInstruction(f"command starts without `{COMMAND_INDICATOR}`", s, 0)
    cmd_dict = {"command": li[0][1:],}
    i = 1
    while i < len(li):
        if li[i][0] == PARAMETER_INDICATOR:
            val = None
            try:
                if li[i+1][0] != PARAMETER_INDICATOR:
                    val = li[i+1]
                    
            except IndexError:
                pass
            cmd_dict[li[i][1:]] = val
        elif li[i][0] not in LEGAL_CHARACTER:
            raise IllegalInstruction(
                f"invalid parameter value: first character must start with alphabet or number `{PARAMETER_INDICATOR}`",
                s,
                len(combine(li[:i]))
            )
        i += 1
    return cmd_dict

if __name__ == "__main__":
    ins = "/184 -t aof -l 2"
    print(parse(ins))