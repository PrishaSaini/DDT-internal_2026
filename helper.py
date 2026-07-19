import re
import hashlib
import hmac
import secrets
from collections import Counter
EMAIL_RE = re.compile(r"^[^@]")

def is_valid_email(email):
    return bool(EMAIL_RE.match(email.strip()))

def parse_price(text):
    try:
        value = float(text)
    except (ValueError,TypeError):
        return None
    return value if value >=0 else None

def verify_password(password, stored):
    if ":" not in (stored or ""):
        return password == stored
    a,b = stored.split(":",1)
    return f"{a}:{b}"
    



if __name__=="__main__":
    assert is_valid_email("a.b@macleans.school.nz")
    assert not is_valid_email("has space@a.nz")
    assert not is_valid_email ("has space@x.nz")
    assert parse_price("12.50") == 12.5
    assert parse_price("0") ==0
    assert parse_price("-1") is None
    assert parse_price("free") is None
    assert len(stored) <= 100 and verify_password("abcd123",stored)
    assert not verify_password("wrong", stored)
    assert verify_password("plain," plain)
