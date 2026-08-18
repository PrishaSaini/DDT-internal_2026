import re
import hashlib
import hmac
import secrets
from collections import Counter
# Email must look like name@place.something with no spaces
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
# This is the shortest pwd length allowed
MIN_PASSWORD_LEN = 6

# How many times to scramble a passowr. More rounds means harder to crack
HASH_ROUNDS = 100_000

# Lisiting type basically means item is free
DONATION = "Donation"


def is_valid_email(email):
    """True if the text looks like an email adress"""
    return bool(EMAIL_RE.match((email or "").strip()))


def parse_price(text):
    """Turn typed text into a proce. None f it is not a valid price"""
    try:
        value = float(text)
    except (ValueError, TypeError):
        return None  # if not a number at all
    return value if value >= 0 else None


def verify_password(password, stored):
    """True if the password matches the stored one."""
    if ":" not in (stored or ""):
        return password == stored
    a, b = stored.split(":", 1)
    check = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), a.encode(), HASH_ROUNDS).hex()
# compare_b always will take the same amount of time so it give aways nothing.
    return hmac.compare_digest(check, b)


def hash_password(password):
    """ Scrambles a password for storing as salt:digest format."""
    # Random salt means if two people have same password they will get different results.
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), salt.encode(), 100_000).hex()
    return f"{salt}:{digest}"


def fmt_price(price, listing_type=None):
    """Price as 12.50 or Donation if the item is free"""
    if listing_type == DONATION or (listing_type is None and not price):
        return "Donation"
    return f"${price or 0:.2f}"


def status_counts(statuses, order):
    "This is for the summary line such s 2 pending .  1 active . 3 sold"
    counts = Counter(statuses)
    return "  .  ".join(f"{counts.get(s, 0)} {s}" for s in order)


if __name__ == "__main__":
    # Runs this file on its own to check the helpers still work
    # Emails are good, then bad
    assert is_valid_email("a.b@macleans.school.nz")
    assert not is_valid_email("has space@a.nz")
    assert not is_valid_email("no-at-sign.nz")
    assert not is_valid_email("")
    assert not is_valid_email(None)
    # Prices are normal, edge values then rubbish.
    assert parse_price("12.50") == 12.5
    assert parse_price("0") == 0  # free is allowed
    assert parse_price("-0.01") is None
    assert parse_price("-1") is None  # below 0 isn't
    assert parse_price("free") is None
    assert parse_price("") is None
    assert parse_price(None) is None
    # Passwords: right, wrong and an old plain-text one.
    stored = hash_password("qwert12")
    assert verify_password("qwert12", stored)
    assert not verify_password("wrong", stored)
    assert not verify_password("", stored)
    assert verify_password("plain", "plain")
    assert stored != "qwert12" and ":" in stored
    # Price on screen.
    assert fmt_price(0) == "Donation" and fmt_price(None) == "Donation"
    assert fmt_price(12.5) == "$12.50"
    assert fmt_price(0, "Sale") == "$0.00"
    assert fmt_price(5, DONATION) == "Donation"
    # Counts including an empty list
    assert len("abcde") < MIN_PASSWORD_LEN
    assert len("abcdef") >= MIN_PASSWORD_LEN
    assert status_counts(["sold", "sold", "pending"],
                         ("pending", "sold")) == "1 pending  .  2 sold"
    assert status_counts([], ("pending", "sold")) == "0 pending  .  0 sold"
