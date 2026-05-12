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
    import ssl
    import socket
    import time
    from urllib.parse import urlparse
    from datetime import datetime
except Exception as e:
    ErrorModule(e)

Title("Website Strength Scanner")

try:
    user_agent = ChoiceUserAgent()
    headers = {"User-Agent": user_agent}

    def CheckSSL(url):
        try:
            parsed = urlparse(url)
            hostname = parsed.hostname
            if not hostname:
                return

            context = ssl.create_default_context()
            with socket.create_connection((hostname, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    issuer = dict(x[0] for x in cert.get('issuer', []))
                    subject = dict(x[0] for x in cert.get('subject', []))

                    not_after = cert.get('notAfter')
                    not_before = cert.get('notBefore')

                    if not_after:
                        expiry_date = datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
                        days_until_expiry = (expiry_date - datetime.now()).days

                        if days_until_expiry > 30:
                            print(f"\033[96m {GEN_VALID} SSL Certificate: \033[96m Valid\033[96m Expires in: \033[96m{days_until_expiry} days\033[96m Issuer: \033[96m{issuer.get('organizationName', 'Unknown')}\033[0m")
                        elif days_until_expiry > 0:
                            print(f"\033[96m {WAIT} SSL Certificate: \033[96m Expiring Soon\033[96m Expires in: \033[96m{days_until_expiry} days\033[96m Issuer: \033[96m{issuer.get('organizationName', 'Unknown')}\033[0m")
                        else:
                            print(f"\033[96m {ERROR} SSL Certificate: \033[96m Expired\033[96m Expired: \033[96m{days_until_expiry} days ago\033[0m")

                    version = ssock.version()
                    if version in ['TLSv1.2', 'TLSv1.3']:
                        print(f"\033[96m {GEN_VALID} SSL Version: \033[96m{version}\033[96m Status: \033[96m Secure\033[0m")
                    else:
                        print(f"\033[96m {ERROR} SSL Version: \033[96m{version}\033[96m Status: \033[96m Weak\033[0m")
        except Exception as e:
            print(f"\033[96m {ERROR} SSL Check: \033[96m Failed\033[96m Error: \033[96m{str(e)[:50]}\033[0m")

    def CheckSecurityHeaders(url):
        try:
            response = requests.get(url, timeout=10, headers=headers, allow_redirects=True)
            headers_dict = response.headers

            security_headers = {
                'Strict-Transport-Security': 'HSTS',
                'Content-Security-Policy': 'CSP',
                'X-Frame-Options': 'X-Frame-Options',
                'X-Content-Type-Options': 'X-Content-Type-Options',
                'X-XSS-Protection': 'X-XSS-Protection',
                'Referrer-Policy': 'Referrer-Policy',
                'Permissions-Policy': 'Permissions-Policy'
            }

            found_headers = []
            missing_headers = []

            for header, name in security_headers.items():
                if header in headers_dict:
                    found_headers.append(name)
                    value = headers_dict[header][:60] if len(headers_dict[header]) > 60 else headers_dict[header]
                    print(f"\033[96m {GEN_VALID} Security Header: \033[96m{name}\033[96m Status: \033[96m Present\033[96m Value: \033[96m{value}\033[0m")
                else:
                    missing_headers.append(name)
                    print(f"\033[96m {ERROR} Security Header: \033[96m{name}\033[96m Status: \033[96m Missing\033[0m")

            if found_headers:
                print(f"\033[96m {GEN_VALID} Security Headers Found: \033[96m{len(found_headers)}/{len(security_headers)}\033[0m")
            if missing_headers:
                print(f"\033[96m {ERROR} Security Headers Missing: \033[96m{len(missing_headers)}/{len(security_headers)}\033[0m")

        except Exception as e:
            print(f"\033[96m {ERROR} Security Headers Check: \033[96m Failed\033[96m Error: \033[96m{str(e)[:50]}\033[0m")

    def CheckServerResponse(url):
        try:
            start_time = time.time()
            response = requests.get(url, timeout=10, headers=headers, allow_redirects=True)
            response_time = (time.time() - start_time) * 1000

            status_code = response.status_code
            server = response.headers.get('Server', 'Unknown')
            powered_by = response.headers.get('X-Powered-By', 'Not Disclosed')

            if response_time < 500:
                print(f"\033[96m {GEN_VALID} Response Time: \033[96m{response_time:.2f}ms\033[96m Status: \033[96m Fast\033[0m")
            elif response_time < 2000:
                print(f"\033[96m {WAIT} Response Time: \033[96m{response_time:.2f}ms\033[96m Status: \033[96m Moderate\033[0m")
            else:
                print(f"\033[96m {ERROR} Response Time: \033[96m{response_time:.2f}ms\033[96m Status: \033[96m Slow\033[0m")

            if status_code == 200:
                print(f"\033[96m {GEN_VALID} HTTP Status: \033[96m{status_code}\033[96m Status: \033[96m OK\033[0m")
            elif status_code in [301, 302, 307, 308]:
                print(f"\033[96m {WAIT} HTTP Status: \033[96m{status_code}\033[96m Status: \033[96m Redirect\033[0m")
            else:
                print(f"\033[96m {ERROR} HTTP Status: \033[96m{status_code}\033[96m Status: \033[96m Error\033[0m")

            if server != 'Unknown':
                print(f"\033[96m {INFO} Server: \033[96m{server}\033[0m")
            if powered_by != 'Not Disclosed':
                print(f"\033[96m {INFO} Powered By: \033[96m{powered_by}\033[0m")

        except Exception as e:
            print(f"\033[96m {ERROR} Server Response Check: \033[96m Failed\033[96m Error: \033[96m{str(e)[:50]}\033[0m")

    def CheckHTTPS(url):
        try:
            parsed = urlparse(url)
            scheme = parsed.scheme.lower()

            if scheme == 'https':
                print(f"\033[96m {GEN_VALID} Protocol: \033[96m HTTPS\033[96m Status: \033[96m Secure\033[0m")
            elif scheme == 'http':
                print(f"\033[96m {ERROR} Protocol: \033[96m HTTP\033[96m Status: \033[96m Insecure\033[0m")
            else:
                print(f"\033[96m {ERROR} Protocol: \033[96m{scheme}\033[96m Status: \033[96m Unknown\033[0m")
        except Exception as e:
            print(f"\033[96m {ERROR} Protocol Check: \033[96m Failed\033[96m Error: \033[96m{str(e)[:50]}\033[0m")

    def CheckContentSecurity(url):
        try:
            response = requests.get(url, timeout=10, headers=headers, allow_redirects=True)
            content = response.text.lower()

            sensitive_patterns = {
                'password': 'Password Field',
                'api_key': 'API Key',
                'secret': 'Secret Key',
                'token': 'Token',
                'database': 'Database Info',
                'config': 'Config File'
            }

            found_patterns = []
            for pattern, name in sensitive_patterns.items():
                if pattern in content[:50000]:
                    found_patterns.append(name)

            if found_patterns:
                print(f"\033[96m {WAIT} Content Security: \033[96m Potential Sensitive Data Found\033[96m Patterns: \033[96m{', '.join(found_patterns[:3])}\033[0m")
            else:
                print(f"\033[96m {GEN_VALID} Content Security: \033[96m No Obvious Sensitive Data\033[96m Status: \033[96m Clean\033[0m")

        except Exception as e:
            print(f"\033[96m {ERROR} Content Security Check: \033[96m Failed\033[96m Error: \033[96m{str(e)[:50]}\033[0m")

    print(f"\033[96m {INFO} Selected User-Agent: \033[96m{user_agent}\033[0m")
    website_url = input(f"\033[96m {INPUT} Website Url -> \033[0m")
    Censored(website_url)

    print(f"\033[96m {WAIT} Analyzing website strength...\033[0m")
    if "https://" not in website_url and "http://" not in website_url:
        website_url = "https://" + website_url

    CheckHTTPS(website_url)
    CheckSSL(website_url)
    CheckServerResponse(website_url)
    CheckSecurityHeaders(website_url)
    CheckContentSecurity(website_url)
    Continue()
    Reset()

except Exception as e:
    Error(e)
