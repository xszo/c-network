from pathlib import Path
from subprocess import run


class repo:
    """git repo"""

    err = False
    __uri = ""
    __loc = Path()

    def __init__(self, loc: Path, uri: str) -> None:
        """clone git repo into loc"""
        self.__loc = loc
        self.__uri = uri
        # if loc is occupied
        if self.__loc.exists():
            # loc is empty dir
            if self.__loc.is_dir() and not any(self.__loc.iterdir()):
                self.clone()
            else:
                # get git remote url
                loc_info = run(
                    ["git", "config", "--get", "remote.origin.url"],
                    cwd=self.__loc,
                    check=True,
                    capture_output=True,
                )
                # loc is this repo
                if (
                    loc_info.returncode == 0
                    and loc_info.stdout.decode("utf-8") == self.__uri + "\n"
                ):
                    self.pull()
                else:
                    self.err = True
        # if loc is empty
        else:
            self.__loc.mkdir(parents=True)
            self.clone()

    def clone(self) -> None:
        """git clone"""
        run(["git", "clone", "--depth=1", self.__uri, "."], cwd=self.__loc, check=False)

    def pull(self) -> None:
        """git pull"""
        run(["git", "pull", "--depth=1", "-r"], cwd=self.__loc, check=False)
