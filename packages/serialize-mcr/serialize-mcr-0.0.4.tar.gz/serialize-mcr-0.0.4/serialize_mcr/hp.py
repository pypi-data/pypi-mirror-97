import re
import socket
import uuid

email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
url_regex = (f"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F]"
             f"[0-9a-fA-F]))+")
email_pattern = re.compile(email_regex)
url_pattern = re.compile(url_regex)


def _regex_match(regex, _str):
    try:
        pt = re.compile(regex)
        return pt.fullmatch(_str) is not None
    except re.error:
        return False


def _valid_regex(_str):
    try:
        re.compile(_str)
        return True
    except re.error:
        return False


def _valid_ipv4(_str):
    try:
        socket.inet_aton(_str)
        return True
    except:
        return False


def _valid_ipv6(_str):
    try:
        socket.inet_pton(socket.AF_INET6, _str)
        return True
    except:
        return False


def _valid_uuid(_str):
    if isinstance(_str, uuid.UUID):
        return True
    try:
        uuid.UUID(_str)
        return True
    except:
        return False


def _valid_email(_str):
    return email_pattern.fullmatch(_str) is not None


def _valid_url(_str):
    return url_pattern.fullmatch(_str) is not None


def _err(e, _name, _type=None, data=None, _default=None, _expected=None):
    if e == 0:
        return f"Property '{_name}' not found in {data}."
    elif e == 1:
        return f"Property '{_name}' is not nullable."
    elif e == 2:
        return f"Compound Property '{_name}' is not of type list or dict."
    elif e == 3:
        return (f"Compound Property '{_name}' does not have a proper "
                f"serialize-mcrr or schema.")
    elif e == 4:
        return (f"Property: '{_name}' with Value: '{data}' does not conform "
                f"with Type: {str(_type)}.")
    elif e == 5:
        return f"Type: {str(_type)} for property '{_name}' is not valid."
    elif e == 6:
        return f"Property: '{_name}' cannot have a default value when it is required."
    elif e == 7:
        return f"Property: '{_name}' does not have a defaulted value: {_default} that is of type: {_type}."
    elif e == 8:
        return f"Property: '{_name}' has an unexpected type: {_type}, expected: {_expected}."
    elif e == 9:
        return f"The following fields were invalid or misspelled: '{data}'."
    elif e == 10:
        return f"Property: {_name} is a null object and has no as_dict() attribute."

_spsstps = dict(
    uuid=_valid_uuid,
    ipv4=_valid_ipv4,
    ipv6=_valid_ipv6,
    email=_valid_email,
    url=_valid_url
)
