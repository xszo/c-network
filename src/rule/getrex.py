import re
from base64 import b64decode
from copy import deepcopy

import yaml

from ..lib.net import get as net_get
from .env import (
    NAME_DOMAIN,
    NAME_IPCIDR_V4,
    NAME_IPCIDR_V6,
    PATH_TMP,
    REX_COMMENT,
    REX_VAR,
)


class getrex:
    """get link text and use rex to format"""

    __data = {
        NAME_DOMAIN: {},
        NAME_IPCIDR_V4: {},
        NAME_IPCIDR_V6: {},
    }
    __rex_var = deepcopy(REX_VAR)
    __no = []

    def __init__(self) -> None:
        PATH_TMP.mkdir(parents=True, exist_ok=True)

    def __del__(self) -> None:
        with open(PATH_TMP / "no-rex.yml", "tw", encoding="utf-8") as file:
            yaml.safe_dump(self.__no, file)

    def get(self) -> None:
        return self.__data

    def add(self, uri: str, rex: dict, pre: list) -> None:
        dat = net_get(uri)
        if "b64" in pre:
            dat = b64decode(dat).decode("utf-8")
        dat = dat.splitlines()
        self.__add_rex(dat, self.__rex_c(rex))

    def add_var(self, dat: dict) -> None:
        # compile var
        for name, line in dat.items():
            self.__rex_var.append((re.compile("\\\\=" + name + "\\\\"), line))

    def __rex_c(self, rex: dict) -> tuple:
        res = []
        for name, ls in rex.items():
            for line in ls:
                for v in self.__rex_var:
                    line = re.sub(v[0], v[1], line)
                match ((line := line.split("  "))[0]):
                    case "d":
                        ty = NAME_DOMAIN
                    case "4":
                        ty = NAME_IPCIDR_V4
                    case "6":
                        ty = NAME_IPCIDR_V6
                    case _:
                        continue
                res.append((ty, name, re.compile(line[1]), line[2]))
                if name not in self.__data[ty]:
                    self.__data[ty][name] = []
        return tuple(res)

    def __add_rex(self, dat: tuple | list, rex: tuple | list) -> None:
        for line in dat:
            if re.match(REX_COMMENT, line):
                continue
            line = line.lower()
            for pat in rex:
                if lma := re.match(pat[2], line):
                    self.__data[pat[0]][pat[1]].append(lma.expand(pat[3]))
                    break
            else:
                self.__no.append(line)
