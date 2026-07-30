import re
import hashlib
import hmac
import secrets
from collections import Counter
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

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
    check=hashlib.pbkdf2_hmac("sha256", password.encode(), a.encode(), 100_000).hex()

    return hmac.compare_digest(check,b)
   

def hash_password(password):
    salt=secrets.token_hex(16)
    digest =hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000).hex()
    return f"{salt}:{digest}"

def fmt_price(price):
    if not price: 
        return "Donation"
    return f"${price:.2f}"

def status_counts(rows, order):
    """'2 pending  .  1 active  . 3 sold'summary line for a row list."""
    counts = Counter(r.get("status") for r in rows)
    return "   .   ".join(f"{counts.get(s,0)} {s}" for s in order)

    

    



if __name__=="__main__":
    assert is_valid_email("a.b@macleans.school.nz")
    assert not is_valid_email("has space@a.nz")
    assert not is_valid_email ("has space@x.nz")
    assert parse_price("12.50") == 12.5
    assert parse_price("0") ==0
    assert parse_price("-1") is None
    assert parse_price("free") is None
    stored = hash_password("qwert12")
    assert len(stored) <= 100 and verify_password("qwert12",stored)
    assert not verify_password("wrong", stored)
    assert verify_password("plain", "plain")
    assert fmt_price(0) == "Donation" and fmt_price(None) =="Donation"
    assert fmt_price(12.5) == "$12.50"
    assert status_counts([{"status": "sold"}, {"status": "sold"}, {"status": "pending"}],
                         ("pending", "sold")) == "1 pending   ·   2 sold"
    print("helper self-check OK")

