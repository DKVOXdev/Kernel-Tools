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
    import phonenumbers
    from phonenumbers import geocoder, carrier, timezone
except Exception as e:
    ErrorModule(e)

Title("Phone Lookup")

try:
    phone_number = input(f"\n\033[96m{current_time_hour()} {INPUT} Phone Number -> \033[0m")
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        if phonenumbers.is_valid_number(parsed_number):
            status = "Valid"
        else:
            status = "Invalid"

        if phone_number.startswith("+"):
            country_code = "+" + phone_number[1:3]
        else:
            country_code = "None"

        try: operator = carrier.name_for_number(parsed_number, "fr")
        except: operator = "None"

        try: type_number = "Mobile" if phonenumbers.number_type(parsed_number) == phonenumbers.PhoneNumberType.MOBILE else "Fixe"
        except: type_number = "None"

        try:
            timezones = timezone.time_zones_for_number(parsed_number)
            timezone_info = timezones[0] if timezones else None
        except: timezone_info = "None"

        try: country = phonenumbers.region_code_for_number(parsed_number)
        except: country = "None"

        try: region = geocoder.description_for_number(parsed_number, "fr")
        except: region = "None"

        try: formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)
        except: formatted_number = "None"

        print(f"""
\033[96m────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 {INFO_ADD} Phone        : {phone_number}
 {INFO_ADD} Formatted    : {formatted_number}
 {INFO_ADD} Status       : {status}
 {INFO_ADD} Country Code : {country_code}
 {INFO_ADD} Country      : {country}
 {INFO_ADD} Region       : {region}
 {INFO_ADD} Timezone     : {timezone_info}
 {INFO_ADD} Operator     : {operator}
 {INFO_ADD} Type Number  : {type_number}
\033[96m────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
\033[0m""")
        Continue()
        Reset()
    except:
        print(f"\033[96m {INFO} Invalid Format !\033[0m")
        Continue()
        Reset()
except Exception as e:
    Error(e)
