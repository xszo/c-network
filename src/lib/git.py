from pathlib import Path
from subprocess import run


class repo:
    """git repo"""

    err: bool = True
    __path: Path = Path()
    __link: str = ""

    def __init__(self, loc: Path) -> None:
        """check if is repo"""
        self.__path = loc.resolve()
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
                    and info.stdout.decode() == str(self.__path) + "\n"
                ):
                    self.err = False
        else:
            self.__path.mkdir(parents=True)
            self.err = False

    def clone(self, remote: str) -> None:
        """clone git repo into loc"""
        if self.err:
            return
        self.__link = remote
        info = run(
            ["git", "remote", "get-url", "origin"],
            cwd=self.__path,
            check=True,
            capture_output=True,
        )
        if not (info.returncode == 0 and info.stdout.decode() == self.__link + "\n"):
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
