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
    NAME_QUANTUMULT,
    NAME_SURGE,
    PATH_OUT,
    REMOTE_URL,
    ZONE,
)

var.zone(ZONE)


class dump:
    """write rule files and register rule"""

    def __init__(self) -> None:
        PATH_OUT.mkdir(parents=True, exist_ok=True)

    def dump(self, raw: dict) -> None:
        reg = {NAME_DOMAIN: {}, NAME_IP: {}, NAME_QUANTUMULT: {}}
        raw_n = {}
        for ty in (
            NAME_DOMAIN,
            NAME_IPCIDR_V4,
            NAME_IPCIDR_V6,
            NAME_IPASN,
            NAME_IPGEO,
        ):
            for key, val in raw[ty].items():
                if len(val) == 0:
                    continue
                if key not in raw_n:
                    raw_n[key] = {}
                raw_n[key][ty] = val
        for key, val in raw_n.items():
            ls_q = []
            if NAME_DOMAIN in val:
                # dump surge domain
                with open(
                    PATH_OUT
                    / (
                        loc := key
                        + "-"
                        + NAME_DOMAIN
                        + "-"
                        + NAME_SURGE
                        + ".txt"
                    ),
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
                            for x in val[NAME_DOMAIN]
                        ]
                    )
                reg[NAME_DOMAIN][key + "-" + NAME_SURGE] = REMOTE_URL + loc
                # dump clash domain
                with open(
                    PATH_OUT
                    / (
                        loc := key
                        + "-"
                        + NAME_DOMAIN
                        + "-"
                        + NAME_CLASH
                        + ".yml"
                    ),
                    "tw",
                    encoding="utf-8",
                ) as file:
                    yaml.safe_dump(
                        {
                            "payload": [
                                "+" + x if x[0] == "." else x
                                for x in val[NAME_DOMAIN]
                            ]
                        },
                        file,
                    )
                reg[NAME_DOMAIN][key + "-" + NAME_CLASH] = REMOTE_URL + loc
                # dump quantumult domain
                ls_q.extend(
                    [
                        (
                            "host-wildcard," + x + ",proxy\n"
                            if "*" in x or "?" in x
                            else (
                                "host-suffix," + x[1:] + ",proxy\n"
                                if x[0] == "."
                                else "host," + x + ",proxy\n"
                            )
                        )
                        for x in val[NAME_DOMAIN]
                    ]
                )
            # dump ip
            ls_s = []
            if NAME_IPCIDR_V4 in val:
                ls_s.extend(
                    ["IP-CIDR," + x + "\n" for x in val[NAME_IPCIDR_V4]]
                )
                ls_q.extend(
                    ["ip-cidr," + x + ",proxy\n" for x in val[NAME_IPCIDR_V4]]
                )
            if NAME_IPCIDR_V6 in val:
                ls_s.extend(
                    ["IP-CIDR6," + x + "\n" for x in val[NAME_IPCIDR_V6]]
                )
                ls_q.extend(
                    ["ip6-cidr," + x + ",proxy\n" for x in val[NAME_IPCIDR_V6]]
                )
            if NAME_IPASN in val:
                ls_s.extend(
                    ["IP-ASN," + str(x) + "\n" for x in val[NAME_IPASN]]
                )
                ls_q.extend(
                    ["ip-asn," + str(x) + ",proxy\n" for x in val[NAME_IPASN]]
                )
            if NAME_IPGEO in val:
                ls_s.extend(
                    ["GEOIP," + x.upper() + "\n" for x in val[NAME_IPGEO]]
                )
                ls_q.extend(
                    ["geoip," + x + ",proxy\n" for x in val[NAME_IPGEO]]
                )
            # write surge ip
            if ls_s:
                loc = key + "-" + NAME_IP + "-" + NAME_SURGE + ".txt"
                with open(PATH_OUT / loc, "tw", encoding="utf-8") as file:
                    file.writelines(ls_s)
                reg[NAME_IP][key + "-" + NAME_SURGE] = REMOTE_URL + loc
            # write quantumult
            loc = key + "-" + NAME_QUANTUMULT + ".txt"
            with open(PATH_OUT / loc, "tw", encoding="utf-8") as file:
                file.writelines(ls_q)
            reg[NAME_QUANTUMULT][key] = REMOTE_URL + loc
        var.adds(reg)
