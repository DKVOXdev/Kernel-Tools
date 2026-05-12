# Copyright (c) Kernel-Tool
# See the file 'LICENSE' for copying permission
# ----------------------------------------------------------------------------------------------------------------------------------------------------------|
# EN:
#     - Do not touch or modify the code below. If there is an error, please contact the owner, but under no circumstances should you touch the code.
#     - Do not resell this tool, do not credit it to yours.
# FR:
#     - Ne pas toucher ni modifier le code ci-dessous. En cas d'erreur, veuillez contacter le propriétaire, mais en aucun cas vous ne devez toucher au code.
#     - Ne revendez pas ce tool, ne le créditez pas au vôtre.

import os
import re
import dns.resolver
from Config.Config import *
from Config.Util import *

if os.name == "nt":
    try:
        import ctypes
        ctypes.windll.kernel32.SetConsoleMode(
            ctypes.windll.kernel32.GetStdHandle(-11), 7
        )
    except:
        pass

resolver = dns.resolver.Resolver(configure=False)
resolver.nameservers = ['8.8.8.8', '8.8.4.4']

def get_email_info(email):
    info = {}
    domain_all = email.split('@')[-1] if '@' in email else "N/A"
    name = email.split('@')[0] if '@' in email else "N/A"
    domain_match = re.search(r"@([^@.]+)\.", email)
    domain = domain_match.group(1) if domain_match else "N/A"
    tld = f".{email.split('.')[-1]}" if '.' in email else "N/A"

    try:
        mx_records = resolver.resolve(domain_all, 'MX')
        info["mx_servers"] = [str(r.exchange) for r in mx_records]
    except:
        info["mx_servers"] = None

    try:
        spf_records = resolver.resolve(domain_all, 'SPF')
        info["spf_records"] = [str(r) for r in spf_records]
    except:
        info["spf_records"] = None

    try:
        dmarc_records = resolver.resolve(f"_dmarc.{domain_all}", 'TXT')
        info["dmarc_records"] = [str(r) for r in dmarc_records]
    except:
        info["dmarc_records"] = None

    info["google_workspace"] = False
    info["microsoft_365"] = False
    if info.get("mx_servers"):
        for server in info["mx_servers"]:
            if "google.com" in server:
                info["google_workspace"] = True
            if "outlook.com" in server:
                info["microsoft_365"] = True

    return info, domain_all, domain, tld, name

Title("Mail Info")

try:
    email = input(f"\033[96m {INPUT} Email -> \033[0m").strip()

    if not email:
        print(f"\033[96m {ERROR} Email invalide\033[0m")
        Continue()
        Reset()
    else:
        info, domain_all, domain, tld, name = get_email_info(email)

        mx = ", ".join(info.get("mx_servers")) if info.get("mx_servers") else "N/A"
        spf = ", ".join(info.get("spf_records")) if info.get("spf_records") else "N/A"
        dmarc = ", ".join(info.get("dmarc_records")) if info.get("dmarc_records") else "N/A"
        google_ws = str(info.get("google_workspace", False))
        microsoft_365 = str(info.get("microsoft_365", False))

        name = str(name)
        domain = str(domain)
        tld = str(tld)
        domain_all = str(domain_all)

        print(f"""
\033[96m────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 {INFO_ADD} Email         : {email}
 {INFO_ADD} Name          : {name}
 {INFO_ADD} Domain        : {domain}
 {INFO_ADD} TLD           : {tld}
 {INFO_ADD} Domain All    : {domain_all}
 {INFO_ADD} MX Servers    : {mx}
 {INFO_ADD} SPF Records   : {spf}
 {INFO_ADD} DMARC         : {dmarc}
 {INFO_ADD} Google WS     : {google_ws}
 {INFO_ADD} Microsoft 365 : {microsoft_365}
\033[96m────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
\033[0m""")

        Continue()
        Reset()

except Exception as e:
    Error(e)
