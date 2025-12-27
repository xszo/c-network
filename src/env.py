from pathlib import Path

# name
NAME_NET = "net"
NAME_RULE = "rule"

# path
PATH_VAR = Path("var/")
PATH_VAR_NET = PATH_VAR / NAME_NET
PATH_VAR_RULE = PATH_VAR / NAME_RULE

PATH_TMP = Path("tmp/")
PATH_TMP_NET = PATH_TMP / NAME_NET
PATH_TMP_RULE = PATH_TMP / NAME_RULE

PATH_OUT = Path("out/")
PATH_OUT_NET = PATH_OUT / NAME_NET
PATH_OUT_RULE = PATH_OUT / NAME_RULE

# remote
REMOTE_URI = "https://xszo.github.io/er/"
REMOTE_URI_NULL = "https://xszo.github.io/er/null"
REMOTE_URI_NET = REMOTE_URI + NAME_NET + "/"
REMOTE_URI_RULE = REMOTE_URI + NAME_RULE + "/"

REMOTE_INTERVAL = 86400
