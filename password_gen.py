# password_gen.py
# secure password generator
import secrets
from string import digits, ascii_lowercase, ascii_uppercase


def _generate_pwd(length=8, uppercase=0, numeric=0, special=0):
    request_length = uppercase + numeric + special
    if length <= request_length:
        raise Exception(f'Total length uppercase, digits\
, and special characters({request_length}) \
must be 1 less than total length({length})')

    chars = ascii_lowercase
    if uppercase >= 1:
        chars += ascii_uppercase
    if numeric >= 1:
        chars += digits
    if special >= 1:
        chars += "!@#$%&*'()+,-./:=?_|"
    return ''.join(secrets.choice(chars) for c in range(length))


def _generate_secure_pwd(length=16, upper=0, digits=0, special=0):
    if length < upper + digits + special:
        raise ValueError('Nice Try!')
    while True:
        pwd = _generate_pwd(length=length, uppercase=upper,
                            numeric=digits, special=special)
        if (any(c.islower() for c in pwd) and sum(c.isupper() for c in pwd)
                >= upper and sum(c.isdigit() for c in pwd) >= digits
                and sum(not c.isalnum() for c in pwd) >= special):
            return pwd


def generate_password(length: int = 8,
                      upper: int = 1, digits: int = 1, special: int = 1,
                      cnt: int = 1) -> str:
    """Generates random password.\r
Takes in the following arguments:\r
length: Length of password to generate.\r
upper: Minimum number of uppercase characters.\r
digits: Minimum number of digits.\r
special: Minimum number of special characters (!@#$%&*'()+,-./:=?_|)\r
cnt: Number of passwords to generate."""
    passwords = []
    for p in range(cnt):
        p = _generate_secure_pwd(length, upper, digits, special)
        passwords.append(p)
    for p in passwords:
        return(p)
