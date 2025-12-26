import re

import yaml

from ..lib.git import repo
from .env import (
    PATH_TMP,
    REX_COMMENT,
    VLC_DATA,
    VLC_REPO,
    VLC_REX_INCL,
    VLC_REX_RULE,
    VLC_URI,
)


class getvlc:
    __repo = repo(VLC_REPO, VLC_URI)
    __data = {}
    __no = []

    def __init__(self) -> None:
        if self.__repo.err:
            print("ERR src/rule/getvlc.py repo")

    def __del__(self) -> None:
        with open(PATH_TMP / "no-vlc.yml", "tw", encoding="utf-8") as file:
            yaml.safe_dump(self.__no, file)

    def get(self) -> None:
        return self.__data

    def add(self, name: str, cmd: list) -> None:
        res = []
        dat = []
        for item in cmd:
            self.__incl_file(dat, item)
        while True:
            dat0 = []
            for item in dat:
                if re.match(REX_COMMENT, item):
                    continue
                if lma := re.match(VLC_REX_INCL, item):
                    self.__incl_file(dat0, lma.expand("\\1"))
                    continue
                for pat in VLC_REX_RULE:
                    if lma := re.match(pat[0], item):
                        res.append(lma.expand(pat[1]))
                        break
                else:
                    self.__no.append(item)
            if len(dat0) > 0:
                dat = dat0
            else:
                break
        self.__data[name] = res

    def __incl_file(self, dat: list, loc: str) -> None:
        with open(VLC_DATA / loc, "tr", encoding="utf-8") as file:
            tmp = file.read().splitlines()
        dat.extend(tmp)
