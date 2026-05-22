import hashlib

import bcrypt


def _normalize_password_bytes(password: str) -> bytes:
    """
    Normalize long passwords for bcrypt by hashing to a fixed length.
    """
    password_bytes = password.encode("utf-8")
    if len(password_bytes) <= 72:
        return password_bytes

    return hashlib.sha256(password_bytes).digest()


def hash_password(password: str) -> str:
    """
    Hashes a plain password using bcrypt algorithm.

    Args:
        password (str): The plain password to be hashed.

    Returns:
        str: The hashed password.
    """
    normalized = _normalize_password_bytes(password)
    return bcrypt.hashpw(normalized, bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain password against a hashed password.

    Args:
        plain_password (str): The plain password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the password is correct, False otherwise.
    """
    normalized = _normalize_password_bytes(plain_password)
    return bcrypt.checkpw(normalized, hashed_password.encode("utf-8"))
