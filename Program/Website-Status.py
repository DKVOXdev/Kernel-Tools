# Copyright (c) Kernel-Tool
# See the file 'LICENSE' for copying permission
# ----------------------------------------------------------------------------------------------------------------------------------------------------------|
# EN:
#     - Do not touch or modify the code below. If there is an error, please contact the owner, but under no circumstances should you touch the code.
#     - Do not resell this tool, do not credit it to yours.
# FR:
#     - Ne pas toucher ni modifier le code ci-dessous. En cas d'erreur, veuillez contacter le propriétaire, mais en aucun cas vous ne devez toucher au code.
#     - Ne revendez pas ce tool, ne le créditez pas au vôtre.

from Config.Util import *
from Config.Config import *

try:
    import requests
    from urllib.parse import urlparse
    import re
    try:
        from bs4 import BeautifulSoup
        BEAUTIFULSOUP_AVAILABLE = True
    except ImportError:
        BEAUTIFULSOUP_AVAILABLE = False
except Exception as e:
    ErrorModule(e)

Title("Website Status")

try:
    user_agent = ChoiceUserAgent()
    headers = {"User-Agent": user_agent}

    def CheckWebsiteStatus(url):
        try:
            parsed = urlparse(url)
            domain = parsed.netloc or parsed.path.split('/')[0]

            if domain.startswith('www.'):
                domain = domain[4:]

            if ':' in domain:
                domain = domain.split(':')[0]

            if not domain:
                print(f"\033[96m {ERROR} Invalid URL: {domain}\033[0m")
                return

            print(f"\033[96m {WAIT} Checking status of {domain}...\033[0m")

            check_url = f"https://www.isitdownrightnow.com/{domain}.html"

            try:
                response = requests.get(check_url, timeout=15, headers=headers, allow_redirects=True)

                if response.status_code == 200:
                    if BEAUTIFULSOUP_AVAILABLE:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        page_text = soup.get_text()
                    else:
                        page_text = re.sub(r'<script[^>]*>.*?</script>', '', response.text, flags=re.DOTALL | re.IGNORECASE)
                        page_text = re.sub(r'<style[^>]*>.*?</style>', '', page_text, flags=re.DOTALL | re.IGNORECASE)
                        page_text = re.sub(r'<[^>]+>', ' ', page_text)
                        page_text = ' '.join(page_text.split())

                    if re.search(r'is\s+up\.', page_text, re.IGNORECASE):
                        status = "UP"
                        status_icon = GEN_VALID
                    elif re.search(r'is\s+down\.', page_text, re.IGNORECASE):
                        status = "DOWN"
                        status_icon = ERROR
                    else:
                        try:
                            test_response = requests.get(f"https://{domain}", timeout=10, headers=headers, allow_redirects=True)
                            if test_response.status_code < 500:
                                status = "UP"
                                status_icon = GEN_VALID
                            else:
                                status = "DOWN"
                                status_icon = ERROR
                        except:
                            status = "DOWN"
                            status_icon = ERROR

                    last_checked_match = re.search(r'Last checked\s+(\d+\s+(?:second|sec|minute|min|hour|hr)s?\s+ago)', page_text, re.IGNORECASE)
                    if last_checked_match:
                        last_checked = last_checked_match.group(1)
                    else:
                        last_checked = "Just now"

                    print(f"\033[96m {status_icon} Website: {domain}\033[0m")
                    print(f"\033[96m {status_icon} Status: {status}\033[0m")
                    print(f"\033[96m {status_icon} Last Checked: {last_checked}\033[0m")
                    print(f"\033[96m {status_icon} Source: isitdownrightnow.com\033[0m")

                    print(f"\n\033[96m {WAIT} Verifying directly...\033[0m")
                    try:
                        direct_url = f"https://{domain}" if not domain.startswith('http') else domain
                        direct_response = requests.get(direct_url, timeout=10, headers=headers, allow_redirects=True)

                        if direct_response.status_code < 500:
                            print(f"\033[96m {GEN_VALID} Direct Check: Accessible Status Code: {direct_response.status_code}\033[0m")
                        else:
                            print(f"\033[96m {ERROR} Direct Check: Error Status Code: {direct_response.status_code}\033[0m")
                    except Exception as e:
                        print(f"\033[96m {ERROR} Direct Check: Failed Error: {str(e)[:50]}\033[0m")

                else:
                    print(f"\033[96m {ERROR} Failed to check status: HTTP {response.status_code}\033[0m")
                    print(f"\033[96m {WAIT} Attempting direct connection...\033[0m")
                    try:
                        direct_url = f"https://{domain}" if not domain.startswith('http') else domain
                        direct_response = requests.get(direct_url, timeout=10, headers=headers, allow_redirects=True)
                        if direct_response.status_code < 500:
                            print(f"\033[96m {GEN_VALID} Website: {domain} Status: UP\033[0m")
                        else:
                            print(f"\033[96m {ERROR} Website: {domain} Status: DOWN Status Code: {direct_response.status_code}\033[0m")
                    except:
                        print(f"\033[96m {ERROR} Website: {domain} Status: DOWN\033[0m")

            except requests.exceptions.RequestException as e:
                print(f"\033[96m {ERROR} Connection Error: {str(e)[:50]}\033[0m")
                print(f"\033[96m {WAIT} Attempting direct connection...\033[0m")
                try:
                    direct_url = f"https://{domain}" if not domain.startswith('http') else domain
                    direct_response = requests.get(direct_url, timeout=10, headers=headers, allow_redirects=True)
                    if direct_response.status_code < 500:
                        print(f"\033[96m {GEN_VALID} Website: {domain} Status: UP\033[0m")
                    else:
                        print(f"\033[96m {ERROR} Website: {domain} Status: DOWN\033[0m")
                except:
                    print(f"\033[96m {ERROR} Website: {domain} Status: DOWN\033[0m")

        except Exception as e:
            print(f"\033[96m {ERROR} Error checking website status: {str(e)[:50]}\033[0m")

    print(f"\033[96m {INFO} Selected User-Agent: {user_agent}\033[0m")
    website_url = input(f"\033[96m {INPUT} Website Url -> \033[0m")
    Censored(website_url)

    if not website_url:
        print(f"\033[96m {ERROR} No URL provided\033[0m")
        Continue()
        Reset()
    else:
        CheckWebsiteStatus(website_url)
        Continue()
        Reset()

except Exception as e:
    Error(e)
