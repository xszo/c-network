from copy import deepcopy

__var = {"var": {}}
__zone = "var"


def zone(use: str) -> str:
    """set var namespace"""
    global __zone
    if isinstance(use, str):
        __zone = use
        if __zone not in __var:
            __var[__zone] = {}
    else:
        __zone = "var"
    return __zone


def get(key: str):
    """get key pair from shared var"""
    return deepcopy(__var[__zone][key])


def gets():
    """get all pairs from shared var"""
    return deepcopy(__var[__zone])


def add(key: str, val) -> None:
    """add key pair to shared var"""
    __var[__zone][key] = val


def adds(ls: dict) -> None:
    """add all key pairs to shared var"""
    __var[__zone].update(ls)


def pop(key: str):
    """pop key from shared var"""
    return __var[__zone].pop(key)


def clear():
    """clear shared var"""
    res = __var.pop(__zone)
    __var[__zone] = {}
    return res
