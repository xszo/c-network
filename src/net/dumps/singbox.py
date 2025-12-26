import json

res = {}
__src = {}
__var = {"map-node": {"direct": "DIRECT", "reject": "REJECT"}, "proxy-link": []}


def let(lsrc: dict) -> None:
    global __src
    __src = lsrc
    for item in __src["node"]:
        if "id" in item:
            __var["map-node"][item["id"]] = item["name"]


def config(out):
    global res
    res = {
        "log": {
            "disabled": True,
        },
        "dns": {
            "servers": [
                {
                    "type": "udp",
                    "server": "",
                },
                {
                    "type": "https",
                    "server": "",
                },
                {
                    "type": "tls",
                    "server": "",
                },
            ],
            "rules": [
                {
                    "domain": ["captive.apple.com"],
                    "server": "local",
                },
            ],
        },
        "endpoints": [],
        "inbounds": [],
        "outbounds": [
            {
                "type": "selector",
                "tag": "select",
                "outbounds": ["proxy-a", "proxy-b", "proxy-c"],
                "default": "proxy-c",
                "interrupt_exist_connections": False,
            },
            {
                "type": "urltest",
                "tag": "auto",
                "outbounds": ["proxy-a", "proxy-b", "proxy-c"],
                "url": "",
                "interval": "",
                "tolerance": 0,
                "idle_timeout": "",
                "interrupt_exist_connections": False,
            },
        ],
        "route": {
            "rules": [],
            "rule_set": [
                {
                    "type": "remote",
                    "tag": "",
                    "format": "source",
                    "url": "",
                    "update_interval": "",
                }
            ],
            "final": "",
            "auto_detect_interface": False,
            "override_android_vpn": False,
            "default_interface": "",
            "default_mark": 0,
            "default_domain_resolver": "",
            "default_network_strategy": "",
            "default_network_type": [],
            "default_fallback_network_type": [],
            "default_fallback_delay": "",
        },
    }
