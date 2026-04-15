import hashlib
import os
import binascii


def generate_salt(length: int = 32) -> str:
    """Generate a cryptographically secure random salt."""
    return binascii.hexlify(os.urandom(length)).decode('utf-8')


def hash_password(password: str, salt: str = None) -> tuple[str, str]:
    """
    Hash a password using SHA-256 + salt.
    Returns (password_hash, salt).
    """
    if salt is None:
        salt = generate_salt()
    salted = f"{salt}{password}"
    password_hash = hashlib.sha256(salted.encode('utf-8')).hexdigest()
    return password_hash, salt


def verify_password(password: str, stored_hash: str, salt: str) -> bool:
    """Verify a password against its stored hash and salt."""
    computed_hash, _ = hash_password(password, salt)
    return computed_hash == stored_hash
