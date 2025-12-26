from pathlib import Path

import requests


def get(link: str) -> str:
    """get link content as text"""
    return requests.get(link, timeout=8, allow_redirects=True).text


def download(link: str, dist: Path) -> None:
    """download link content to given path"""
    with open(dist, "tw", encoding="utf-8") as file:
        file.write(get(link))
