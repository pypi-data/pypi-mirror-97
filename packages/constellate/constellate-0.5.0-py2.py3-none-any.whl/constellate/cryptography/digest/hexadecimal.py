import hashlib


def hex_sha256(value: str = None):
    h = hashlib.sha256()
    return _hex(value=value, hash=h)


def _hex(value: str = None, hash=None):
    hash.update(value.encode("utf-8"))
    return hash.hexdigest()
