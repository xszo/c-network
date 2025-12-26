from ..env import REMOTE_URI_NULL


def proxy(out) -> None:
    out.writelines(
        [
            x + "\n"
            for x in [
                "[custom]",
                #
                "enable_rule_generator=true",
                "overwrite_original_rules=true",
                "ruleset=DIRECT,[]FINAL",
                #
                "custom_proxy_group=ON`select`[]DIRECT`[]REJECT",
                #
                "rename=^(JMS-\\d+).(c\\d+s[123])\\..*@$1 $2 US",
                "rename=^(JMS-\\d+).(c\\d+s4)\\..*@$1 $2 JP",
                "rename=^(JMS-\\d+).(c\\d+s5)\\..*@$1 $2 NL",
                "rename=^(JMS-\\d+).(c\\d+s\\d+)\\..*@$1 $2",
                #
                "clash_rule_base=" + REMOTE_URI_NULL,
                "loon_rule_base=" + REMOTE_URI_NULL,
                "mellow_rule_base=" + REMOTE_URI_NULL,
                "quan_rule_base=" + REMOTE_URI_NULL,
                "quanx_rule_base=" + REMOTE_URI_NULL,
                "singbox_rule_base=" + REMOTE_URI_NULL,
                "sssub_rule_base=" + REMOTE_URI_NULL,
                "surfboard_rule_base=" + REMOTE_URI_NULL,
                "surge_rule_base=" + REMOTE_URI_NULL,
            ]
        ]
    )
