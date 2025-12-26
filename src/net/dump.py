from ..lib import net
from .dumps import clash, clash_conv, conv, quantumult, shadowrocket, surge
from .env import EXT_QUANTUMULT_PARSER, PATH_OUT, URI_NET

# Var
__src = {}
__var = {"once": set()}


# Init
def init() -> None:
    PATH_OUT.mkdir(parents=True, exist_ok=True)


def dump(lsrc: dict) -> None:
    global __src
    if not "ref" in lsrc:
        return
    var = lsrc.pop("ref")
    if var["id"] != "":
        var["id"] = "-" + var["id"]
    __src = lsrc

    if "quantumult" in var["tar"]:
        __quantumult(var["id"])
    if "clash" in var["tar"]:
        __clash(var["id"])
    if "surge" in var["tar"]:
        __surge(var["id"])
    if "shadowrocket" in var["tar"]:
        __shadowrocket(var["id"])


def __quantumult(alia: str) -> None:
    quantumult.let(__src)

    with open(
        PATH_OUT / ("quantumult" + alia + ".conf"),
        "tw",
        encoding="utf-8",
    ) as out:
        quantumult.profile(
            out,
            {
                "parse": URI_NET + "quantumult-parser.js",
            },
        )

    if not "qp" in __var["once"]:
        __var["once"].add("qp")
        net.download(
            EXT_QUANTUMULT_PARSER,
            PATH_OUT / "quantumult-parser.js",
        )


def __clash(alia: str) -> None:
    clash.let(__src)

    with open(PATH_OUT / ("clash" + alia + ".yml"), "tw", encoding="utf-8") as out:
        clash.config(out)

    clash_conv.let(__src)

    with open(
        PATH_OUT / ("clash-conv" + alia + ".conf"),
        "tw",
        encoding="utf-8",
    ) as out:
        clash_conv.config(out, {"yml": URI_NET + "clash-conv-base" + alia + ".yml"})

    with open(
        PATH_OUT / ("clash-conv-base" + alia + ".yml"),
        "tw",
        encoding="utf-8",
    ) as out:
        clash_conv.base(out)


def __surge(alia: str) -> None:
    surge.let(__src)

    with open(
        PATH_OUT / ("surge-base" + alia + ".conf"),
        "tw",
        encoding="utf-8",
    ) as out:
        surge.base(out, {"up": URI_NET + "surge-base" + alia + ".conf"})

    if not "sp" in __var["once"]:
        __var["once"].add("sp")
        with open(
            PATH_OUT / "surge-proxy.conf",
            "tw",
            encoding="utf-8",
        ) as out:
            surge.proxy(out)

    with open(
        PATH_OUT / ("surge" + alia + ".conf"),
        "tw",
        encoding="utf-8",
    ) as out:
        surge.profile(out, {"base": "surge-base" + alia + ".conf"})

    if not "sc" in __var["once"]:
        __var["once"].add("sc")
        with open(
            PATH_OUT / "conv.conf",
            "tw",
            encoding="utf-8",
        ) as out:
            conv.proxy(out)


def __shadowrocket(alia: str) -> None:
    shadowrocket.let(__src)

    with open(
        PATH_OUT / ("shadowrocket" + alia + ".conf"),
        "tw",
        encoding="utf-8",
    ) as out:
        shadowrocket.config(
            out,
            {
                "up": URI_NET + "shadowrocket" + alia + ".conf",
            },
        )
