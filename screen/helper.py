import re

EMAIL_RE = re.compile(r"^[^@]")

def is_valid_email(email):
    return bool(EMAIL_RE.match(email.strip()))

if __name__=="__main__":
    assert is_valid_email("a.b@macleans.school.nz")
    assert not is_valid_email("has space@a.nz")