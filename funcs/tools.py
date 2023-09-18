def is_intstr(s: str):
    try:
        int(s)
        return True
    except ValueError:
        return False