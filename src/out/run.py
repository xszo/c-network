from ..env import PATH_OUT, REMOTE_URI
from .html import write_index


def run() -> None:
    write_index(PATH_OUT, REMOTE_URI)
    with open(PATH_OUT / "null", "tw", encoding="utf-8") as file:
        file.write("\n")
