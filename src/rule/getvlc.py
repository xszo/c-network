import re

import yaml

from ..lib.git import repo
from .env import (
    PATH_TMP,
    REX_COMMENT,
    VLC_DATA,
    VLC_REPO_PATH,
    VLC_REPO_URL,
    VLC_REX_INCL,
    VLC_REX_RULE,
    VLC_REX_COM,
)


class getvlc:
    __repo: repo = None
    __data: dict[str, list[str]] = {}
    __no: list[str] = []

    def __init__(self) -> None:
        self.__repo = repo(VLC_REPO_PATH)
        self.__repo.clone(VLC_REPO_URL)
        self.__repo.pull()
        if self.__repo.err:
            print("ERR src/rule/getvlc.py repo")
            self.__del__()

    def __del__(self) -> None:
        # dump no match lines
        with open(PATH_TMP / "no-vlc.yml", "tw", encoding="utf-8") as file:
            yaml.safe_dump(self.__no, file)

    def get(self) -> dict:
        return self.__data

    def add(self, name: str, cmd: list) -> None:
        res = []
        # read files
        dat = []
        for item in cmd:
            dat.append(self.__load_incl(item))
        # parse lines
        while len(dat) > 0:
            dat_nxt = []
            for item in dat:
                if len(item["incl"]) + len(item["excl"]) > 0:
                    for line in item["data"]:
                        if len(line := re.sub(VLC_REX_COM, "", line)) == 0:
                            continue
                        if lma := re.match(VLC_REX_INCL, line):
                            tmp = self.__load_incl(lma.expand("\\1"))
                            tmp["incl"].update(item["incl"])
                            tmp["excl"].update(item["excl"])
                            dat_nxt.append(tmp)
                            continue
                        line = re.sub("\\s", "", line).split("@")
                        if len(line) > 1:
                            a = set(line[1:])
                            if (
                                len(item["incl"]) > 0 and a.isdisjoint(item["incl"])
                            ) or (
                                len(item["excl"]) > 0 and not a.isdisjoint(item["excl"])
                            ):
                                continue
                        for pat in VLC_REX_RULE:
                            if lma := re.match(pat[0], line[0]):
                                res.append(lma.expand(pat[1]))
                                break
                        else:
                            self.__no.append(line[0])
                else:
                    for line in item["data"]:
                        if len(line := re.sub(VLC_REX_COM, "", line)) == 0:
                            continue
                        if lma := re.match(VLC_REX_INCL, line):
                            dat_nxt.append(self.__load_incl(lma.expand("\\1")))
                            continue
                        line = re.sub("\\s", "", line).split("@")
                        for pat in VLC_REX_RULE:
                            if lma := re.match(pat[0], line[0]):
                                res.append(lma.expand(pat[1]))
                                break
                        else:
                            self.__no.append(line[0])
            dat = dat_nxt
        self.__data[name] = res

    def __load_incl(self, text: str) -> dict:
        # remove space and split attr
        line = re.sub("\\s", "", text).split("@")
        # load incl & excl
        attr = {"incl": set(), "excl": set()}
        if len(line) > 1:
            for item in line[1:]:
                if item[0] == "-":
                    attr["excl"].add(item[1:])
                else:
                    attr["incl"].add(item)
        # load file from vlc
        with open(VLC_DATA / line[0], "tr", encoding="utf-8") as file:
            attr["data"] = file.read().splitlines()
        return attr
