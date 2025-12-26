import yaml

from ..lib import var
from .env import (
    NAME_CLASH,
    NAME_DOMAIN,
    NAME_IP,
    NAME_IPASN,
    NAME_IPCIDR_V4,
    NAME_IPCIDR_V6,
    NAME_IPGEO,
    NAME_SURGE,
    PATH_OUT,
    ZONE,
)

var.zone(ZONE)


class dump:
    """write rule files and register rule"""

    __raw = {}
    # rulesets

    def __init__(self) -> None:
        PATH_OUT.mkdir(parents=True, exist_ok=True)

    def dump(self, raw: dict) -> None:
        self.__raw = raw
        var.add(NAME_DOMAIN, self.__do_domain())
        var.add(NAME_IP, self.__do_ip())

    def __do_domain(self) -> dict:
        res = {}
        for key, val in self.__raw[NAME_DOMAIN].items():
            if len(val) == 0:
                continue
            # dump surge
            loc = key + "-" + NAME_DOMAIN + "-" + NAME_SURGE + ".txt"
            with open(
                PATH_OUT / loc,
                "tw",
                encoding="utf-8",
            ) as file:
                file.writelines(
                    [
                        (
                            "DOMAIN-WILDCARD," + x + "\n"
                            if "*" in x or "?" in x
                            else (
                                "DOMAIN-SUFFIX," + x[1:] + "\n"
                                if x[0] == "."
                                else "DOMAIN," + x + "\n"
                            )
                        )
                        for x in val
                    ]
                )
            res[key + "-" + NAME_SURGE] = loc
            # dump clash
            loc = key + "-" + NAME_DOMAIN + "-" + NAME_CLASH + ".yml"
            with open(PATH_OUT / loc, "tw", encoding="utf-8") as file:
                yaml.safe_dump(
                    {"payload": ["+" + x if x[0] == "." else x for x in val]}, file
                )
            res[key + "-" + NAME_CLASH] = loc
        return res

    def __do_ip(self) -> dict:
        res = {}
        # convert to {name: {type: [list]}}
        raw = {}
        for ty in (NAME_IPCIDR_V4, NAME_IPCIDR_V6, NAME_IPASN, NAME_IPGEO):
            for key, val in self.__raw[ty].items():
                if len(val) == 0:
                    continue
                if key not in raw:
                    raw[key] = {}
                raw[key][ty] = val
        # dump surge
        for key, val in raw.items():
            # format data
            dat = []
            if NAME_IPCIDR_V4 in val:
                dat.extend(["IP-CIDR," + x + "\n" for x in val[NAME_IPCIDR_V4]])
            if NAME_IPCIDR_V6 in val:
                dat.extend(["IP-CIDR6," + x + "\n" for x in val[NAME_IPCIDR_V6]])
            if NAME_IPASN in val:
                dat.extend(["IP-ASN," + str(x) + "\n" for x in val[NAME_IPASN]])
            if NAME_IPGEO in val:
                dat.extend(["GEOIP," + x + "\n" for x in val[NAME_IPGEO]])
            # write file
            loc = key + "-" + NAME_IP + "-" + NAME_SURGE + ".txt"
            with open(PATH_OUT / loc, "tw", encoding="utf-8") as file:
                file.writelines(dat)
            res[key + "-" + NAME_SURGE] = loc
        return res
