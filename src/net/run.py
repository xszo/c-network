import yaml

from . import dump, load
from .env import PATH_VAR, PATH_VAR_LIST


def run() -> None:
    dump.init()
    # load runtime data
    with open(PATH_VAR_LIST, "tr", encoding="utf-8") as file:
        data = yaml.safe_load(file)
    with open(PATH_VAR / data["base"], "tr", encoding="utf-8") as file:
        raw = yaml.safe_load(file)
        raw["proxy"] = data["proxy"]
        load.base(raw)
    # generate files
    for item in data["list"]:
        with open(PATH_VAR / item, "tr", encoding="utf-8") as file:
            raw = yaml.safe_load(file)
            dump.dump(load.load(raw))
