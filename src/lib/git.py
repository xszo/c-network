from pathlib import Path
from subprocess import run

from ..env import SYS_TXTCODE


class repo:
    """git repo"""

    err: bool = True
    __path: Path
    __link: str

    def __init__(self, loc: Path, rmt: str = "") -> None:
        """check if is repo"""
        self.__path = loc.resolve()
        if len(rmt) > 8:
            self.__link = rmt

        if self.__path.exists():
            if self.__path.is_dir():
                info = run(
                    ["git", "rev-parse", "--show-toplevel"],
                    cwd=self.__path,
                    check=True,
                    capture_output=True,
                )
                if (
                    info.returncode == 0
                    and info.stdout.decode(SYS_TXTCODE)
                    == str(self.__path) + "\n"
                ):
                    if self.__link:
                        info = run(
                            ["git", "remote", "get-url", "origin"],
                            cwd=self.__path,
                            check=True,
                            capture_output=True,
                        )
                        if not (
                            info.returncode == 0
                            and info.stdout.decode(SYS_TXTCODE) == self.__link
                        ):
                            self.err = False
                    else:
                        self.err = False

        else:
            self.__path.mkdir(parents=True)
            if self.__link:
                self.__clone()
            else:
                self.__initialize()
            self.err = False

    def __initialize(self) -> None:
        """initialize git repo"""
        run(["git", "init"], cwd=self.__path, check=False)

    def __clone(self) -> None:
        """clone git repo using link"""
        run(["rm", "-rf", "{*,.*}"], cwd=self.__path, check=False)
        run(
            ["git", "clone", "--depth=1", self.__link, "."],
            cwd=self.__path,
            check=False,
        )

    def pull(self) -> None:
        """git pull"""
        if self.err:
            return
        run(["git", "pull", "--depth=1", "-r"], cwd=self.__path, check=False)
