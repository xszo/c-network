from pathlib import Path
from subprocess import run

from ..env import PATH_TMP


class repo:
    """git repo"""

    err = False
    __uri = ""
    __loc = PATH_TMP / "tmp"

    def __init__(self, loc: Path, uri: str) -> None:
        """clone git repo into loc"""
        self.__loc = loc
        self.__uri = uri
        # if loc is occupied
        if self.__loc.exists():
            loc_info = run(
                ["git", "config", "--get", "remote.origin.url"],
                cwd=self.__loc,
                check=True,
                capture_output=True,
            )
            # loc is this repo
            if (
                loc_info.returncode == 0
                and loc_info.stdout.decode("utf-8") == uri + "\n"
            ):
                self.pull()
            elif self.__loc.is_dir() and len(self.__loc.iterdir()) == 0:
                self.clone()
            else:
                self.err = True
        # if loc is empty
        else:
            loc.mkdir(parents=True)
            self.clone()

    def clone(self) -> None:
        """git clone"""
        run(["git", "clone", "--depth=1", self.__uri, "."], cwd=self.__loc, check=False)

    def pull(self) -> None:
        """git pull"""
        run(["git", "pull", "--depth=1", "-r"], cwd=self.__loc, check=False)
