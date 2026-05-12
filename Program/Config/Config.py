# Copyright (c) Kernel-Tool
# See the file 'LICENSE' for copying permission
# ------------------------------------------------------------------------------------------------
# EN:
#     - Do not touch or modify the code below. If there is an error, please contact the owner,
#       but under no circumstances should you touch the code.
#     - Do not resell this tool, do not credit it to yours.
# FR:
#     - Ne pas toucher ni modifier le code ci-dessous. En cas d'erreur, veuillez contacter le
#       propriétaire, mais en aucun cas vous ne devez toucher au code.
#     - Ne revendez pas ce tool, ne le créditez pas au vôtre.
# ------------------------------------------------------------------------------------------------

import os
import sys

LC = "\033[38;2;0;200;255m"
RS = "\033[0m"

class color:
    RESET   = RS
    RED     = LC
    GREEN   = LC
    YELLOW  = LC
    BLUE    = LC
    MAGENTA = LC
    CYAN    = LC
    WHITE   = LC

BEFORE       = LC
AFTER        = RS
BEFORE_GREEN = LC
AFTER_GREEN  = RS

INFO        = "[INFO]"
ERROR       = "[ERROR]"
WAIT        = "[WAIT]"
INPUT       = "[INPUT]"
GEN_VALID   = "[VALID]"
GEN_INVALID = "[INVALID]"
ADD         = "[ADD]"
INFO_ADD    = "[+]"

white = LC
green = LC
red   = LC
blue  = LC
cyan  = LC
reset = RS

sql_banner = (
    f"{LC}"
    "\n"
    "╔══════════════════════════════════════════════════════════════╗\n"
    "║                    Website Strength Scanner                   ║\n"
    "╚══════════════════════════════════════════════════════════════╝"
    f"{RS}"
)

discord_banner = (
    f"{LC}"
    "\n"
    "╔══════════════════════════════════════════════════════════════╗\n"
    "║                      Discord Tools                            ║\n"
    "╚══════════════════════════════════════════════════════════════╝"
    f"{RS}"
)

map_banner = (
    f"{LC}"
    "\n"
    "╔══════════════════════════════════════════════════════════════╗\n"
    "║                        IP Lookup                             ║\n"
    "╚══════════════════════════════════════════════════════════════╝"
    f"{RS}"
)

mail_banner = (
    f"{LC}"
    "\n"
    "╔══════════════════════════════════════════════════════════════╗\n"
    "║                       Mail Info                               ║\n"
    "╚══════════════════════════════════════════════════════════════╝"
    f"{RS}"
)

status_banner = (
    f"{LC}"
    "\n"
    "╔══════════════════════════════════════════════════════════════╗\n"
    "║                     Website Status                            ║\n"
    "╚══════════════════════════════════════════════════════════════╝"
    f"{RS}"
)

phone_banner = (
    f"{LC}"
    "\n"
    "╔══════════════════════════════════════════════════════════════╗\n"
    "║                      Phone Lookup                             ║\n"
    "╚══════════════════════════════════════════════════════════════╝"
    f"{RS}"
)

username_banner = (
    f"{LC}"
    "\n"
    "╔══════════════════════════════════════════════════════════════╗\n"
    "║                    Username Tracker                           ║\n"
    "╚══════════════════════════════════════════════════════════════╝"
    f"{RS}"
)

github_banner = (
    f"{LC}"
    "\n"
    "╔══════════════════════════════════════════════════════════════╗\n"
    "║                      Lookup Github                            ║\n"
    "╚══════════════════════════════════════════════════════════════╝"
    f"{RS}"
)

fake_identity_banner = (
    f"{LC}"
    "\n"
    "╔══════════════════════════════════════════════════════════════╗\n"
    "║                      Fake Identity                            ║\n"
    "╚══════════════════════════════════════════════════════════════╝"
    f"{RS}"
)

cookie_login_banner = (
    f"{LC}"
    "\n"
    "╔══════════════════════════════════════════════════════════════╗\n"
    "║                      Cookie Login                             ║\n"
    "╚══════════════════════════════════════════════════════════════╝"
    f"{RS}"
)

roblox_banner = (
    f"{LC}"
    "\n"
    "╔══════════════════════════════════════════════════════════════╗\n"
    "║                      Pseudo Info                              ║\n"
    "╚══════════════════════════════════════════════════════════════╝"
    f"{RS}"
)

tool_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os_name   = "Windows" if os.name == 'nt' else "Linux"

