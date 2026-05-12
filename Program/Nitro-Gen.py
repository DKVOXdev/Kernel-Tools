# =============================================================================
# Copyright (c) Kernel-Tool
# See the file 'LICENSE' for full licensing information.
# =============================================================================
#
# EN:
#     - Do not modify or touch the code below.
#     - If there is an error, contact the owner.
#     - Do not resell this tool. Do not claim it as your own.
#
# FR:
#     - Ne pas modifier ni toucher au code ci-dessous.
#     - En cas d'erreur, contactez le propriétaire.
#     - Ne revendez pas cet outil. Ne le revendiquez pas comme le vôtre.
#
# =============================================================================

from Config.Util import *
from Config.Config import *

try:
    import random
    import string
    import json
    import requests
    import threading
except Exception as e:
   ErrorModule(e)

Title("Nitro Gen")

# Force bleu cyan clair partout
cyan = "\033[1;36m"
reset = "\033[0m"

try:
    print(f"{cyan}")
    use_webhook = input(f"{BEFORE + AFTER} {INPUT} Webhook ? (y/n) -> {reset}").strip()

    if use_webhook.lower() in ['y', 'yes']:
        webhook_url = input(f"{BEFORE + AFTER} {INPUT} Webhook Url -> {reset}").strip()
        CheckWebhook(webhook_url)

    try:
        thread_count = int(input(f"{BEFORE + AFTER} {INPUT} Threads Number -> {reset}"))
    except:
        ErrorNumber()

    def send_webhook(nitro_url):
        webhook_payload = {
            'embeds': [{
                'title': 'Nitro Valid !',
                'description': f"**Nitro Verified:**\n```{nitro_url}```",
                'color': color_webhook,
                'footer': {
                    "text": username_webhook,
                    "icon_url": avatar_webhook,
                }
            }],
            'username': username_webhook,
            'avatar_url': avatar_webhook
        }

        webhook_headers = {'Content-Type': 'application/json'}
        requests.post(webhook_url, data=json.dumps(webhook_payload), headers=webhook_headers)

    def check_nitro():
        nitro_code = ''.join([random.choice(string.ascii_uppercase + string.digits) for _ in range(16)])
        nitro_url = f'https://discord.gift/{nitro_code}'
        
        try:
            api_response = requests.get(
                f'https://discordapp.com/api/v6/entitlements/gift-codes/{nitro_code}?with_application=false&with_subscription_plan=true',
                timeout=1
            )
        except:
            api_response = type('obj', (object,), {'status_code': 404})()

        if api_response.status_code == 200:
            if use_webhook.lower() in ['y', 'yes']:
                send_webhook(nitro_url)
            print(f"{BEFORE + AFTER} {GEN_VALID} Status: {white}Valid {cyan}✅ Verified {cyan}Nitro: {nitro_url}{reset}")
        else:
            print(f"{BEFORE + AFTER} {GEN_INVALID} Status: {white}Invalid {cyan}Nitro: {nitro_url}{reset}")

    def run_threads():
        thread_list = []
        try:
            for _ in range(int(thread_count)):
                thread = threading.Thread(target=check_nitro)
                thread.start()
                thread_list.append(thread)
        except:
            ErrorNumber()

        for thread in thread_list:
            thread.join()

    print(f"{cyan}Nitro Generator démarré avec {thread_count} threads...{reset}\n")
    
    while True:
        run_threads()

except Exception as e:
    Error(e)
