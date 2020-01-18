import re

PAN = r'(?i)^[a-z]{3}[abcfghljpte][a-z]\d{4}[a-z]$'
MOBILE_NUMBER_REGEX = r'^[1-9][0-9]{9}$'
NAME_REGEX = r'(?i)^[a-z\s]{1,}[\.]{0,1}[a-z0-9\.\s]{0,}$'
PIN_REGEX = r'^[1-9]{1}[0-9]{5}$'
USERNAME_REGEX = r'^[\w.@+-]+$'
ALPHANUMERIC_WITH_SPACE = r'(?i)^[a-z\d\s]+$'


def validate_pan(value):
    if not value:
        return False
    return True if re.match(pattern=PAN, string=value) else False


def validate_mobile_number(value):
    if not value:
        return False
    return True if re.match(pattern=MOBILE_NUMBER_REGEX, string=value) else False


def validate_name(value):
    if not value:
        return False
    return True if re.match(pattern=NAME_REGEX, string=value) else False


def validate_pin(value):
    if not value:
        return False
    return True if re.match(pattern=PIN_REGEX, string=str(value)) else False


def validate_username(value):
    if not value:
        return False
    return True if re.match(pattern=USERNAME_REGEX, string=str(value)) else False


def validate_alphanumeric_with_space(value):
    if not value:
        return False
    return True if re.match(pattern=ALPHANUMERIC_WITH_SPACE, string=str(value)) else False
